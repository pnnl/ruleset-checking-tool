from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import PROPOSED
from rct229.rulesets.ashrae9012019.ruleset_functions.get_hvac_systems_serving_zone_health_safety_vent_reqs import (
    get_hvac_systems_serving_zone_health_safety_vent_reqs,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.pint_utils import ZERO

FAN_SYSTEM_OPERATION = SchemaEnums.schema_enums["FanSystemOperationOptions"]


class PRM9012019Rule09g49(RuleDefinitionListIndexedBase):
    """Rule 26 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(PRM9012019Rule09g49, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=False, PROPOSED=True
            ),
            each_rule=PRM9012019Rule09g49.HVACRule(),
            index_rmd=PROPOSED,
            id="19-26",
            description="HVAC fans shall remain on during unoccupied hours in spaces that have health and safety mandated minimum ventilation requirements during unoccupied hours in the proposed design.",
            ruleset_section_title="HVAC - General",
            standard_section="Section G3.1-4 Schedules exception #2 for the proposed building and Section G3.1.2.4 Appendix G Section Reference: None",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0",
            list_path="$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
        )

    def create_data(self, context, data):
        rmd_p = context.PROPOSED
        applicable_hvac_systems_list_p = (
            get_hvac_systems_serving_zone_health_safety_vent_reqs(rmd_p)
        )

        return {"applicable_hvac_systems_list_p": applicable_hvac_systems_list_p}

    class HVACRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule09g49.HVACRule, self).__init__(
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
            applicable_hvac_systems_list_p = data["applicable_hvac_systems_list_p"]

            return hvac_id_p in applicable_hvac_systems_list_p

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
            )

        def get_fail_msg(self, context, calc_vals=None, data=None):
            hvac_p = context.PROPOSED
            hvac_id_p = hvac_p["id"]

            return f"{hvac_id_p} SERVES ZONE(S) THAT APPEAR LIKELY TO HAVE HEALTH AND SAFETY MANDATED MINIMUM VENTILATION REQUIREMENTS DURING UNOCCUPIED HOURS AND THEREFORE (IF THE HVAC SYSTEM SUPPLIES OA CFM) MAY WARRANT CONTINUOUS OPERATION DURING UNOCCUPIED HOURS PER SECTION G3.1-4 SCHEDULES EXCEPTION #2 FOR THE PROPOSED BUILDING AND PER SECTION G3.1.2.4."
