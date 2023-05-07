from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.rulesets.ashrae9012019.data.schema_enums import schema_enums
from rct229.rulesets.ashrae9012019.ruleset_functions.get_hvac_systems_primarily_serving_comp_room import (
    get_hvac_systems_primarily_serving_comp_room,
)
from rct229.utils.pint_utils import ZERO

FAN_SYSTEM_OPERATION = schema_enums["FanSystemOperationOptions"]


class Section19Rule32(RuleDefinitionListIndexedBase):
    """Rule 32 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(Section19Rule32, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section19Rule32.HVACRule(),
            index_rmr="baseline",
            id="19-32",
            description="HVAC fans in the baseline design model shall remain on during unoccupied hours in systems primarily serving computer rooms in the B_RMR.",
            ruleset_section_title="HVAC - General",
            standard_section="Section G3.1-4 Schedules exception #3 in the proposed column",
            is_primary_rule=True,
            rmr_context="ruleset_model_instances/0",
            list_path="$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
        )

    def create_data(self, context, data):
        rmi_b = context.baseline

        hvac_systems_primarily_serving_comp_room_b = (
            get_hvac_systems_primarily_serving_comp_room(rmi_b)
        )

        return {
            "hvac_systems_primarily_serving_comp_room_b": hvac_systems_primarily_serving_comp_room_b
        }

    class HVACRule(RuleDefinitionBase):
        def __init__(self):
            super(Section19Rule32.HVACRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
            )

        def is_applicable(self, context, data=None):
            hvac_b = context.baseline
            hvac_id_b = hvac_b["id"]
            hvac_systems_primarily_serving_comp_room_b = data[
                "hvac_systems_primarily_serving_comp_room_b"
            ]

            return hvac_id_b in hvac_systems_primarily_serving_comp_room_b

        def get_calc_vals(self, context, data=None):
            hvac_b = context.baseline

            operation_during_unoccupied_b = hvac_b["fan_system"][
                "operation_during_unoccupied"
            ]
            minimum_outdoor_airflow_b = hvac_b["fan_system"]["minimum_outdoor_airflow"]

            return {
                "operation_during_unoccupied_b": operation_during_unoccupied_b,
                "minimum_outdoor_airflow_b": minimum_outdoor_airflow_b,
            }

        def rule_check(self, context, calc_vals=None, data=None):
            operation_during_unoccupied_b = calc_vals["operation_during_unoccupied_b"]
            minimum_outdoor_airflow_b = calc_vals["minimum_outdoor_airflow_b"]

            return (
                operation_during_unoccupied_b == FAN_SYSTEM_OPERATION.CONTINUOUS
                and minimum_outdoor_airflow_b > ZERO.FLOW
            ) or (
                operation_during_unoccupied_b == FAN_SYSTEM_OPERATION.CYCLING
                and minimum_outdoor_airflow_b == ZERO.FLOW
            )
