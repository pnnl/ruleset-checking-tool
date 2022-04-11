from rct229.data.schema_enums import schema_enums
from rct229.rule_engine.rule_base import RuleDefinitionListIndexedBase, RuleDefinitionBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.ruleset_functions.get_area_type_window_wall_area_dict import get_area_type_window_wall_area_dict
from rct229.ruleset_functions.get_opaque_surface_type import (OpaqueSurfaceType as OST, get_opaque_surface_type)
from rct229.utils.assertions import getattr_, MissingKeyException
from rct229.utils.jsonpath_utils import find_all
from rct229.ruleset_functions.get_surface_conditioning_category_dict import (SurfaceConditioningCategory as SCC, get_surface_conditioning_category_dict)
from rct229.utils.match_lists import match_lists_by_id
from rct229.utils.pint_utils import ZERO

DOOR = schema_enums["SubsurfaceClassificationType"].DOOR.name


class Section5Rule21(RuleDefinitionListIndexedBase):
    """Rule 5 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule21, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, True),
            required_fields={
                "$": ["weather"],
                "weather": ["climate_zone"],
            },
            each_rule=Section5Rule21.BuildingRule(),
            index_rmr="baseline",
            id="5-21",
            description="The vertical fenestration shall be distributed on each face of the building in the same proportion as in the proposed design.",
            list_path="ruleset_model_instances[0].buildings[*]",
        )

    def create_data(self, context, data=None):
        rmr_baseline = context.baseline
        return {"climate_zone": rmr_baseline["weather"]["climate_zone"]}

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section5Rule21.BuildingRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, True),
                required_fields={},
                each_rule=Section5Rule21.BuildingRule.AboveGradeWallRule(),
                index_rmr="baseline",
            )

        def create_data(self, context, data=None):
            building_b = context.baseline
            building_p = context.proposed
            climate_zone = data["climate_zone"]

            window_wall_areas_dictionary_b = get_area_type_window_wall_area_dict(climate_zone, building_b)
            window_wall_areas_dictionary_p = get_area_type_window_wall_area_dict(climate_zone, building_p)

            return {
                **data,
                "total_fenestration_area_b": sum(find_all("$..total_window_area", window_wall_areas_dictionary_b), ZERO.AREA),
                "total_fenestration_area_p": sum(find_all("$..total_window_area", window_wall_areas_dictionary_p), ZERO.AREA),
                "surface_conditioning_category_dict_b": get_surface_conditioning_category_dict(
                    data["climate_zone"], building_b
                ),
            }

        def create_context_list(self, context, data=None):
            building_b = context.baseline
            building_p = context.proposed

            scc = data["surface_conditioning_category_dict_b"]

            baseline_surfaces = find_all("$..surfaces[*]", building_b)
            proposed_surfaces = find_all("$..surfaces[*]", building_p)

            matched_proposed_surfaces = match_lists_by_id(baseline_surfaces, proposed_surfaces)
            proposed_baseline_surface_pairs = zip(baseline_surfaces, matched_proposed_surfaces)
            # List of all baseline above grade wall to become the context for AboveGradeWall
            return [
                UserBaselineProposedVals(None, surface_b, surface_p)
                for surface_b, surface_p in proposed_baseline_surface_pairs
                if get_opaque_surface_type(surface_b) == OST.ABOVE_GRADE_WALL and scc[surface_b["id"]] != SCC.UNREGULATED
            ]

        class AboveGradeWallRule(RuleDefinitionBase):
            def __init__(self):
                super(Section5Rule21.BuildingRule.AboveGradeWallRule, self).__init__(
                    rmrs_used=UserBaselineProposedVals(False, True, True),
                    required_fields={
                        "$": ["construction"],
                        "construction": ["u_factor"],
                    },
                )

            @staticmethod
            def _helper_calc_val(above_grade_wall):
                """Helper function for calculating the total fenestration area for an above grade wall"""

                return sum([
                    subsurface.get("glazed_area", ZERO.AREA) + subsurface.get("opaque_area", ZERO.AREA)
                    for subsurface in find_all("subsurfaces[*]", above_grade_wall)
                    if (subsurface["classification"] == DOOR and
                        (subsurface.get("glazed_area", ZERO.AREA) > subsurface.get("opaque_area", ZERO.AREA)) or
                        (subsurface["classification"] != DOOR))
                ], ZERO.AREA)

            def get_calc_vals(self, context, data=None):
                above_grade_wall_b = context.baseline
                above_grade_wall_p = context.proposed

                if (above_grade_wall_b.get["subsurfaces"] ^ above_grade_wall_p.get["subsurfaces"]) or \
                        (data["total_fenestration_area_b"] == 0.0 ^ data["total_fenestration_area_p"] == 0.0):
                    # baseline & proposed mismatch:
                    # baseline has subsurface xor proposed has subsurface or
                    # baseline fenestration area == 0 xor proposed fenestration area == 0
                    return {
                        "total_fenestration_area_surface_b": None,
                        "total_fenestration_area_b": None,
                        "total_fenestration_area_surface_p": None,
                        "total_fenestration_area_p": None
                    }

                total_fenestration_area_surface_b = 0.0
                total_fenestration_area_b = data["total_fenestration_area_b"]
                total_fenestration_area_surface_p = 0.0
                total_fenestration_area_p = data["total_fenestration_area_p"]

                calc_val = {
                    "total_fenestration_area_surface_b": total_fenestration_area_surface_b,
                    "total_fenestration_area_b": total_fenestration_area_b,
                    "total_fenestration_area_surface_p": total_fenestration_area_surface_p,
                    "total_fenestration_area_p": total_fenestration_area_p
                }

                try:
                    self._helper_calc_val(total_fenestration_area_surface_b, above_grade_wall_b)
                    self._helper_calc_val(total_fenestration_area_surface_p, above_grade_wall_p)
                except MissingKeyException as e:
                    error = f"Missing key in object: {str(e)}, rule check stopped."
                    return {
                        "error": error
                    }

                return {
                    **calc_val
                }

            def manual_check_required(self, context, calc_vals=None, data=None):
                return "error" in calc_vals.keys()

            def rule_check(self, context, calc_vals=None, data=None):
                if calc_vals["total_fenestration_area_surface_b"] is None and calc_vals["total_fenestration_area_surface_p"] is None \
                        and calc_vals["total_fenestration_area_b"] is None and calc_vals["total_fenestration_area_p"] is None:
                    # Failed case where baseline mismatch proposed
                    return False
                else:
                    total_fenestration_area_surface_b = calc_vals["total_fenestration_area_surface_b"]
                    total_fenestration_area_surface_p = calc_vals["total_fenestration_area_surface_p"]
                    total_fenestration_area_b = calc_vals["total_fenestration_area_b"]
                    total_fenestration_area_p = calc_vals["total_fenestration_area_p"]

                    if total_fenestration_area_b == 0.0 and total_fenestration_area_p == 0.0:
                        # No fenestration in this building, avoid 0.0 division
                        return True

                    return (total_fenestration_area_surface_b / total_fenestration_area_b) == \
                           (total_fenestration_area_surface_p / total_fenestration_area_p)








