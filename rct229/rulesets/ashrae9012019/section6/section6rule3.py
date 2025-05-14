from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import PROPOSED
from rct229.rulesets.ashrae9012019.ruleset_functions.get_building_segment_lighting_status_type_dict import (
    LightingStatusType,
    get_building_segment_lighting_status_type_dict,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import ZERO, CalcQ
from rct229.utils.std_comparisons import std_equal

OFFICE_OPEN_PLAN = SchemaEnums.schema_enums[
    "LightingSpaceOptions2019ASHRAE901TG37"
].OFFICE_OPEN_PLAN
FAIL_MSG = "Lighting exists or is submitted with design documents. Lighting power density in P_RMD does not match U_RMD."
MANUAL_CHECK_REQUIRED_MSG = "Lighting is not yet designed, or lighting is as-designed or as-existing but matches Table 9.5.1. Lighting power density in P_RMD does not match U_RMD."


class PRM9012019Rule73a47(RuleDefinitionListIndexedBase):
    """Rule 3 of ASHRAE 90.1-2019 Appendix G Section 6 (Lighting)"""

    def __init__(self):
        super(PRM9012019Rule73a47, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=True, BASELINE_0=False, PROPOSED=True
            ),
            each_rule=PRM9012019Rule73a47.BuildingSegmentRule(),
            index_rmd=PROPOSED,
            id="6-3",
            description="Where a complete lighting system exists, the actual lighting power for each building_segment shall be used in the model. Where a lighting system has been designed and submitted with design documents, lighting power shall be determined in accordance with Sections 9.1.3 and 9.1.4. Where lighting neither exists nor is submitted with design documents, lighting shall comply with but not exceed the requirements of Section 9. Lighting power shall be determined in accordance with the Building Area Method (Section 9.5.1).",
            ruleset_section_title="Lighting",
            standard_section="Section G3.1-6(a)(b)(c) Modeling Requirements for the Proposed Design",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0].buildings[*].building_segments[*]",
        )

    class BuildingSegmentRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(PRM9012019Rule73a47.BuildingSegmentRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=True, BASELINE_0=False, PROPOSED=True
                ),
                each_rule=PRM9012019Rule73a47.BuildingSegmentRule.SpaceRule(),
                index_rmd=PROPOSED,
                list_path="zones[*].spaces[*]",
            )

        def create_data(self, context, data=None):
            building_segment_p = context.PROPOSED
            return {
                "building_segment_lighting_status_type_dict_p": get_building_segment_lighting_status_type_dict(
                    building_segment_p
                )
            }

        class SpaceRule(RuleDefinitionBase):
            def __init__(self):
                super(PRM9012019Rule73a47.BuildingSegmentRule.SpaceRule, self).__init__(
                    fail_msg=FAIL_MSG,
                    manual_check_required_msg=MANUAL_CHECK_REQUIRED_MSG,
                    rmds_used=produce_ruleset_model_description(
                        USER=True, BASELINE_0=False, PROPOSED=True
                    ),
                    precision={
                        "total_space_lpd_p": {
                            "precision": 0.01,
                            "unit": "W/ft2",
                        }
                    },
                )

            def get_calc_vals(self, context, data=None):
                space_u = context.USER
                space_p = context.PROPOSED
                total_space_lpd_u = (
                    sum(find_all("$.interior_lighting[*].power_per_area", space_u))
                    or ZERO.POWER_PER_AREA
                )
                total_space_lpd_p = (
                    sum(find_all("$.interior_lighting[*].power_per_area", space_p))
                    or ZERO.POWER_PER_AREA
                )

                space_lighting_status_type_p = data[
                    "building_segment_lighting_status_type_dict_p"
                ][space_p["id"]]

                return {
                    "total_space_lpd_u": CalcQ("power_density", total_space_lpd_u),
                    "total_space_lpd_p": CalcQ("power_density", total_space_lpd_p),
                    "space_lighting_status_type_p": space_lighting_status_type_p,
                }

            def manual_check_required(self, context, calc_vals=None, data=None):
                space_lighting_status_type_p = calc_vals["space_lighting_status_type_p"]
                total_space_lpd_u = calc_vals["total_space_lpd_u"]
                total_space_lpd_p = calc_vals["total_space_lpd_p"]
                return (
                    not self.precision_comparison["total_space_lpd_p"](
                        total_space_lpd_u, total_space_lpd_p
                    )
                    and space_lighting_status_type_p
                    is not LightingStatusType.AS_DESIGNED_OR_AS_EXISTING
                )

            def rule_check(self, context, calc_vals=None, data=None):
                total_space_lpd_u = calc_vals["total_space_lpd_u"]
                total_space_lpd_p = calc_vals["total_space_lpd_p"]
                return self.precision_comparison["total_space_lpd_p"](
                    total_space_lpd_u, total_space_lpd_p
                )

            def is_tolerance_fail(self, context, calc_vals=None, data=None):
                total_space_lpd_u = calc_vals["total_space_lpd_u"]
                total_space_lpd_p = calc_vals["total_space_lpd_p"]
                return std_equal(total_space_lpd_u, total_space_lpd_p)
