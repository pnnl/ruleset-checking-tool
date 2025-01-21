from pydash import reject
from rct229.rule_engine.partial_rule_definition import PartialRuleDefinition
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import PROPOSED
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_system_type_compare import (
    baseline_system_type_compare,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_baseline_system_types import (
    get_baseline_system_types,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_dict_of_zones_and_terminal_units_served_by_hvac_sys import (
    get_dict_of_zones_and_terminal_units_served_by_hvac_sys,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.utility_functions import find_exactly_one_zone

APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_3,
    HVAC_SYS.SYS_4,
    HVAC_SYS.SYS_5,
    HVAC_SYS.SYS_6,
    HVAC_SYS.SYS_7,
    HVAC_SYS.SYS_8,
    HVAC_SYS.SYS_11_1,
    HVAC_SYS.SYS_11_2,
    HVAC_SYS.SYS_12,
    HVAC_SYS.SYS_13,
]

DehumidificationOptions = SchemaEnums.schema_enums["DehumidificationOptions"]


class PRM9012019Rule71f87(RuleDefinitionListIndexedBase):
    """Rule 15 of ASHRAE 90.1-2019 Appendix G Section 23 (Air-side)"""

    def __init__(self):
        super(PRM9012019Rule71f87, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=PRM9012019Rule71f87.HVACRule(),
            index_rmd=PROPOSED,
            id="23-15",
            description="Dehumidification reheat shall be the same as the system heating type.",
            ruleset_section_title="HVAC - Airside",
            standard_section="G3.1.3.18 Dehumidification (Systems 3 through 8 and 11, 12, and 13)",
            is_primary_rule=False,
            rmd_context="ruleset_model_descriptions/0",
            list_path="$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
        )

    def is_applicable(self, context, data=None):
        rmd_b = context.BASELINE_0
        baseline_system_types_dict = get_baseline_system_types(rmd_b)
        # if baseline does not have system 3-8 or 11, 12, 13, then this rule is not applicable
        return any(
            [
                baseline_system_types_dict[system_type]
                and baseline_system_type_compare(
                    system_type, applicable_sys_type, False
                )
                for system_type in baseline_system_types_dict
                for applicable_sys_type in APPLICABLE_SYS_TYPES
            ]
        )

    def create_data(self, context, data):
        rmd_p = context.PROPOSED
        # Create a new dict that maps hvac_id to zones with humidity setpoints
        hvac_systems_and_zones_p = (
            get_dict_of_zones_and_terminal_units_served_by_hvac_sys(rmd_p)
        )
        hvac_system_zone_with_humidistatic_dict = {
            key: reject(
                hvac_systems_and_zones_p[key]["zone_list"],
                lambda zone_id: find_exactly_one_zone(rmd_p, zone_id).get(
                    "maximum_humidity_setpoint_schedule"
                )
                is None,
            )
            for key in hvac_systems_and_zones_p
        }

        return {
            "hvac_system_zone_with_humidistatic_dict": hvac_system_zone_with_humidistatic_dict,
        }

    class HVACRule(PartialRuleDefinition):
        def __init__(self):
            super(PRM9012019Rule71f87.HVACRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=False, PROPOSED=True
                ),
                required_fields={"$": ["cooling_system"]},
            )

        def get_calc_vals(self, context, data=None):
            hvac_p = context.PROPOSED
            hvac_systems_and_zones_p = data["hvac_system_zone_with_humidistatic_dict"]
            dehumidification_type_p = hvac_p["cooling_system"].get(
                "dehumidification_type"
            )
            zones_with_humidity_schedules_list_p = hvac_systems_and_zones_p[
                hvac_p["id"]
            ]

            return {
                "dehumidification_type": dehumidification_type_p,
                "zones_with_humidity_schedules_list": zones_with_humidity_schedules_list_p,
            }

        def applicability_check(self, context, calc_vals, data):
            dehumidification_type_p = calc_vals["dehumidification_type"]
            zones_with_humidity_schedules_list_p = calc_vals[
                "zones_with_humidity_schedules_list"
            ]
            return (
                dehumidification_type_p
                and dehumidification_type_p != DehumidificationOptions.NONE
                and len(zones_with_humidity_schedules_list_p) > 0
            )

        def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
            zones_with_humidity_schedules_list_p = calc_vals[
                "zones_with_humidity_schedules_list"
            ]
            return f"The following zones have humidity schedules: {zones_with_humidity_schedules_list_p}"
