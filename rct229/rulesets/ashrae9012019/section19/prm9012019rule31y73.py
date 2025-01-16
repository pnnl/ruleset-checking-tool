from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.get_hvac_systems_primarily_serving_comp_room import (
    get_hvac_systems_primarily_serving_comp_room,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.pint_utils import ZERO

FAN_SYSTEM_OPERATION = SchemaEnums.schema_enums["FanSystemOperationOptions"]


class PRM9012019Rule31y73(RuleDefinitionListIndexedBase):
    """Rule 32 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(PRM9012019Rule31y73, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012019Rule31y73.HVACRule(),
            index_rmd=BASELINE_0,
            id="19-32",
            description="HVAC fans in the baseline design model shall remain on during unoccupied hours in systems primarily serving computer rooms in the B_RMD.",
            ruleset_section_title="HVAC - General",
            standard_section="Section G3.1-4 Schedules exception #3 in the proposed column",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0",
            list_path="$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
        )

    def create_data(self, context, data):
        rmd_b = context.BASELINE_0

        hvac_systems_primarily_serving_comp_room_b = (
            get_hvac_systems_primarily_serving_comp_room(rmd_b)
        )

        return {
            "hvac_systems_primarily_serving_comp_room_b": hvac_systems_primarily_serving_comp_room_b
        }

    class HVACRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule31y73.HVACRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
            )

        def is_applicable(self, context, data=None):
            hvac_b = context.BASELINE_0
            hvac_id_b = hvac_b["id"]
            hvac_systems_primarily_serving_comp_room_b = data[
                "hvac_systems_primarily_serving_comp_room_b"
            ]

            return hvac_id_b in hvac_systems_primarily_serving_comp_room_b

        def get_calc_vals(self, context, data=None):
            hvac_b = context.BASELINE_0

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
