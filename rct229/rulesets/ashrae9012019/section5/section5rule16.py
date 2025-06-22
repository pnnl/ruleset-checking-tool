from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
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
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import ZERO, CalcQ
from rct229.utils.std_comparisons import std_equal

DOOR = SchemaEnums.schema_enums["SubsurfaceClassificationOptions"].DOOR
FAIL_MSG = "The vertical fenestration is not distributed across baseline opaque surfaces in the same proportion as in the proposed design. Verify if envelope is existing or altered and can be excluded from this check."


class PRM9012019Rule80o45(RuleDefinitionListIndexedBase):
    """Rule 16 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(PRM9012019Rule80o45, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=PRM9012019Rule80o45.BuildingRule(),
            index_rmd=BASELINE_0,
            id="5-16",
            description="The vertical fenestration shall be distributed on each face of the building in the same proportion as in the proposed design.",
            ruleset_section_title="Envelope",
            standard_section="Section G3.1-5(c) Building Envelope Modeling Requirements for the Baseline building",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0].buildings[*]",
            required_fields={
                "$.ruleset_model_descriptions[*]": ["weather"],
                "weather": ["climate_zone"],
            },
        )

    def create_data(self, context, data=None):
        rpd_b = context.BASELINE_0
        climate_zone = rpd_b["ruleset_model_descriptions"][0]["weather"]["climate_zone"]
        constructions = rpd_b["ruleset_model_descriptions"][0].get("constructions")
        return {
            "climate_zone": climate_zone,
            "constructions": constructions,
        }

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(PRM9012019Rule80o45.BuildingRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=True
                ),
                required_fields={},
                each_rule=PRM9012019Rule80o45.BuildingRule.AboveGradeWallRule(),
                index_rmd=BASELINE_0,
                # list_path and list_filter together determine the list of
                # above grade walls to be passed to AboveGradeWallRule
                list_path="$.building_segments[*].zones[*].surfaces[*]",
            )

        def create_data(self, context, data=None):
            building_b = context.BASELINE_0
            building_p = context.PROPOSED
            climate_zone = data["climate_zone"]
            constructions = data["constructions"]

            window_wall_areas_dictionary_b = get_area_type_window_wall_area_dict(
                climate_zone, constructions, building_b
            )
            window_wall_areas_dictionary_p = get_area_type_window_wall_area_dict(
                climate_zone, constructions, building_p
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
                    data["climate_zone"], building_b, data["constructions"]
                ),
            }

        def list_filter(self, context_item, data=None):
            surface_b = context_item.BASELINE_0

            return (
                get_opaque_surface_type(surface_b) == OST.ABOVE_GRADE_WALL
                and data["surface_conditioning_category_dict_b"][surface_b["id"]]
                != SCC.UNREGULATED
            )

        class AboveGradeWallRule(RuleDefinitionBase):
            def __init__(self):
                super(
                    PRM9012019Rule80o45.BuildingRule.AboveGradeWallRule, self
                ).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False, BASELINE_0=True, PROPOSED=True
                    ),
                    required_fields={
                        "$": ["construction"],
                    },
                    precision={
                        "total_fenestration_area_surface_b / total_fenstration_area_b": {
                            "precision": 0.01,
                            "unit": "",
                        }
                    },
                    fail_msg=FAIL_MSG,
                )

            def get_calc_vals(self, context, data=None):
                above_grade_wall_b = context.BASELINE_0
                above_grade_wall_p = context.PROPOSED

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
                ) or (
                    self.precision_comparison[
                        "total_fenestration_area_surface_b / total_fenstration_area_b"
                    ](
                        (
                            total_fenestration_area_surface_b
                            / total_fenestration_area_b
                        ).magnitude,
                        (
                            total_fenestration_area_surface_p
                            / total_fenestration_area_p
                        ).magnitude,
                    )
                )

            def is_tolerance_fail(self, context, calc_vals=None, data=None):
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
                ) or (
                    std_equal(
                        (
                            total_fenestration_area_surface_b
                            / total_fenestration_area_b
                        ).magnitude,
                        (
                            total_fenestration_area_surface_p
                            / total_fenestration_area_p
                        ).magnitude,
                    )
                )
