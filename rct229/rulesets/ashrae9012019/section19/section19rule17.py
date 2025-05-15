from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
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
from rct229.rulesets.ashrae9012019.ruleset_functions.get_fan_object_electric_power import (
    get_fan_object_electric_power,
)
from rct229.schema.config import ureg
from rct229.utils.assertions import getattr_
from rct229.utils.compare_standard_val import std_le
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import ZERO, CalcQ

APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_1,
    HVAC_SYS.SYS_2,
]

FAN_POWER_AIRFLOW_LIMIT = 0.3 * ureg("W/cfm")


class PRM9012019Rule84b07(RuleDefinitionListIndexedBase):
    """Rule 17 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(PRM9012019Rule84b07, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012019Rule84b07.HVACRule(),
            index_rmd=BASELINE_0,
            id="19-17",
            description="For baseline system 1 and 2, the total fan electrical power (Pfan) for supply, return, exhaust, and relief shall be = CFMs × 0.3, where, CFMs = the baseline system maximum design supply fan airflow rate, cfm.",
            ruleset_section_title="HVAC - General",
            standard_section="Section G3.1.2.9",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0",
            list_path="$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
        )

    def is_applicable(self, context, data=None):
        rmd_b = context.BASELINE_0
        baseline_system_types_dict = get_baseline_system_types(rmd_b)

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
        rmd_b = context.BASELINE_0
        baseline_system_types_dict = get_baseline_system_types(rmd_b)

        return {
            "baseline_system_types_dict": baseline_system_types_dict,
            "dict_of_zones_and_terminal_units_served_by_hvac_sys": (
                get_dict_of_zones_and_terminal_units_served_by_hvac_sys(rmd_b)
            ),
            "zone_exhaust_fan_power_dict_b": {
                zone["id"]: sum(
                    [
                        get_fan_object_electric_power(exhaust_fan)
                        for exhaust_fan in find_all("$.zonal_exhaust_fan", zone)
                    ]
                )
                for zone in find_all(
                    "$.buildings[*].building_segments[*].zones[*]", rmd_b
                )
            },
        }

    class HVACRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule84b07.HVACRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={
                    "$": ["fan_system"],
                },
                precision={
                    "fan_power_airflow": {
                        "precision": 0.1,
                        "unit": "W/cfm",
                    },
                },
            )

        def is_applicable(self, context, data=None):
            hvac_b = context.BASELINE_0
            hvac_id_b = hvac_b["id"]
            baseline_system_types_dict = data["baseline_system_types_dict"]

            return any(
                hvac_id_b in baseline_system_types_dict[system_type]
                for system_type in APPLICABLE_SYS_TYPES
            )

        def get_calc_vals(self, context, data=None):
            hvac_b = context.BASELINE_0
            hvac_id_b = hvac_b["id"]
            dict_of_zones_and_terminal_units_served_by_hvac_sys = data[
                "dict_of_zones_and_terminal_units_served_by_hvac_sys"
            ]
            zone_exhaust_fan_power_dict_b = data["zone_exhaust_fan_power_dict_b"]
            fan_sys_b = hvac_b["fan_system"]

            supply_airflow_b = ZERO.FLOW
            total_fan_power = ZERO.POWER
            for fan_type_b in ("supply", "return", "relief", "exhaust"):
                for fan_b in find_all(f"$.{fan_type_b}_fans[*]", fan_sys_b):
                    if fan_type_b == "supply":
                        supply_airflow_b += getattr_(
                            fan_b, "Supply fans", "design_airflow"
                        )
                    total_fan_power += get_fan_object_electric_power(fan_b)

            for zone_id_b in dict_of_zones_and_terminal_units_served_by_hvac_sys[
                hvac_id_b
            ]["zone_list"]:
                total_fan_power += zone_exhaust_fan_power_dict_b[zone_id_b]

            fan_power_airflow = (
                total_fan_power / supply_airflow_b
                if supply_airflow_b != ZERO.FLOW
                else ZERO.POWER_PER_FLOW
            )

            return {
                "fan_power_airflow": CalcQ("power_per_air_flow_rate", fan_power_airflow)
            }

        def rule_check(self, context, calc_vals=None, data=None):
            fan_power_airflow = calc_vals["fan_power_airflow"]

            return (
                fan_power_airflow < FAN_POWER_AIRFLOW_LIMIT
                or self.precision_comparison["fan_power_airflow"](
                    fan_power_airflow,
                    FAN_POWER_AIRFLOW_LIMIT,
                )
            )

        def is_tolerance_fail(self, context, calc_vals=None, data=None):
            fan_power_airflow = calc_vals["fan_power_airflow"]

            return std_le(val=fan_power_airflow, std_val=FAN_POWER_AIRFLOW_LIMIT)
