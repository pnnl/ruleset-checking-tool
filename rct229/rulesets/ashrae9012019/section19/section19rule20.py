from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.get_dict_of_zones_and_terminal_units_served_by_hvac_sys import (
    get_dict_of_zones_and_terminal_units_served_by_hvac_sys,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_fan_system_object_supply_return_exhaust_relief_total_power_flow import (
    get_fan_system_object_supply_return_exhaust_relief_total_power_flow,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_zone_supply_return_exhaust_relief_terminal_fan_power_dict import (
    get_zone_supply_return_exhaust_relief_terminal_fan_power_dict,
)
from rct229.utils.pint_utils import ZERO, CalcQ
from rct229.utils.std_comparisons import std_equal


class PRM9012019Rule60d49(RuleDefinitionListIndexedBase):
    """Rule 20 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(PRM9012019Rule60d49, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=PRM9012019Rule60d49.HVACRule(),
            index_rmd=BASELINE_0,
            id="19-20",
            description="The calculated system fan power shall be distributed to supply, return, exhaust, and relief fans in the same proportion as the proposed design.",
            ruleset_section_title="HVAC - General",
            standard_section="Section G3.1.2.9",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0",
            list_path="$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
        )

    def create_data(self, context, data):
        rmd_b = context.BASELINE_0
        rmd_p = context.PROPOSED

        return {
            "zone_supply_return_exhaust_relief_terminal_fan_power_dict_p": get_zone_supply_return_exhaust_relief_terminal_fan_power_dict(
                rmd_p
            ),
            "dict_of_zones_and_terminal_units_served_by_hvac_sys_b": get_dict_of_zones_and_terminal_units_served_by_hvac_sys(
                rmd_b
            ),
        }

    class HVACRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule60d49.HVACRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={
                    "$": ["fan_system"],
                },
                precision={
                    "hvac_sys_total_supply_fan_power_b": {
                        "precision": 1,
                        "unit": "W",
                    },
                    "hvac_sys_total_return_fan_power_b": {
                        "precision": 1,
                        "unit": "W",
                    },
                    "hvac_sys_total_exhaust_fan_power_b": {
                        "precision": 1,
                        "unit": "W",
                    },
                    "hvac_sys_total_relief_fan_power_b": {
                        "precision": 1,
                        "unit": "W",
                    },
                },
            )

        def get_calc_vals(self, context, data=None):
            hvac_b = context.BASELINE_0
            hvac_id_b = hvac_b["id"]
            zone_supply_return_exhaust_relief_terminal_fan_power_dict_p = data[
                "zone_supply_return_exhaust_relief_terminal_fan_power_dict_p"
            ]
            list_zones_served_b = data[
                "dict_of_zones_and_terminal_units_served_by_hvac_sys_b"
            ][hvac_id_b]["zone_list"]

            fan_sys_b = hvac_b["fan_system"]

            fan_sys_power_flow_info_dict_b = (
                get_fan_system_object_supply_return_exhaust_relief_total_power_flow(
                    fan_sys_b
                )
            )

            hvac_sys_total_supply_fan_power_b = fan_sys_power_flow_info_dict_b[
                "supply_fans_power"
            ]
            hvac_sys_total_return_fan_power_b = fan_sys_power_flow_info_dict_b[
                "return_fans_power"
            ]
            hvac_sys_total_exhaust_fan_power_b = fan_sys_power_flow_info_dict_b[
                "exhaust_fans_power"
            ]
            hvac_sys_total_relief_fan_power_b = fan_sys_power_flow_info_dict_b[
                "relief_fans_power"
            ]

            total_modeled_fan_power_b = (
                hvac_sys_total_supply_fan_power_b
                + hvac_sys_total_return_fan_power_b
                + hvac_sys_total_exhaust_fan_power_b
                + hvac_sys_total_relief_fan_power_b
            )

            proposed_total_supply_fan_power = ZERO.POWER
            proposed_total_return_fan_power = ZERO.POWER
            proposed_total_exhaust_fan_power = ZERO.POWER
            proposed_total_relief_fan_power = ZERO.POWER
            for zone_id_b in list_zones_served_b:
                proposed_total_supply_fan_power += (
                    zone_supply_return_exhaust_relief_terminal_fan_power_dict_p[
                        zone_id_b
                    ]["supply_fans_power"]
                )
                proposed_total_return_fan_power += (
                    zone_supply_return_exhaust_relief_terminal_fan_power_dict_p[
                        zone_id_b
                    ]["return_fans_power"]
                )
                proposed_total_exhaust_fan_power += (
                    zone_supply_return_exhaust_relief_terminal_fan_power_dict_p[
                        zone_id_b
                    ]["exhaust_fans_power"]
                )
                proposed_total_relief_fan_power += (
                    zone_supply_return_exhaust_relief_terminal_fan_power_dict_p[
                        zone_id_b
                    ]["relief_fans_power"]
                )

            total_modeled_fan_power_p = (
                proposed_total_supply_fan_power
                + proposed_total_return_fan_power
                + proposed_total_exhaust_fan_power
                + proposed_total_relief_fan_power
            )

            fraction_of_total_supply_p = 0.0
            fraction_of_total_return_p = 0.0
            fraction_of_total_exhaust_p = 0.0
            fraction_of_total_relief_p = 0.0

            if total_modeled_fan_power_p > ZERO.POWER:
                fraction_of_total_supply_p = (
                    proposed_total_supply_fan_power / total_modeled_fan_power_p
                )
                fraction_of_total_return_p = (
                    proposed_total_return_fan_power / total_modeled_fan_power_p
                )
                fraction_of_total_exhaust_p = (
                    proposed_total_exhaust_fan_power / total_modeled_fan_power_p
                )
                fraction_of_total_relief_p = (
                    proposed_total_relief_fan_power / total_modeled_fan_power_p
                )
            return {
                "hvac_sys_total_supply_fan_power_b": CalcQ(
                    "electric_power", hvac_sys_total_supply_fan_power_b
                ),
                "hvac_sys_total_return_fan_power_b": CalcQ(
                    "electric_power", hvac_sys_total_return_fan_power_b
                ),
                "hvac_sys_total_exhaust_fan_power_b": CalcQ(
                    "electric_power", hvac_sys_total_exhaust_fan_power_b
                ),
                "hvac_sys_total_relief_fan_power_b": CalcQ(
                    "electric_power", hvac_sys_total_relief_fan_power_b
                ),
                "expected_baseline_fan_power_supply": CalcQ(
                    "electric_power",
                    total_modeled_fan_power_b * fraction_of_total_supply_p,
                ),
                "expected_baseline_fan_power_return": CalcQ(
                    "electric_power",
                    total_modeled_fan_power_b * fraction_of_total_return_p,
                ),
                "expected_baseline_fan_power_exhaust": CalcQ(
                    "electric_power",
                    total_modeled_fan_power_b * fraction_of_total_exhaust_p,
                ),
                "expected_baseline_fan_power_relief": CalcQ(
                    "electric_power",
                    total_modeled_fan_power_b * fraction_of_total_relief_p,
                ),
            }

        def rule_check(self, context, calc_vals=None, data=None):
            hvac_sys_total_supply_fan_power_b = calc_vals[
                "hvac_sys_total_supply_fan_power_b"
            ]
            hvac_sys_total_return_fan_power_b = calc_vals[
                "hvac_sys_total_return_fan_power_b"
            ]
            hvac_sys_total_exhaust_fan_power_b = calc_vals[
                "hvac_sys_total_exhaust_fan_power_b"
            ]
            hvac_sys_total_relief_fan_power_b = calc_vals[
                "hvac_sys_total_relief_fan_power_b"
            ]
            expected_baseline_fan_power_supply = calc_vals[
                "expected_baseline_fan_power_supply"
            ]
            expected_baseline_fan_power_return = calc_vals[
                "expected_baseline_fan_power_return"
            ]
            expected_baseline_fan_power_exhaust = calc_vals[
                "expected_baseline_fan_power_exhaust"
            ]
            expected_baseline_fan_power_relief = calc_vals[
                "expected_baseline_fan_power_relief"
            ]
            return (
                self.precision_comparison["hvac_sys_total_supply_fan_power_b"](
                    hvac_sys_total_supply_fan_power_b,
                    expected_baseline_fan_power_supply,
                )
                and self.precision_comparison["hvac_sys_total_supply_fan_power_b"](
                    hvac_sys_total_return_fan_power_b,
                    expected_baseline_fan_power_return,
                )
                and self.precision_comparison["hvac_sys_total_exhaust_fan_power_b"](
                    hvac_sys_total_exhaust_fan_power_b,
                    expected_baseline_fan_power_exhaust,
                )
                and self.precision_comparison["hvac_sys_total_relief_fan_power_b"](
                    hvac_sys_total_relief_fan_power_b,
                    expected_baseline_fan_power_relief,
                )
            )

        def is_tolerance_fail(self, context, calc_vals=None, data=None):
            hvac_sys_total_supply_fan_power_b = calc_vals[
                "hvac_sys_total_supply_fan_power_b"
            ]
            hvac_sys_total_return_fan_power_b = calc_vals[
                "hvac_sys_total_return_fan_power_b"
            ]
            hvac_sys_total_exhaust_fan_power_b = calc_vals[
                "hvac_sys_total_exhaust_fan_power_b"
            ]
            hvac_sys_total_relief_fan_power_b = calc_vals[
                "hvac_sys_total_relief_fan_power_b"
            ]
            expected_baseline_fan_power_supply = calc_vals[
                "expected_baseline_fan_power_supply"
            ]
            expected_baseline_fan_power_return = calc_vals[
                "expected_baseline_fan_power_return"
            ]
            expected_baseline_fan_power_exhaust = calc_vals[
                "expected_baseline_fan_power_exhaust"
            ]
            expected_baseline_fan_power_relief = calc_vals[
                "expected_baseline_fan_power_relief"
            ]
            return (
                std_equal(
                    hvac_sys_total_supply_fan_power_b,
                    expected_baseline_fan_power_supply,
                )
                and std_equal(
                    hvac_sys_total_return_fan_power_b,
                    expected_baseline_fan_power_return,
                )
                and std_equal(
                    hvac_sys_total_exhaust_fan_power_b,
                    expected_baseline_fan_power_exhaust,
                )
                and std_equal(
                    hvac_sys_total_relief_fan_power_b,
                    expected_baseline_fan_power_relief,
                )
            )

        def get_fail_msg(self, context, calc_vals=None, data=None):
            hvac_b = context.BASELINE_0
            hvac_id_b = hvac_b["id"]
            expected_baseline_fan_power_supply = calc_vals[
                "expected_baseline_fan_power_supply"
            ]
            expected_baseline_fan_power_return = calc_vals[
                "expected_baseline_fan_power_return"
            ]
            expected_baseline_fan_power_exhaust = calc_vals[
                "expected_baseline_fan_power_exhaust"
            ]
            expected_baseline_fan_power_relief = calc_vals[
                "expected_baseline_fan_power_relief"
            ]

            return f"The calculated system fan power doesn't appear to be distributed to the supply, return, exhaust, and relief fans in the same proportion as the proposed design for {hvac_id_b}.The expected modeled baseline supply, return, exhaust, and relief kW is {expected_baseline_fan_power_supply}, {expected_baseline_fan_power_return}, {expected_baseline_fan_power_exhaust}, {expected_baseline_fan_power_relief} respectively."
