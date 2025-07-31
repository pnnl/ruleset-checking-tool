from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import PROPOSED
from rct229.rulesets.ashrae9012019.ruleset_functions.get_hvac_systems_primarily_serving_comp_room import (
    get_hvac_systems_primarily_serving_comp_room,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.pint_utils import ZERO

FAN_SYSTEM_OPERATION = SchemaEnums.schema_enums["FanSystemOperationOptions"]


class PRM9012019Rule58x03(RuleDefinitionListIndexedBase):
    """Rule 31 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(PRM9012019Rule58x03, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=False, PROPOSED=True
            ),
            each_rule=PRM9012019Rule58x03.HVACRule(),
            index_rmd=PROPOSED,
            id="19-31",
            description="HVAC fans in the proposed design model shall remain on during unoccupied hours in systems primarily serving computer rooms.",
            ruleset_section_title="HVAC - General",
            standard_section="Section G3.1-4 Schedules exception #3 for the proposed building",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0",
            list_path="$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
        )

    def create_data(self, context, data):
        rmd_p = context.PROPOSED

        hvac_systems_primarily_serving_comp_room_p = (
            get_hvac_systems_primarily_serving_comp_room(rmd_p)
        )

        return {
            "hvac_systems_primarily_serving_comp_room_p": hvac_systems_primarily_serving_comp_room_p
        }

    class HVACRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule58x03.HVACRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=False, PROPOSED=True
                ),
                required_fields={
                    "$": ["fan_system"],
                    "fan_system": [
                        "operation_during_unoccupied",
                        "minimum_outdoor_airflow",
                    ],
                },
            )

        def is_applicable(self, context, data=None):
            hvac_p = context.PROPOSED
            hvac_id_p = hvac_p["id"]
            hvac_systems_primarily_serving_comp_room_p = data[
                "hvac_systems_primarily_serving_comp_room_p"
            ]

            return hvac_id_p in hvac_systems_primarily_serving_comp_room_p

        def get_calc_vals(self, context, data=None):
            hvac_p = context.PROPOSED

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
