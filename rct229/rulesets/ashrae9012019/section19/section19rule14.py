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
from rct229.rulesets.ashrae9012019.ruleset_functions.get_fan_system_object_supply_return_exhaust_relief_total_power_flow import (
    get_fan_system_object_supply_return_exhaust_relief_total_power_flow,
)
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all, find_one
from rct229.utils.pint_utils import ZERO
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
    HVAC_SYS.SYS_11,
    HVAC_SYS.SYS_12,
    HVAC_SYS.SYS_13,
]


def get_zone_supply_return_exhaust_relief_terminal_fan_power_dict():
    return True


class Section19Rule14(RuleDefinitionListIndexedBase):
    """Rule 14 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(Section19Rule14, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, True),
            each_rule=Section19Rule14.HVACRule(),
            index_rmr="baseline",
            id="19-14",
            description="For baseline system types 1-8 and 11-13, if return or relief fans are specified in the proposed design, the baseline building design shall also be modeled with fans serving the same functions and sized for the baseline system supply fan air quantity less the minimum outdoor air, or 90% of the supply fan air quantity, whichever is larger.",
            ruleset_section_title="HVAC - General",
            standard_section="3.1.2.8.1 Excluding Exceptions 1 and 2",
            is_primary_rule=True,
            rmr_context="ruleset_model_instances/0",
            list_path="$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
        )

    def create_data(self, context, data):
        rmi_b = context.baseline
        rmi_p = context.proposed

        dict_of_zones_and_terminal_units_served_by_hvac_sys_b = (
            get_dict_of_zones_and_terminal_units_served_by_hvac_sys(rmi_b)
        )
        zone_supply_return_exhaust_relief_terminal_fan_power_dict = (
            get_zone_supply_return_exhaust_relief_terminal_fan_power_dict(rmi_p)
        )

        for hvac_b in find_all(
            "$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
            rmi_b,
        ):
            fan_system_info_b = (
                get_fan_system_object_supply_return_exhaust_relief_total_power_flow(
                    getattr_(hvac_b, "HVAC", "fan_system")
                )
            )
            if (
                fan_system_info_b["supply_fans_qty"] == 1
                and fan_system_info_b["return_fans_qty"] == 1
            ):
                more_than_one_supply_or_return_fan = False
                hvac_id_b = hvac_b["id"]
                for zone_b in dict_of_zones_and_terminal_units_served_by_hvac_sys_b[
                    hvac_id_b
                ]["zone_list"]:
                    zone_p = find_one(
                        f'$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[?(@.id == "{hvac_id_b}")]',
                        rmi_p,
                    )

                    modeled_fan_power_list_p = list(
                        zone_supply_return_exhaust_relief_terminal_fan_power_dict[
                            zone_p["id"]
                        ]
                    )

                    if (
                        modeled_fan_power_list_p["zone_total_return_fan_power"]
                        > ZERO.POWER
                    ):
                        is_modeled_with_return_fan_in_proposed = True
                    if (
                        modeled_fan_power_list_p["zone_total_exhaust_fan_power"]
                        > ZERO.POWER
                    ):
                        is_modeled_with_relief_fan_in_proposed = False

        return {
            "baseline_system_types_dict": get_baseline_system_types(rmi_b),
            "more_than_one_supply_or_return_fan": more_than_one_supply_or_return_fan,
            "is_modeled_with_return_fan_in_proposed": is_modeled_with_return_fan_in_proposed,
            "is_modeled_with_relief_fan_in_proposed": is_modeled_with_relief_fan_in_proposed,
        }

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

    class HVACRule(RuleDefinitionBase):
        def __init__(self):
            super(Section19Rule14.HVACRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, True),
                required_fields={
                    "$": ["fan_system"],
                },
            )

        def is_applicable(self, context, data=None):
            hvac_b = context.baseline
            hvac_id_b = hvac_b["id"]
            baseline_system_types_dict = data["baseline_system_types_dict"]

            return any(
                hvac_id_b in baseline_system_types_dict[system_type]
                for system_type in baseline_system_types_dict.keys()
            )

        def get_calc_vals(self, context, data=None):
            hvac_b = context.baseline
            hvac_id_b = hvac_b["id"]

            is_modeled_with_return_fan_p = data[
                "is_modeled_with_return_fan_in_proposed"
            ]
            is_modeled_with_relief_fan_p = data[
                "is_modeled_with_relief_fan_in_proposed"
            ]

            fan_sys_b = hvac_b["fan_system"]

            fan_sys_cfm = (
                get_fan_system_object_supply_return_exhaust_relief_total_power_flow(
                    fan_sys_b
                )
            )

            hvac_sys_total_supply_fan_cfm_b = fan_sys_cfm["supply_fans_airflow"]

            supply_cfm_90_percent = 0.9 * hvac_sys_total_supply_fan_cfm_b

            supply_minus_OA_cfm = hvac_sys_total_supply_fan_cfm_b - getattr_(
                fan_sys_b, "Fan System", "minimum_outdoor_airflow"
            )

            return_fans_airflow = fan_sys_cfm["return_fans_airflow"]
            relief_fans_airflow = fan_sys_cfm["relief_fans_airflow"]
            if is_modeled_with_return_fan_p and is_modeled_with_relief_fan_p:
                modeled_cfm = return_fans_airflow + relief_fans_airflow
            else:
                modeled_cfm = ZERO.FLOW

            baseline_modeled_return_as_expected = False
            baseline_modeled_relief_as_expected = False
            if (is_modeled_with_return_fan_p and return_fans_airflow > ZERO.FLOW) and (
                not is_modeled_with_relief_fan_p and return_fans_airflow == ZERO.FLOW
            ):
                baseline_modeled_return_as_expected = True
            if (
                baseline_modeled_relief_as_expected and relief_fans_airflow > ZERO.FLOW
            ) and (
                not baseline_modeled_relief_as_expected
                and relief_fans_airflow == ZERO.FLOW
            ):
                baseline_modeled_return_as_expected = True

            return {
                "return_fans_airflow": return_fans_airflow,
                "relief_fans_airflow": relief_fans_airflow,
                "baseline_modeled_return_as_expected": baseline_modeled_return_as_expected,
                "baseline_modeled_return_as_expected": baseline_modeled_return_as_expected,
                "modeled_cfm": modeled_cfm,
                "supply_minus_OA_cfm": supply_minus_OA_cfm,
                "supply_cfm_90_percent": supply_cfm_90_percent,
            }

        def manual_check_required(self, context, calc_vals=None, data=None):
            return calc_vals["more_than_one_supply_or_return_fan"]

        def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
            hvac_b = context.baseline
            hvac_id_b = hvac_b["id"]
            return f"{hvac_id_b} has more than one supply or return fan associated with the HVAC system in the baseline and therefore this check could not be conducted for this HVAC sytem. Conduct manual check for compliance with G3.1.2.8.1."

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
            supply_minus_OA_cfm = calc_vals["supply_minus_OA_cfm"]
            supply_cfm_90_percent = calc_vals["supply_cfm_90_percent"]

            more_than_one_supply_or_return_fan = data[
                "more_than_one_supply_or_return_fan"
            ]
            is_modeled_with_return_fan_in_proposed = data[
                "is_modeled_with_return_fan_in_proposed"
            ]
            is_modeled_with_relief_fan_in_proposed = data[
                "is_modeled_with_relief_fan_in_proposed "
            ]

            return (
                not more_than_one_supply_or_return_fan
                and baseline_modeled_return_as_expected
                and baseline_modeled_relief_as_expected
                and (
                    is_modeled_with_return_fan_in_proposed
                    or is_modeled_with_relief_fan_in_proposed
                )
                and std_equal(
                    modeled_cfm, max(supply_minus_OA_cfm, supply_cfm_90_percent)
                )
            ) and (
                not is_modeled_with_return_fan_in_proposed
                and not is_modeled_with_relief_fan_in_proposed
                and std_equal(ZERO.FLOW, return_fans_airflow)
                and std_equal(ZERO.FLOW, relief_fans_airflow)
            )
