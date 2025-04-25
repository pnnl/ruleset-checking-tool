from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.data_fns.table_G3_7_fns import table_G3_7_lookup
from rct229.rulesets.ashrae9012019.ruleset_functions.get_avg_zone_height import (
    get_avg_zone_height,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_building_segment_lighting_status_type_dict import (
    LightingStatusType,
    get_building_segment_lighting_status_type_dict,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import CalcQ
from rct229.utils.std_comparisons import std_equal

OFFICE_OPEN_PLAN = SchemaEnums.schema_enums[
    "LightingSpaceOptions2019ASHRAE901TG37"
].OFFICE_OPEN_PLAN
FAIL_MSG = "P_RMD lighting status type is as-designed or as-existing. But lighting space type in B_RMD is not specified."


class PRM9012019Rule22l93(RuleDefinitionListIndexedBase):
    """Rule 4 of ASHRAE 90.1-2019 Appendix G Section 6 (Lighting)"""

    def __init__(self):
        super(PRM9012019Rule22l93, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=PRM9012019Rule22l93.BuildingSegmentRule(),
            index_rmd=BASELINE_0,
            id="6-4",
            description='Where a complete lighting system exists and where a lighting system has been designed and submitted with design documents, the baseline LPD is equal to expected value in Table G3.7. Where lighting neither exists nor is submitted with design documents, baseline LPD shall be determined in accordance with Table G3-7 for "Office-Open Plan" space type.',
            ruleset_section_title="Lighting",
            standard_section="Section G3.1-6 Modeling Requirements for the Baseline",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0].buildings[*].building_segments[*]",
        )

    class BuildingSegmentRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(PRM9012019Rule22l93.BuildingSegmentRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=True
                ),
                each_rule=PRM9012019Rule22l93.BuildingSegmentRule.ZoneRule(),
                index_rmd=BASELINE_0,
                list_path="zones[*]",
            )

        def create_data(self, context, data=None):
            building_segment_p = context.PROPOSED

            return {
                "building_segment_lighting_status_type_dict_p": get_building_segment_lighting_status_type_dict(
                    building_segment_p
                )
            }

        class ZoneRule(RuleDefinitionListIndexedBase):
            def __init__(self):
                super(PRM9012019Rule22l93.BuildingSegmentRule.ZoneRule, self).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False, BASELINE_0=True, PROPOSED=True
                    ),
                    each_rule=PRM9012019Rule22l93.BuildingSegmentRule.ZoneRule.SpaceRule(),
                    index_rmd=BASELINE_0,
                    list_path="spaces[*]",
                )

            def create_data(self, context, data=None):
                zone_b = context.BASELINE_0

                # We will need this after Weili's update to table_G3_7_lookup()
                return {"avg_zone_ht_b": get_avg_zone_height(zone_b)}

            class SpaceRule(RuleDefinitionBase):
                def __init__(self):
                    super(
                        PRM9012019Rule22l93.BuildingSegmentRule.ZoneRule.SpaceRule, self
                    ).__init__(
                        fail_msg=FAIL_MSG,
                        rmds_used=produce_ruleset_model_description(
                            USER=False, BASELINE_0=True, PROPOSED=True
                        ),
                        precision={
                            "total_space_lpd_b": {
                                "precision": 1,
                                "unit": "W/m2",
                            },
                        },
                    )

                def get_calc_vals(self, context, data=None):
                    space_b = context.BASELINE_0
                    space_p = context.PROPOSED
                    total_space_lpd_b = sum(
                        find_all("$.interior_lighting[*].power_per_area", space_b)
                    )
                    space_lighting_status_type_p = data[
                        "building_segment_lighting_status_type_dict_p"
                    ][space_p["id"]]
                    lpd_allowance_b = (
                        table_G3_7_lookup(
                            space_b["lighting_space_type"],
                            data["avg_zone_ht_b"],
                            getattr_(space_b, "Space", "floor_area"),
                        )
                        if "lighting_space_type" in space_b
                        else table_G3_7_lookup(
                            OFFICE_OPEN_PLAN,
                            data["avg_zone_ht_b"],
                            getattr_(space_b, "Space", "floor_area"),
                        )
                    )["lpd"]

                    return {
                        "total_space_lpd_b": CalcQ("power_density", total_space_lpd_b),
                        "space_lighting_status_type_p": space_lighting_status_type_p,
                        "lpd_allowance_b": CalcQ("power_density", lpd_allowance_b),
                    }

                def rule_check(self, context, calc_vals=None, data=None):
                    space_b = context.BASELINE_0
                    lighting_space_type_b = space_b.get("lighting_space_type")

                    space_lighting_status_type_p = calc_vals[
                        "space_lighting_status_type_p"
                    ]
                    total_space_lpd_b = calc_vals["total_space_lpd_b"]
                    lpd_allowance_b = calc_vals["lpd_allowance_b"]

                    return (
                        # Not Case 1
                        not (
                            space_lighting_status_type_p
                            == LightingStatusType.AS_DESIGNED_OR_AS_EXISTING
                            and not lighting_space_type_b
                        )
                        # Passes for both values of space_lighting_status_type_p
                        and (
                            space_lighting_status_type_p
                            in [
                                LightingStatusType.AS_DESIGNED_OR_AS_EXISTING,
                                LightingStatusType.NOT_YET_DESIGNED_OR_MATCH_TABLE_9_5_1,
                            ]
                            and self.precision_comparison["total_space_lpd_b"](
                                total_space_lpd_b, lpd_allowance_b
                            )
                        )
                    )

                def is_tolerance_fail(self, context, calc_vals=None, data=None):
                    space_b = context.BASELINE_0
                    lighting_space_type_b = space_b.get("lighting_space_type")

                    space_lighting_status_type_p = calc_vals[
                        "space_lighting_status_type_p"
                    ]
                    total_space_lpd_b = calc_vals["total_space_lpd_b"]
                    lpd_allowance_b = calc_vals["lpd_allowance_b"]

                    return (
                        # Not Case 1
                        not (
                            space_lighting_status_type_p
                            == LightingStatusType.AS_DESIGNED_OR_AS_EXISTING
                            and not lighting_space_type_b
                        )
                        # Passes for both values of space_lighting_status_type_p
                        and (
                            space_lighting_status_type_p
                            in [
                                LightingStatusType.AS_DESIGNED_OR_AS_EXISTING,
                                LightingStatusType.NOT_YET_DESIGNED_OR_MATCH_TABLE_9_5_1,
                            ]
                            and std_equal(lpd_allowance_b, total_space_lpd_b)
                        )
                    )

                def get_fail_msg(self, context, calc_vals=None, data=None):
                    space_b = context.BASELINE_0
                    lighting_space_type_b = space_b.get("lighting_space_type")

                    space_lighting_status_type_p = calc_vals[
                        "space_lighting_status_type_p"
                    ]

                    return (
                        "P_RMD lighting status type is as-designed or as-existing. But lighting space type in B_RMD is not specified."
                        if space_lighting_status_type_p
                        == LightingStatusType.AS_DESIGNED_OR_AS_EXISTING
                        and not lighting_space_type_b
                        else ""
                    )
