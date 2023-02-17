from rct229.data.schema_enums import schema_enums
from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.rulesets.ashrae9012019.ruleset_functions.get_area_type_window_wall_area_dict import (
    get_area_type_window_wall_area_dict,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_opaque_surface_type import (
    OpaqueSurfaceType as OST,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_opaque_surface_type import (
    get_opaque_surface_type,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_surface_conditioning_category_dict import (
    SurfaceConditioningCategory as SCC,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_surface_conditioning_category_dict import (
    get_surface_conditioning_category_dict,
)
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import ZERO, CalcQ
from rct229.utils.std_comparisons import std_equal

DOOR = schema_enums["SubsurfaceClassificationOptions"].DOOR
FAIL_MSG = "The vertical fenestration is not distributed across baseline opaque surfaces in the same proportion as in the proposed design. Verify if envelope is existing or altered and can be excluded from this check."


class Section5Rule21(RuleDefinitionListIndexedBase):
    """Rule 21 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

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
            ruleset_section_title="Envelope",
            standard_section="Section G3.1-5(c) Building Envelope Modeling Requirements for the Baseline building",
            is_primary_rule=True,
            list_path="ruleset_model_instances[0].buildings[*]",
            data_items={"climate_zone": ("baseline", "weather/climate_zone")},
        )

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section5Rule21.BuildingRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, True),
                required_fields={},
                each_rule=Section5Rule21.BuildingRule.AboveGradeWallRule(),
                index_rmr="baseline",
                # list_path and list_filter together determine the list of
                # above grade walls to be passed to AboveGradeWallRule
                list_path="$..surfaces[*]",
            )

        def create_data(self, context, data=None):
            building_b = context.baseline
            building_p = context.proposed
            climate_zone = data["climate_zone"]

            window_wall_areas_dictionary_b = get_area_type_window_wall_area_dict(
                climate_zone, building_b
            )
            window_wall_areas_dictionary_p = get_area_type_window_wall_area_dict(
                climate_zone, building_p
            )

            return {
                "total_fenestration_area_b": sum(
                    find_all("$..total_window_area", window_wall_areas_dictionary_b),
                    ZERO.AREA,
                ),
                "total_fenestration_area_p": sum(
                    find_all("$..total_window_area", window_wall_areas_dictionary_p),
                    ZERO.AREA,
                ),
                "surface_conditioning_category_dict_b": get_surface_conditioning_category_dict(
                    data["climate_zone"], building_b
                ),
            }

        def list_filter(self, context_item, data=None):
            surface_b = context_item.baseline

            return (
                get_opaque_surface_type(surface_b) == OST.ABOVE_GRADE_WALL
                and data["surface_conditioning_category_dict_b"][surface_b["id"]]
                != SCC.UNREGULATED
            )

        class AboveGradeWallRule(RuleDefinitionBase):
            def __init__(self):
                super(Section5Rule21.BuildingRule.AboveGradeWallRule, self).__init__(
                    rmrs_used=UserBaselineProposedVals(False, True, True),
                    required_fields={
                        "$": ["construction"],
                        "construction": ["u_factor"],
                    },
                    fail_msg=FAIL_MSG,
                )

            def get_calc_vals(self, context, data=None):
                above_grade_wall_b = context.baseline
                above_grade_wall_p = context.proposed

                def _helper_calc_val(above_grade_wall):
                    """Helper function for calculating the total fenestration area for an above grade wall"""
                    return sum(
                        [
                            subsurface.get("glazed_area", ZERO.AREA)
                            + subsurface.get("opaque_area", ZERO.AREA)
                            for subsurface in find_all(
                                "subsurfaces[*]", above_grade_wall
                            )
                            if (
                                getattr_(subsurface, "subsurface", "classification")
                                == DOOR
                                and (
                                    subsurface.get("glazed_area", ZERO.AREA)
                                    > subsurface.get("opaque_area", ZERO.AREA)
                                )
                                or (
                                    getattr_(subsurface, "subsurface", "classification")
                                    != DOOR
                                )
                            )
                        ],
                        ZERO.AREA,
                    )

                return {
                    "total_fenestration_area_surface_b": CalcQ(
                        "area", _helper_calc_val(above_grade_wall_b)
                    ),
                    "total_fenestration_area_b": CalcQ(
                        "area", data["total_fenestration_area_b"]
                    ),
                    "total_fenestration_area_surface_p": CalcQ(
                        "area", _helper_calc_val(above_grade_wall_p)
                    ),
                    "total_fenestration_area_p": CalcQ(
                        "area", data["total_fenestration_area_p"]
                    ),
                }

            def rule_check(self, context, calc_vals=None, data=None):
                total_fenestration_area_surface_b = calc_vals[
                    "total_fenestration_area_surface_b"
                ]
                total_fenestration_area_surface_p = calc_vals[
                    "total_fenestration_area_surface_p"
                ]
                total_fenestration_area_b = calc_vals["total_fenestration_area_b"]
                total_fenestration_area_p = calc_vals["total_fenestration_area_p"]

                return (
                    total_fenestration_area_b == ZERO.AREA
                    and total_fenestration_area_p == ZERO.AREA
                ) or std_equal(
                    (total_fenestration_area_surface_b / total_fenestration_area_b),
                    (total_fenestration_area_surface_p / total_fenestration_area_p),
                )
