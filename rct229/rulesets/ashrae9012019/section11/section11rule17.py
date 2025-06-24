from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import PROPOSED
from rct229.rulesets.ashrae9012019.ruleset_functions.get_building_segment_swh_bat import (
    get_building_segment_swh_bat,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_swh_uses_associated_with_each_building_segment import (
    get_swh_uses_associated_with_each_building_segment,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all

SERVICE_WATER_HEATING_SPACE = SchemaEnums.schema_enums[
    "ServiceWaterHeatingAreaOptions2019ASHRAE901"
]


class PRM9012019Rule63z32(RuleDefinitionListIndexedBase):
    """Rule 17 of ASHRAE 90.1-2019 Appendix G Section 11 (Service Water Heating)"""

    def __init__(self):
        super(PRM9012019Rule63z32, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=PRM9012019Rule63z32.RMDRule(),
            index_rmd=PROPOSED,
            id="11-17",
            description="All buildings that will have service water heating loads must include those loads in the simulation.",
            ruleset_section_title="Service Water Heating",
            standard_section="Table G3.1 #1, proposed column, (a)",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0]",
        )

    class RMDRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(PRM9012019Rule63z32.RMDRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=False, PROPOSED=True
                ),
                each_rule=PRM9012019Rule63z32.RMDRule.BuildingSegmentRule(),
                index_rmd=PROPOSED,
                list_path="$.buildings[*].building_segments[*]",
            )

        def create_data(self, context, data):
            rmd_p = context.PROPOSED
            is_leap_year_p = True

            swh_bat = {
                bldg_seg_id: get_building_segment_swh_bat(
                    rmd_p, bldg_seg_id, is_leap_year_p
                )
                for bldg_seg_id in find_all(
                    "$.buildings[*].building_segments[*].id", rmd_p
                )
            }

            service_water_heating_use_ids = (
                get_swh_uses_associated_with_each_building_segment(rmd_p)
            )

            return {
                "swh_bat": swh_bat,
                "service_water_heating_use_ids": service_water_heating_use_ids,
            }

        class BuildingSegmentRule(RuleDefinitionBase):
            def __init__(self):
                super(PRM9012019Rule63z32.RMDRule.BuildingSegmentRule, self).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False, BASELINE_0=False, PROPOSED=True
                    )
                )

            def get_calc_vals(self, context, data=None):
                bldg_seg_p = context.PROPOSED
                service_water_heating_use_ids = data["service_water_heating_use_ids"]
                swh_bat = data["swh_bat"][bldg_seg_p["id"]]

                has_swh_loads = any(
                    [
                        getattr_(swh_use, "service_water_heating_uses", "use") > 0.0
                        for service_water_heating_use_id in service_water_heating_use_ids
                        for swh_use in find_all(
                            f'$.zones[*].spaces[*].service_water_heating_uses[*][?(@.id="{service_water_heating_use_id}")]',
                            bldg_seg_p,
                        )
                    ]
                )

                return {
                    "has_swh_loads": has_swh_loads,
                    "swh_bat": swh_bat,
                }

            def manual_check_required(self, context, calc_vals=None, data=None):
                swh_bat = calc_vals["swh_bat"]

                return swh_bat in (
                    "UNDETERMINED",
                    SERVICE_WATER_HEATING_SPACE.ALL_OTHERS,
                    SERVICE_WATER_HEATING_SPACE.WAREHOUSE,
                    SERVICE_WATER_HEATING_SPACE.PARKING_GARAGE,
                )

            def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
                swh_bat = calc_vals["swh_bat"]

                manual_check_msg = ""
                if swh_bat == "UNDETERMINED":
                    manual_check_msg = (
                        f"No SWH loads were simulated. The SWH Building Area type is UNDETERMINED, "
                        f"so this rule cannot assess whether building type is likely to have SWH loads. Recommend manual check "
                        f"to determine if SWH loads should have been simulated based on whether the building will have SWH loads."
                    )
                elif swh_bat in (
                    SERVICE_WATER_HEATING_SPACE.ALL_OTHERS,
                    SERVICE_WATER_HEATING_SPACE.WAREHOUSE,
                    SERVICE_WATER_HEATING_SPACE.PARKING_GARAGE,
                ):
                    manual_check_msg = (
                        f"There are no service water heating loads simulated in this building segment. "
                        f"SWH Building Area type is {swh_bat}. Confirm that there will be no service water heating loads in this building segment."
                    )

                return manual_check_msg

            def rule_check(self, context, calc_vals=None, data=None):
                has_swh_loads = calc_vals["has_swh_loads"]

                return has_swh_loads

            def get_fail_msg(self, context, calc_vals=None, data=None):
                swh_bat = calc_vals["swh_bat"]

                return (
                    f"There were no service water heating loads simulated in this building segment. "
                    f"Service water heating loads are expected for Building Area Type: {swh_bat}"
                )
