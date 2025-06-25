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
from rct229.rulesets.ashrae9012019.ruleset_functions.get_fan_system_object_supply_return_exhaust_relief_total_power_flow import (
    get_fan_system_object_supply_return_exhaust_relief_total_power_flow,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_list_hvac_systems_associated_with_zone import (
    get_list_hvac_systems_associated_with_zone,
)
from rct229.schema.config import ureg
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import assert_
from rct229.utils.jsonpath_utils import find_all, find_one
from rct229.utils.pint_utils import ZERO
from rct229.utils.std_comparisons import std_equal
from rct229.utils.utility_functions import (
    find_exactly_one_hvac_system,
    find_exactly_one_zone,
)

APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_9,
    HVAC_SYS.SYS_10,
]


COOLING_SYSTEM = SchemaEnums.schema_enums["CoolingSystemOptions"]
REQ_FAN_POWER_FLOW_RATIO = 0.3 * ureg("W/cfm")


class PRM9012019Rule51d17(RuleDefinitionListIndexedBase):
    """Rule 19 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(PRM9012019Rule51d17, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=PRM9012019Rule51d17.HVACRule(),
            index_rmd=BASELINE_0,
            id="19-19",
            description="For baseline systems 9 and 10 the system fan electrical power (Pfan) for supply, return, exhaust, and relief shall be CFMs × 0.3, where, CFMs = the baseline system maximum design supply fan airflow rate, cfm. "
            "If modeling a non-mechanical cooling fan is required by Section G3.1.2.8.2, there is a fan power allowance of Pfan = CFMnmc × 0.054, where, CFMnmc = the baseline non-mechanical cooling fan airflow, cfm for the non-mechanical cooling.",
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
        rmd_p = context.PROPOSED

        baseline_system_types_dict = get_baseline_system_types(rmd_b)
        applicable_hvac_sys_ids = [
            hvac_id
            for sys_type in baseline_system_types_dict
            for target_sys_type in APPLICABLE_SYS_TYPES
            if baseline_system_type_compare(sys_type, target_sys_type, False)
            for hvac_id in baseline_system_types_dict[sys_type]
        ]

        dict_of_zones_and_terminal_units_served_by_hvac_sys_b = (
            get_dict_of_zones_and_terminal_units_served_by_hvac_sys(rmd_b)
        )

        zone_map = {}
        for zone_id_p in find_all(
            "$.buildings[*].building_segments[*].zones[*].id", rmd_p
        ):
            zone_map[zone_id_p] = any(
                [
                    find_one(
                        "$.cooling_system.cooling_system",
                        find_exactly_one_hvac_system(rmd_p, hvac_id_p),
                    )
                    == COOLING_SYSTEM.NON_MECHANICAL
                    for hvac_id_p in get_list_hvac_systems_associated_with_zone(
                        rmd_p, zone_id_p
                    )
                ]
            )

        hvac_map = {}
        for hvac_id_b in find_all(
            "$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*].id",
            rmd_b,
        ):
            hvac_map[hvac_id_b] = {
                "zonal_exhaust_fan_elec_power_b": ZERO.POWER,
                "zones_served_by_hvac_has_non_mech_cooling_bool_p": False,
            }
            for zone_id_b in dict_of_zones_and_terminal_units_served_by_hvac_sys_b[
                hvac_id_b
            ]["zone_list"]:
                zone_b = find_exactly_one_zone(rmd_b, zone_id_b)
                zone_p = find_exactly_one_zone(rmd_p, zone_id_b)

                zone_b_exhaust_fans = zone_b.get("zonal_exhaust_fans", [])
                zone_p_exhaust_fans = zone_p.get("zonal_exhaust_fans", [])
                zone_p_supply_fans = zone_p.get("supply_fans", [])

                for zone_b_exhaust_fan in zone_b_exhaust_fans:
                    hvac_map[hvac_id_b][
                        "zonal_exhaust_fan_elec_power_b"
                    ] += get_fan_object_electric_power(zone_b_exhaust_fan)

                zone_p_has_non_mech_cooling = any(
                    fan.get("design_airflow", 0) > ZERO.FLOW
                    for fan in zone_p_exhaust_fans + zone_p_supply_fans
                )

                hvac_map[hvac_id_b].update(
                    {
                        "zones_served_by_hvac_has_non_mech_cooling_bool_p": zone_p_has_non_mech_cooling
                    }
                )

        return {
            "applicable_hvac_sys_ids": applicable_hvac_sys_ids,
            "dict_of_zones_and_terminal_units_served_by_hvac_sys_b": dict_of_zones_and_terminal_units_served_by_hvac_sys_b,
            "zone_map": zone_map,
            "hvac_map": hvac_map,
        }

    def list_filter(self, context_item, data):
        applicable_hvac_sys_ids = data["applicable_hvac_sys_ids"]

        return context_item.BASELINE_0["id"] in applicable_hvac_sys_ids

    class HVACRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule51d17.HVACRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=True
                ),
                required_fields={
                    "$": ["fan_system"],
                },
                precision={
                    "fan_power_per_flow_b": {
                        "precision": 0.1,
                        "unit": "W/cfm",
                    },
                },
            )

        def is_applicable(self, context, data=None):
            hvac_b = context.BASELINE_0
            hvac_id_b = hvac_b["id"]
            applicable_hvac_sys_ids = data["applicable_hvac_sys_ids"]

            return hvac_id_b in applicable_hvac_sys_ids

        def get_calc_vals(self, context, data=None):
            hvac_b = context.BASELINE_0
            hvac_id_b = hvac_b["id"]

            dict_of_zones_and_terminal_units_served_by_hvac_sys_b = data[
                "dict_of_zones_and_terminal_units_served_by_hvac_sys_b"
            ]

            zone_dict_b = data["zone_map"]
            zone_hvac_has_non_mech_cooling_p = any(
                [
                    zone_dict_b[zone_id_p]
                    for zone_id_p in dict_of_zones_and_terminal_units_served_by_hvac_sys_b[
                        hvac_id_b
                    ][
                        "zone_list"
                    ]
                ]
            )

            hvac_dict_b = data["hvac_map"][hvac_id_b]
            zonal_exhaust_fan_elec_power_b = hvac_dict_b[
                "zonal_exhaust_fan_elec_power_b"
            ]
            zones_served_by_hvac_has_non_mech_cooling_bool_p = hvac_dict_b[
                "zones_served_by_hvac_has_non_mech_cooling_bool_p"
            ]

            fan_sys_b = hvac_b["fan_system"]

            fan_sys_info_b = (
                get_fan_system_object_supply_return_exhaust_relief_total_power_flow(
                    fan_sys_b
                )
            )
            supply_fans_qty_b = fan_sys_info_b["supply_fans_qty"]
            more_than_one_supply_fan_b = supply_fans_qty_b > 1

            assert_(
                supply_fans_qty_b > 0,
                f"No supply fan is found in HVAC {hvac_id_b} fan system.",
            )

            total_fan_power_b = (
                fan_sys_info_b["supply_fans_power"]
                + fan_sys_info_b["return_fans_power"]
                + fan_sys_info_b["exhaust_fans_power"]
                + fan_sys_info_b["relief_fans_power"]
                + zonal_exhaust_fan_elec_power_b
            )

            supply_fan_flow_b = fan_sys_info_b["supply_fans_airflow"]

            assert_(
                supply_fan_flow_b > ZERO.FLOW,
                f"Supply fan air flow in HVAC {hvac_id_b} is 0.",
            )

            fan_power_per_flow_b = total_fan_power_b / supply_fan_flow_b

            return {
                "zones_served_by_hvac_has_non_mech_cooling_bool_p": zones_served_by_hvac_has_non_mech_cooling_bool_p,
                "zone_hvac_has_non_mech_cooling_p": zone_hvac_has_non_mech_cooling_p,
                "more_than_one_supply_fan_b": more_than_one_supply_fan_b,
                "fan_power_per_flow_b": fan_power_per_flow_b,
            }

        def manual_check_required(self, context, calc_vals=None, data=None):
            more_than_one_supply_fan_b = calc_vals["more_than_one_supply_fan_b"]
            fan_power_per_flow_b = calc_vals["fan_power_per_flow_b"]
            zone_hvac_has_non_mech_cooling_p = calc_vals[
                "zone_hvac_has_non_mech_cooling_p"
            ]
            zones_served_by_hvac_has_non_mech_cooling_bool_p = calc_vals[
                "zones_served_by_hvac_has_non_mech_cooling_bool_p"
            ]

            return more_than_one_supply_fan_b or (
                (
                    fan_power_per_flow_b > REQ_FAN_POWER_FLOW_RATIO
                    or self.precision_comparison["fan_power_per_flow_b"](
                        fan_power_per_flow_b,
                        REQ_FAN_POWER_FLOW_RATIO,
                    )
                )
                and (
                    zone_hvac_has_non_mech_cooling_p
                    or zones_served_by_hvac_has_non_mech_cooling_bool_p
                )
            )

        def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
            hvac_b = context.BASELINE_0
            hvac_id_b = hvac_b["id"]
            more_than_one_supply_fan_b = calc_vals["more_than_one_supply_fan_b"]

            if more_than_one_supply_fan_b:
                UNDETERMINED_MSG = f"{hvac_id_b} has more than one supply fan associated with the HVAC system in the baseline and therefore this check could not be conducted for this HVAC sytem. Conduct manual check for compliance with G3.1.2.9."
            else:
                UNDETERMINED_MSG = f"{hvac_id_b} has zone(s) with non-mechanical cooling in the proposed design, conduct a manual check that the baseline building design includes a fan power allowance of <insert IP or SI version as applicable Pfan = CFMnmc × 0.054, where, CFMnmc = the baseline non-mechanical cooling fan airflow, cfm for the non-mechanical cooling fan in additional to the 0.3 W/CFM allowance for the HVAC system>."

            return UNDETERMINED_MSG

        def rule_check(self, context, calc_vals=None, data=None):
            zones_served_by_hvac_has_non_mech_cooling_bool_p = calc_vals[
                "zones_served_by_hvac_has_non_mech_cooling_bool_p"
            ]
            zone_hvac_has_non_mech_cooling_p = calc_vals[
                "zone_hvac_has_non_mech_cooling_p"
            ]
            fan_power_per_flow_b = calc_vals["fan_power_per_flow_b"]

            return (
                not zone_hvac_has_non_mech_cooling_p
                and not zones_served_by_hvac_has_non_mech_cooling_bool_p
                and self.precision_comparison["fan_power_per_flow_b"](
                    fan_power_per_flow_b,
                    REQ_FAN_POWER_FLOW_RATIO,
                )
            )

        def is_tolerance_fail(self, context, calc_vals=None, data=None):
            zones_served_by_hvac_has_non_mech_cooling_bool_p = calc_vals[
                "zones_served_by_hvac_has_non_mech_cooling_bool_p"
            ]
            zone_hvac_has_non_mech_cooling_p = calc_vals[
                "zone_hvac_has_non_mech_cooling_p"
            ]
            fan_power_per_flow_b = calc_vals["fan_power_per_flow_b"]

            return (
                not zone_hvac_has_non_mech_cooling_p
                and not zones_served_by_hvac_has_non_mech_cooling_bool_p
                and std_equal(REQ_FAN_POWER_FLOW_RATIO, fan_power_per_flow_b)
            ) or (fan_power_per_flow_b < REQ_FAN_POWER_FLOW_RATIO)

        def get_fail_msg(self, context, calc_vals=None, data=None):
            hvac_b = context.BASELINE_0
            hvac_id_b = hvac_b["id"]
            more_than_one_supply_fan_b = calc_vals["more_than_one_supply_fan_b"]
            fan_power_per_flow_b = calc_vals["fan_power_per_flow_b"]
            fan_power_per_flow_b = fan_power_per_flow_b.to(ureg("W/cfm"))

            fail_msg = ""
            if (
                not more_than_one_supply_fan_b
                and fan_power_per_flow_b < REQ_FAN_POWER_FLOW_RATIO
            ):
                fail_msg = f"Rule evaluation fails with a conservative outcome. The fan power airflow (W/cfm) for {hvac_id_b} is modeled as {fan_power_per_flow_b.magnitude} W/cfm which is less than the expected W/cfm."

            return fail_msg
