from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.schema.schema_enums import SchemaEnums
from rct229.rulesets.ashrae9012019.ruleset_functions.get_proposed_hvac_modeled_with_virtual_cooling import (
    get_proposed_hvac_modeled_with_virtual_cooling,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_proposed_hvac_modeled_with_virtual_heating import (
    get_proposed_hvac_modeled_with_virtual_heating,
)
from rct229.utils.pint_utils import ZERO

FAN_SYSTEM_OPERATION = SchemaEnums.schema_enums["FanSystemOperationOptions"]


class Section19Rule24(RuleDefinitionListIndexedBase):
    """Rule 24 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(Section19Rule24, self).__init__(
            rmrs_used=UserBaselineProposedVals(True, False, True),
            each_rule=Section19Rule24.HVACRule(),
            index_rmr="proposed",
            id="19-24",
            description="Schedules for HVAC fans that provide outdoor air for ventilation shall run continuously whenever spaces are occupied in the proposed design.",
            ruleset_section_title="HVAC - General",
            standard_section="Section G3.1-4 Schedules for the proposed building excluding exception #1 and Section G3.1.2.4.",
            is_primary_rule=True,
            rmr_context="ruleset_model_descriptions/0",
            list_path="$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
        )

    def create_data(self, context, data):
        user_p = context.user
        rmi_p = context.proposed

        inapplicable_hvac_sys_list_p = list(
            set(
                get_proposed_hvac_modeled_with_virtual_cooling(user_p, rmi_p)
                + get_proposed_hvac_modeled_with_virtual_heating(user_p, rmi_p)
            )
        )

        return {"inapplicable_hvac_sys_list_p": inapplicable_hvac_sys_list_p}

    class HVACRule(RuleDefinitionBase):
        def __init__(self):
            super(Section19Rule24.HVACRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(True, False, True),
                required_fields={
                    "$": ["fan_system"],
                    "fan_system": [
                        "operation_during_occupied",
                    ],
                },
            )

        def is_applicable(self, context, data=None):
            hvac_p = context.proposed
            hvac_id_p = hvac_p["id"]
            inapplicable_hvac_sys_list_p = data["inapplicable_hvac_sys_list_p"]

            return hvac_id_p not in inapplicable_hvac_sys_list_p

        def get_calc_vals(self, context, data=None):
            hvac_p = context.proposed

            operation_during_occupied_p = hvac_p["fan_system"][
                "operation_during_occupied"
            ]
            minimum_outdoor_airflow_p = hvac_p["fan_system"]["minimum_outdoor_airflow"]

            return {
                "operation_during_occupied_p": operation_during_occupied_p,
                "minimum_outdoor_airflow_p": minimum_outdoor_airflow_p,
            }

        def rule_check(self, context, calc_vals=None, data=None):
            operation_during_occupied_p = calc_vals["operation_during_occupied_p"]
            minimum_outdoor_airflow_p = calc_vals["minimum_outdoor_airflow_p"]

            return (
                operation_during_occupied_p == FAN_SYSTEM_OPERATION.CONTINUOUS
                and minimum_outdoor_airflow_p > ZERO.FLOW
            ) or (
                operation_during_occupied_p == FAN_SYSTEM_OPERATION.CYCLING
                and minimum_outdoor_airflow_p == ZERO.FLOW
            )
