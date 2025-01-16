from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import PROPOSED
from rct229.rulesets.ashrae9012019.ruleset_functions.get_proposed_hvac_modeled_with_virtual_cooling import (
    get_proposed_hvac_modeled_with_virtual_cooling,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_proposed_hvac_modeled_with_virtual_heating import (
    get_proposed_hvac_modeled_with_virtual_heating,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import getattr_
from rct229.utils.pint_utils import ZERO, CalcQ

FAN_SYSTEM_OPERATION = SchemaEnums.schema_enums["FanSystemOperationOptions"]


class PRM9012019Rule54e25(RuleDefinitionListIndexedBase):
    """Rule 24 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(PRM9012019Rule54e25, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=True, BASELINE_0=False, PROPOSED=True
            ),
            each_rule=PRM9012019Rule54e25.HVACRule(),
            index_rmd=PROPOSED,
            id="19-24",
            description="Schedules for HVAC fans that provide outdoor air for ventilation shall run continuously whenever spaces are occupied in the proposed design.",
            ruleset_section_title="HVAC - General",
            standard_section="Section G3.1-4 Schedules for the proposed building excluding exception #1 and Section G3.1.2.4.",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0",
            list_path="$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
        )

    def create_data(self, context, data):
        user_p = context.USER
        rmd_p = context.PROPOSED

        inapplicable_hvac_sys_list_p = list(
            set(
                get_proposed_hvac_modeled_with_virtual_cooling(user_p, rmd_p)
                + get_proposed_hvac_modeled_with_virtual_heating(user_p, rmd_p)
            )
        )

        return {"inapplicable_hvac_sys_list_p": inapplicable_hvac_sys_list_p}

    class HVACRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule54e25.HVACRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=False, PROPOSED=True
                ),
            )

        def is_applicable(self, context, data=None):
            hvac_p = context.PROPOSED
            hvac_id_p = hvac_p["id"]
            inapplicable_hvac_sys_list_p = data["inapplicable_hvac_sys_list_p"]

            return hvac_id_p not in inapplicable_hvac_sys_list_p

        def get_calc_vals(self, context, data=None):
            hvac_p = context.PROPOSED

            operation_during_occupied_p = getattr_(
                hvac_p,
                "heating_ventilating_air_conditioning_systems",
                "fan_system",
                "operation_during_occupied",
            )
            minimum_outdoor_airflow_p = getattr_(
                hvac_p,
                "heating_ventilating_air_conditioning_systems",
                "fan_system",
                "minimum_outdoor_airflow",
            )

            return {
                "operation_during_occupied_p": operation_during_occupied_p,
                "minimum_outdoor_airflow_p": CalcQ(
                    "air_flow_rate", minimum_outdoor_airflow_p
                ),
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
