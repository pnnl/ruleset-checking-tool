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
from rct229.rulesets.ashrae9012019.ruleset_functions.get_fan_system_object_supply_return_exhaust_relief_total_power_flow import (
    get_fan_system_object_supply_return_exhaust_relief_total_power_flow,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_zone_supply_return_exhaust_relief_terminal_fan_power_dict import (
    get_zone_supply_return_exhaust_relief_terminal_fan_power_dict,
)
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all, find_one
from rct229.utils.pint_utils import ZERO, CalcQ
from rct229.utils.std_comparisons import std_equal

APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_1,
    HVAC_SYS.SYS_2,
    HVAC_SYS.SYS_3,
    HVAC_SYS.SYS_4,
    HVAC_SYS.SYS_5,
    HVAC_SYS.SYS_6,
    HVAC_SYS.SYS_7,
    HVAC_SYS.SYS_8,
    HVAC_SYS.SYS_11_1,
    HVAC_SYS.SYS_12,
    HVAC_SYS.SYS_13,
]


class PRM9012019Rule60f12(RuleDefinitionListIndexedBase):
    """Rule 14 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(PRM9012019Rule60f12, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=PRM9012019Rule60f12.HVACRule(),
            index_rmd=BASELINE_0,
            id="19-14",
            description="For baseline system types 1-8 and 11-13, if return or relief fans are specified in the proposed design, the baseline building design shall also be modeled with fans serving the same functions and sized for the baseline system supply fan air quantity less the minimum outdoor air, or 90% of the supply fan air quantity, whichever is larger.",
            ruleset_section_title="HVAC - General",
            standard_section="Section G3.1.2.8.1 Excluding Exceptions 1 and 2",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0",
            list_path="$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
        )

    def is_applicable(self, context, data=None):
        rmd_b = context.BASELINE_0
        baseline_system_types_dict_b = get_baseline_system_types(rmd_b)

        return any(
            [
                baseline_system_types_dict_b[system_type]
                and baseline_system_type_compare(
                    system_type, applicable_sys_type, False
                )
                for system_type in baseline_system_types_dict_b
                for applicable_sys_type in APPLICABLE_SYS_TYPES
            ]
        )

    def create_data(self, context, data):
        rmd_b = context.BASELINE_0
        rmd_p = context.PROPOSED

        zone_supply_return_exhaust_relief_terminal_fan_power_dict = (
            get_zone_supply_return_exhaust_relief_terminal_fan_power_dict(rmd_p)
        )

        hvac_info_b = {}
        for hvac_b in find_all(
            "$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
            rmd_b,
        ):
            hvac_id_b = hvac_b["id"]
            hvac_info_b[hvac_id_b] = {}

            hvac_info_b[hvac_id_b][
                "fan_system_info_b"
            ] = get_fan_system_object_supply_return_exhaust_relief_total_power_flow(
                getattr_(hvac_b, "HVAC", "fan_system")
            )

        zone_fan_power_dict_b = {}
        for zone_id_b in find_all(
            "$.buildings[*].building_segments[*].zones[*].id", rmd_b
        ):
            modeled_fan_power_list_p = zone_supply_return_exhaust_relief_terminal_fan_power_dict[
                find_one(
                    f'$.buildings[*].building_segments[*].zones[*][?(@.id = "{zone_id_b}")]',
                    rmd_p,
                )["id"]
            ]
            zone_fan_power_dict_b[zone_id_b] = modeled_fan_power_list_p

        return {
            "dict_of_zones_and_terminal_units_served_by_hvac_sys_b": get_dict_of_zones_and_terminal_units_served_by_hvac_sys(
                rmd_b
            ),
            "baseline_system_types_dict_b": get_baseline_system_types(rmd_b),
            "hvac_info_b": hvac_info_b,
            "zone_fan_power_dict_b": zone_fan_power_dict_b,
        }

    class HVACRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule60f12.HVACRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={
                    "$": ["fan_system"],
                },
                precision={
                    "modeled_cfm": {
                        "precision": 1,
                        "unit": "cfm",
                    },
                },
            )

        def is_applicable(self, context, data=None):
            hvac_b = context.BASELINE_0
            hvac_id_b = hvac_b["id"]
            baseline_system_types_dict_b = data["baseline_system_types_dict_b"]

            return any(
                hvac_id_b in baseline_system_types_dict_b[system_type]
                for system_type in baseline_system_types_dict_b
            )

        def get_calc_vals(self, context, data=None):
            hvac_b = context.BASELINE_0
            hvac_id_b = hvac_b["id"]

            hvac_info_b = data["hvac_info_b"][hvac_id_b]

            fan_system_info_b = hvac_info_b["fan_system_info_b"]
            more_than_one_supply_and_return_fan = (
                fan_system_info_b["supply_fans_qty"] > 1
                or fan_system_info_b["return_fans_qty"] > 1
            )

            dict_of_zones_and_terminal_units_served_by_hvac_sys_b = data[
                "dict_of_zones_and_terminal_units_served_by_hvac_sys_b"
            ]
            zone_fan_power_dict_b = data["zone_fan_power_dict_b"]
            zone_id_list = dict_of_zones_and_terminal_units_served_by_hvac_sys_b[
                hvac_id_b
            ]["zone_list"]

            is_modeled_with_return_fan_p = any(
                [
                    zone_fan_power_dict_b[zone_id_p]["return_fans_power"] > ZERO.POWER
                    for zone_id_p in zone_id_list
                ]
            )
            is_modeled_with_relief_fan_p = any(
                [
                    zone_fan_power_dict_b[zone_id_p]["relief_fans_power"] > ZERO.POWER
                    for zone_id_p in zone_id_list
                ]
            )

            fan_sys_b = hvac_b["fan_system"]
            fan_sys_cfm = (
                get_fan_system_object_supply_return_exhaust_relief_total_power_flow(
                    fan_sys_b
                )
            )

            hvac_sys_total_supply_fan_cfm_b = fan_sys_cfm["supply_fans_airflow"]
            supply_cfm_90_percent = 0.9 * hvac_sys_total_supply_fan_cfm_b
            supply_minus_OA_flow = hvac_sys_total_supply_fan_cfm_b - getattr_(
                fan_sys_b, "Fan System", "minimum_outdoor_airflow"
            )

            return_fans_airflow = fan_sys_cfm["return_fans_airflow"]
            relief_fans_airflow = fan_sys_cfm["relief_fans_airflow"]
            modeled_cfm = (
                return_fans_airflow + relief_fans_airflow
                if is_modeled_with_return_fan_p or is_modeled_with_relief_fan_p
                else ZERO.FLOW
            )

            baseline_modeled_return_as_expected = (
                is_modeled_with_return_fan_p and return_fans_airflow > ZERO.FLOW
            ) or (not is_modeled_with_return_fan_p and return_fans_airflow == ZERO.FLOW)

            baseline_modeled_relief_as_expected = (
                is_modeled_with_relief_fan_p and relief_fans_airflow > ZERO.FLOW
            ) or (not is_modeled_with_relief_fan_p and relief_fans_airflow == ZERO.FLOW)

            return {
                "more_than_one_supply_and_return_fan": more_than_one_supply_and_return_fan,
                "is_modeled_with_return_fan_p": is_modeled_with_return_fan_p,
                "is_modeled_with_relief_fan_p": is_modeled_with_relief_fan_p,
                "return_fans_airflow": CalcQ("air_flow_rate", return_fans_airflow),
                "relief_fans_airflow": CalcQ("air_flow_rate", relief_fans_airflow),
                "baseline_modeled_return_as_expected": baseline_modeled_return_as_expected,
                "baseline_modeled_relief_as_expected": baseline_modeled_relief_as_expected,
                "modeled_cfm": CalcQ("air_flow_rate", modeled_cfm),
                "supply_minus_OA_flow": CalcQ("air_flow_rate", supply_minus_OA_flow),
                "supply_cfm_90_percent": CalcQ("air_flow_rate", supply_cfm_90_percent),
            }

        def manual_check_required(self, context, calc_vals=None, data=None):
            return calc_vals["more_than_one_supply_and_return_fan"]

        def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
            hvac_b = context.BASELINE_0
            hvac_id_b = hvac_b["id"]

            return f"{hvac_id_b} has more than one supply or return fan associated with the HVAC system in the baseline and therefore this check could not be conducted for this HVAC system. Conduct manual check for compliance with G3.1.2.8.1."

        def rule_check(self, context, calc_vals=None, data=None):
            return_fans_airflow = calc_vals["return_fans_airflow"]
            relief_fans_airflow = calc_vals["relief_fans_airflow"]
            baseline_modeled_return_as_expected = calc_vals[
                "baseline_modeled_return_as_expected"
            ]
            baseline_modeled_relief_as_expected = calc_vals[
                "baseline_modeled_relief_as_expected"
            ]
            modeled_cfm = calc_vals["modeled_cfm"]
            supply_minus_OA_flow = calc_vals["supply_minus_OA_flow"]
            supply_cfm_90_percent = calc_vals["supply_cfm_90_percent"]
            is_modeled_with_return_fan_in_p = calc_vals["is_modeled_with_return_fan_p"]
            is_modeled_with_relief_fan_p = calc_vals["is_modeled_with_relief_fan_p"]

            return (
                baseline_modeled_return_as_expected
                and baseline_modeled_relief_as_expected
                and (is_modeled_with_return_fan_in_p or is_modeled_with_relief_fan_p)
                and self.precision_comparison["modeled_cfm"](
                    modeled_cfm,
                    max(supply_minus_OA_flow, supply_cfm_90_percent),
                )
            ) or (
                not is_modeled_with_return_fan_in_p
                and not is_modeled_with_relief_fan_p
                and std_equal(ZERO.FLOW, return_fans_airflow)
                and std_equal(ZERO.FLOW, relief_fans_airflow)
            )

        def is_tolerance_fail(self, context, calc_vals=None, data=None):
            return_fans_airflow = calc_vals["return_fans_airflow"]
            relief_fans_airflow = calc_vals["relief_fans_airflow"]
            baseline_modeled_return_as_expected = calc_vals[
                "baseline_modeled_return_as_expected"
            ]
            baseline_modeled_relief_as_expected = calc_vals[
                "baseline_modeled_relief_as_expected"
            ]
            modeled_cfm = calc_vals["modeled_cfm"]
            supply_minus_OA_flow = calc_vals["supply_minus_OA_flow"]
            supply_cfm_90_percent = calc_vals["supply_cfm_90_percent"]
            is_modeled_with_return_fan_in_p = calc_vals["is_modeled_with_return_fan_p"]
            is_modeled_with_relief_fan_p = calc_vals["is_modeled_with_relief_fan_p"]

            return (
                baseline_modeled_return_as_expected
                and baseline_modeled_relief_as_expected
                and (is_modeled_with_return_fan_in_p or is_modeled_with_relief_fan_p)
                and std_equal(
                    modeled_cfm, max(supply_minus_OA_flow, supply_cfm_90_percent)
                )
            ) or (
                not is_modeled_with_return_fan_in_p
                and not is_modeled_with_relief_fan_p
                and std_equal(ZERO.FLOW, return_fans_airflow)
                and std_equal(ZERO.FLOW, relief_fans_airflow)
            )
