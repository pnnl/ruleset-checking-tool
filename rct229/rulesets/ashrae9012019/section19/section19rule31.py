from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.rulesets.ashrae9012019.data.schema_enums import schema_enums
from rct229.rulesets.ashrae9012019.ruleset_functions.get_hvac_systems_primarily_serving_comp_room import (
    get_hvac_systems_primarily_serving_comp_room,
)
from rct229.utils.pint_utils import ZERO

FAN_SYSTEM_OPERATION = schema_enums["FanSystemOperationOptions"]


class Section19Rule31(RuleDefinitionListIndexedBase):
    """Rule 31 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(Section19Rule31, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, False, True),
            each_rule=Section19Rule31.HVACRule(),
            index_rmr="proposed",
            id="19-31",
            description="HVAC fans in the proposed design model shall remain on during unoccupied hours in systems primarily serving computer rooms.",
            ruleset_section_title="HVAC - General",
            standard_section="Section G3.1-4 Schedules exception #3 for the proposed building",
            is_primary_rule=True,
            rmr_context="ruleset_model_instances/0",
            list_path="$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
        )

    def create_data(self, context, data):
        rmi_p = context.proposed

        hvac_systems_primarily_serving_comp_room_p = (
            get_hvac_systems_primarily_serving_comp_room(rmi_p)
        )

        return {
            "hvac_systems_primarily_serving_comp_room_p": hvac_systems_primarily_serving_comp_room_p
        }

    class HVACRule(RuleDefinitionBase):
        def __init__(self):
            super(Section19Rule31.HVACRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, False, True),
                required_fields={
                    "$": ["fan_system"],
                    "fan_system": [
                        "operation_during_unoccupied",
                        "minimum_outdoor_airflow",
                    ],
                },
            )

        def is_applicable(self, context, data=None):
            hvac_p = context.proposed
            hvac_id_p = hvac_p["id"]
            hvac_systems_primarily_serving_comp_room_p = data[
                "hvac_systems_primarily_serving_comp_room_p"
            ]

            return hvac_id_p in hvac_systems_primarily_serving_comp_room_p

        def get_calc_vals(self, context, data=None):
            hvac_p = context.proposed

            operation_during_unoccupied_p = hvac_p["fan_system"][
                "operation_during_unoccupied"
            ]
            minimum_outdoor_airflow_p = hvac_p["fan_system"]["minimum_outdoor_airflow"]

            return {
                "operation_during_unoccupied_p": operation_during_unoccupied_p,
                "minimum_outdoor_airflow_p": minimum_outdoor_airflow_p,
            }

        def rule_check(self, context, calc_vals=None, data=None):
            operation_during_unoccupied_p = calc_vals["operation_during_unoccupied_p"]
            minimum_outdoor_airflow_p = calc_vals["minimum_outdoor_airflow_p"]

            return (
                operation_during_unoccupied_p == FAN_SYSTEM_OPERATION.CONTINUOUS
                and minimum_outdoor_airflow_p > ZERO.FLOW
            ) or (
                operation_during_unoccupied_p == FAN_SYSTEM_OPERATION.CYCLING
                and minimum_outdoor_airflow_p == ZERO.FLOW
            )
