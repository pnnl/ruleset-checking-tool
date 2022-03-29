from rct229.rule_engine.rule_base import (
    RuleDefinitionBase,
    RuleDefinitionListIndexedBase,
)
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.ruleset_functions.get_opaque_surface_type import (
    OpaqueSurfaceType as OST,
    get_opaque_surface_type,
)
from rct229.ruleset_functions.get_surface_conditioning_category_dict import (
    SurfaceConditioningCategory as SCC,
    get_surface_conditioning_category_dict,
)
from rct229.utils.jsonpath_utils import find_all

from rct229.utils.match_lists import match_lists_exactly_by_id


class Section5Rule17(RuleDefinitionListIndexedBase):
    """Rule 5 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule17, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, True),
            required_fields={
                "$": ["weather"],
                "weather": ["climate_zone"],
            },
            each_rule=Section5Rule17.BuildingRule(),
            index_rmr="proposed",
            id="5-17",
            description="Opaque surfaces that are not regulated (not part of opaque building envelope) must be modeled the same in the baseline as in the proposed design. ",
            list_path="ruleset_model_instances[0].buildings[*]",
        )

    def create_data(self, context, data=None):
        rmr_baseline = context.baseline
        return {"climate_zone": rmr_baseline["weather"]["climate_zone"]}

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section5Rule17.BuildingRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, True),
                required_fields={},
                each_rule=Section5Rule17.BuildingRule.UnregulatedSurfaceRule(),
                index_rmr="baseline",
            )

        def create_context_list(self, context, data=None):
            # List of all baseline roof surfaces to become the context for RoofRule
            scc = data["surface_conditioning_category_dict"]

            baseline_surfaces = find_all("$..surfaces[*]", context.baseline)
            proposed_surfaces = find_all("$..surfaces[*]", context.proposed)

            # This assumes that the surfaces matched by IDs between proposed and baseline
            matched_proposed_surfaces = match_lists_exactly_by_id(
                baseline_surfaces, proposed_surfaces
            )

            proposed_baseline_surface_pairs = zip(baseline_surfaces, matched_proposed_surfaces)

            return [
                UserBaselineProposedVals(None, surface_b, surface_p)
                for surface_b, surface_p in proposed_baseline_surface_pairs
                if scc[surface_b["id"]] == SCC.UNREGULATED
            ]

        def create_data(self, context, data=None):
            building = context.baseline
            # Merge into the existing data dict
            return {
                **data,
                "surface_conditioning_category_dict": get_surface_conditioning_category_dict(
                    data["climate_zone"], building
                ),
            }

        class UnregulatedSurfaceRule(RuleDefinitionBase):
            def __init__(self):
                super(Section5Rule17.BuildingRule.UnregulatedSurfaceRule, self).__init__(
                    rmrs_used=UserBaselineProposedVals(False, True, True),
                    required_fields={"$": ["construction"]},
                )

            def get_calc_vals(self, context, data=None):
                surface_b = context.baseline
                surface_p = context.proposed

                surface_b_type = get_opaque_surface_type(surface_b)
                surface_b_construction = surface_b["construction"]
                surface_p_type = None
                surface_p_construction = None

                if surface_p is not None:
                    surface_p_type = get_opaque_surface_type(surface_p)
                    surface_p_construction = surface_p["construction"]

                if surface_b_type in [OST.ABOVE_GRADE_WALL, OST.FLOOR, OST.ROOF]:
                    return {
                        "id": surface_b["id"],
                        "baseline_surface_type": surface_b_type,
                        "proposed_surface_type": surface_p_type,
                        "baseline_surface_u_factor": surface_b_construction.get("u_factor"),
                        "proposed_surface_u_factor": surface_p_construction if surface_p_construction is None else
                        surface_p_construction.get("u_factor")
                    }
                elif surface_b_type in [OST.UNHEATED_SOG, OST.HEATED_SOG]:
                    return {
                        "id": surface_b["id"],
                        "baseline_surface_type": surface_b_type,
                        "proposed_surface_type": surface_p_type,
                        "baseline_surface_f_factor": surface_b_construction.get("f_factor"),
                        "proposed_surface_f_factor": surface_p_construction if surface_p_construction is None else
                        surface_p_construction.get("f_factor")
                    }
                elif surface_b_type == OST.BELOW_GRADE_WALL:
                    return {
                        "id": surface_b["id"],
                        "baseline_surface_type": surface_b_type,
                        "proposed_surface_type": surface_p_type,
                        "baseline_surface_c_factor": surface_b_construction.get("c_factor"),
                        "proposed_surface_c_factor": surface_p_construction if surface_p_construction is None else
                        surface_p_construction.get("c_factor")
                    }
                else:
                    # Will never reach this line
                    # The OST defaults all unidentifiable surfaces to above wall grade
                    # Serve code completeness
                    return {
                        "id": surface_b["id"],
                        "baseline_surface_type": None,
                        "proposed_surface_type": None,
                        "baseline_surface_c_factor": None,
                        "proposed_surface_c_factor": None
                    }

            def rule_check(self, context, calc_vals, data=None):
                baseline_surface_type = calc_vals["baseline_surface_type"]
                proposed_surface_type = calc_vals["proposed_surface_type"]
                # Check 1. surface type needs to be matched
                if proposed_surface_type is None or baseline_surface_type != proposed_surface_type:
                    return False

                if baseline_surface_type in [OST.ABOVE_GRADE_WALL, OST.FLOOR, OST.ROOF]:
                    return calc_vals["proposed_surface_u_factor"] is not None or \
                            calc_vals["baseline_surface_u_factor"] is not None or \
                            calc_vals["baseline_surface_u_factor"] == calc_vals["proposed_surface_u_factor"]
                elif baseline_surface_type in [OST.UNHEATED_SOG, OST.HEATED_SOG]:
                    return calc_vals["proposed_surface_f_factor"] is not None or \
                            calc_vals["baseline_surface_f_factor"] is not None or \
                            calc_vals["baseline_surface_f_factor"] == calc_vals["proposed_surface_f_factor"]
                elif baseline_surface_type == OST.BELOW_GRADE_WALL:
                    return calc_vals["proposed_surface_c_factor"] is not None or \
                            calc_vals["baseline_surface_c_factor"] is not None or \
                            calc_vals["baseline_surface_c_factor"] == calc_vals["proposed_surface_c_factor"]
                else:
                    return False
