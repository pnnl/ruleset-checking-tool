from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.get_hvac_systems_serving_zone_health_safety_vent_reqs import (
    get_hvac_systems_serving_zone_health_safety_vent_reqs,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.pint_utils import ZERO

FAN_SYSTEM_OPERATION = SchemaEnums.schema_enums["FanSystemOperationOptions"]


class PRM9012019Rule88f26(RuleDefinitionListIndexedBase):
    """Rule 27 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(PRM9012019Rule88f26, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012019Rule88f26.HVACRule(),
            index_rmd=BASELINE_0,
            id="19-27",
            description="HVAC fans shall remain on during unoccupied hours in spaces that have health and safety mandated minimum ventilation requirements during unoccupied hours in the baseline design.",
            ruleset_section_title="HVAC - General",
            standard_section="Section G3.1-4 Schedules exception #2 for the proposed building and Section G3.1.2.4",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0",
            list_path="$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
        )

    def create_data(self, context, data):
        rmd_b = context.BASELINE_0
        applicable_hvac_systems_list_b = (
            get_hvac_systems_serving_zone_health_safety_vent_reqs(rmd_b)
        )

        return {"applicable_hvac_systems_list_b": applicable_hvac_systems_list_b}

    class HVACRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule88f26.HVACRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
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
            hvac_b = context.BASELINE_0
            hvac_id_b = hvac_b["id"]
            applicable_hvac_systems_list_b = data["applicable_hvac_systems_list_b"]

            return hvac_id_b in applicable_hvac_systems_list_b

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
            )

        def get_fail_msg(self, context, calc_vals=None, data=None):
            hvac_b = context.BASELINE_0
            hvac_id_b = hvac_b["id"]

            return f"{hvac_id_b} SERVES ZONE(S) THAT APPEAR LIKELY TO HAVE HEALTH AND SAFETY MANDATED MINIMUM VENTILATION REQUIREMENTS DURING UNOCCUPIED HOURS AND THEREFORE (IF THE HVAC SYSTEM SUPPLIES OA CFM) MAY WARRANT CONTINUOUS OPERATION DURING UNOCCUPIED HOURS PER SECTION G3.1-4 SCHEDULES EXCEPTION #2 FOR THE BASELINE BUILDING AND PER SECTION G3.1.2.4."
