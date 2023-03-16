from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
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
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.std_comparisons import std_equal
from rct229.schema.config import ureg

APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_1,
    HVAC_SYS.SYS_2,
]

FAN_POWER_LIMIT = 0.3 * ureg("")
AHJ_RA_compare = False


class Section19Rule18(RuleDefinitionListIndexedBase):
    """Rule 18 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(Section19Rule18, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section19Rule18.HVACRule(),
            index_rmr="baseline",
            id="19-18",
            description="or baseline system 1 and 2, the total fan electrical power (Pfan) for supply, return, exhaust, and relief shall be = CFMs × 0.3, where, CFMs = the baseline system maximum design supply fan airflow rate, cfm.",
            ruleset_section_title="HVAC - General",
            standard_section=" Section G3.1.2.9",
            is_primary_rule=True,
            rmr_context="ruleset_model_instances/0",
            list_path="$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
        )

    def is_applicable(self, context, data=None):
        rmi_b = context.baseline
        baseline_system_types_dict = get_baseline_system_types(rmi_b)

        return any(
            [
                baseline_system_type_compare(system_type, applicable_sys_type, False)
                for system_type in baseline_system_types_dict.keys()
                for applicable_sys_type in APPLICABLE_SYS_TYPES
            ]
        )

    def create_data(self, context, data):
        rmi_b = context.baseline
        dict_of_zones_and_terminal_units_served_by_hvac_sys = (
            get_dict_of_zones_and_terminal_units_served_by_hvac_sys(rmi_b)
        )

        return {
            "dict_of_zones_and_terminal_units_served_by_hvac_sys": dict_of_zones_and_terminal_units_served_by_hvac_sys
        }

    class HVACRule(RuleDefinitionBase):
        def __init__(self):
            super(Section19Rule18.HVACRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
            )

        def get_calc_vals(self, context, data=None):
            hvac_b = context.baseline
            hvac_id_b = hvac_b["id"]
            dict_of_zones_and_terminal_units_served_by_hvac_sys = data[
                "dict_of_zones_and_terminal_units_served_by_hvac_sys"
            ]
            zone_list = dict_of_zones_and_terminal_units_served_by_hvac_sys[hvac_id_b][
                "zone_list"
            ]

            fan_system_b = hvac_b["fan_system"]

            supply_cfm_b = 0.0 * ureg("cfm")
            return_cfm_b = 0.0 * ureg("cfm")
            relief_cfm_b = 0.0 * ureg("cfm")
            exhaust_cfm_b = 0.0 * ureg("cfm")
            total_fan_power = 0.0 * ureg("W")
            for supply_fan_b in find_all("$.supply_fans[*]", fan_system_b):
                supply_cfm_b += supply_fan_b["design_airflow"]
                # TODO add `get_fan_object_electric_power`
                total_fan_power += 1

            for return_fan_b in find_all("$.return_fans[*]", fan_system_b):
                return_cfm_b += return_fan_b["design_airflow"]
                # TODO add `get_fan_object_electric_power`
                total_fan_power += 1

            for relief_fan_b in find_all("$.relief_fans[*]", fan_system_b):
                relief_cfm_b += relief_fan_b["design_airflow"]
                # TODO add `get_fan_object_electric_power`
                total_fan_power += 1

            for relief_fan_b in find_all("$.relief_fans[*]", fan_system_b):
                relief_cfm_b += relief_fan_b["design_airflow"]
                # TODO add `get_fan_object_electric_power`
                total_fan_power += 1

            for exhaust_fan_b in find_all("$.exhaust_fans[*]", fan_system_b):
                exhaust_cfm_b += exhaust_fan_b["design_airflow"]
                # TODO add `get_fan_object_electric_power`
                total_fan_power += 1

            fan_elec_power = 0.0
            for zone_b in zone_list:
                if zone_b["zonal_exhaust_fan"]:
                    total_fan_power += fan_elec_power

            fan_power_W_CFM = total_fan_power / supply_cfm_b

            return {"fan_power_W_CFM": fan_power_W_CFM}

        def rule_check(self, context, calc_vals=None, data=None):
            fan_power_W_CFM = calc_vals["fan_power_W_CFM"]
            return std_equal(FAN_POWER_LIMIT, fan_power_W_CFM) or (
                AHJ_RA_compare and fan_power_W_CFM <= FAN_POWER_LIMIT
            )
