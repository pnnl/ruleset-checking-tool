from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.rulesets.ashrae9012019.data.schema_enums import schema_enums
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_system_type_compare import (
    baseline_system_type_compare,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
    find_exactly_one_hvac_system,
    find_exactly_one_zone,
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
from rct229.utils.assertions import assert_, getattr_
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import ZERO
from rct229.utils.std_comparisons import std_equal

APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_9,
    HVAC_SYS.SYS_10,
]


COOLING_SYSTEM = schema_enums["CoolingSystemOptions"]
REQ_FAN_POWER_FLOW_RATIO = 0.3 * ureg("W/cfm")


class Section19Rule19(RuleDefinitionListIndexedBase):
    """Rule 19 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(Section19Rule19, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, True),
            each_rule=Section19Rule19.HVACRule(),
            index_rmr="baseline",
            id="19-19",
            description="For baseline systems 9 and 10 the system fan electrical power (Pfan) for supply, return, exhaust, and relief shall be CFMs × 0.3, where, CFMs = the baseline system maximum design supply fan airflow rate, cfm. If modeling a non-mechanical cooling fan is required by Section G3.1.2.8.2, there is a fan power allowance of Pfan = CFMnmc × 0.054, where, CFMnmc = the baseline non-mechanical cooling fan airflow, cfm for the non-mechanical cooling.",
            ruleset_section_title="HVAC - General",
            standard_section="Section G3.1.2.9",
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
        rmi_p = context.proposed

        baseline_system_types_dict = get_baseline_system_types(rmi_b)
        applicable_hvac_sys_ids = [
            hvac_id
            for sys_type in baseline_system_types_dict
            for target_sys_type in APPLICABLE_SYS_TYPES
            if baseline_system_type_compare(sys_type, target_sys_type, False)
            for hvac_id in baseline_system_types_dict[sys_type]
        ]

        dict_of_zones_and_terminal_units_served_by_hvac_sys_b = (
            get_dict_of_zones_and_terminal_units_served_by_hvac_sys(rmi_b)
        )

        zone_hvac_non_mech_cooling_map = {}
        for zone_id_p in find_all(
            "$.buildings[*].building_segments[*].zones[*]", rmi_p
        ):
            zone_hvac_non_mech_cooling_map[zone_id_p] = any(
                [
                    getattr_(
                        find_exactly_one_hvac_system(rmi_p, hvac_id_p),
                        "HVAC",
                        "cooling_system",
                        "cooling_system_type",
                    )
                    == COOLING_SYSTEM.NON_MECHANICAL
                    for hvac_id_p in get_list_hvac_systems_associated_with_zone(
                        rmi_p, zone_id_p
                    )
                ]
            )

        hvac_map = {}
        for hvac_id_b in find_all(
            "$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*].id",
            rmi_b,
        ):
            zonal_exhaust_fan_elec_power_b = ZERO.POWER
            zones_served_by_hvac_has_non_mech_cooling_bool_p = False

            for zone_id_b in dict_of_zones_and_terminal_units_served_by_hvac_sys_b[
                hvac_id_b
            ]["zone_list"]:
                zone_p = find_exactly_one_zone(zone_id_b, rmi_p)

                zonal_exhaust_fan_elec_power_b += get_fan_object_electric_power(
                    zone_p.get("zonal_exhaust_fan")
                )

                if (
                    zone_p.get("non_mechanical_cooling_fan_airflow") is not None
                    and zone_p["non_mechanical_cooling_fan_airflow"] > ZERO.FLOW
                ):
                    zones_served_by_hvac_has_non_mech_cooling_bool_p = True

                if zone_hvac_non_mech_cooling_map[zone_id_b]:
                    zones_served_by_hvac_has_non_mech_cooling_bool_p = True

            hvac_map[hvac_id_b] = {
                "zones_served_by_hvac_has_non_mech_cooling_bool_p": zones_served_by_hvac_has_non_mech_cooling_bool_p
            }

        return {
            "applicable_hvac_sys_ids": applicable_hvac_sys_ids,
            "zonal_exhaust_fan_elec_power_b": zonal_exhaust_fan_elec_power_b,
            "hvac_map": hvac_map,
        }

    def list_filter(self, context_item, data):
        applicable_hvac_sys_ids = data["applicable_hvac_sys_ids"]

        return context_item.baseline["id"] in applicable_hvac_sys_ids

    class HVACRule(RuleDefinitionBase):
        def __init__(self):
            super(Section19Rule19.HVACRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, True),
                required_fields={
                    "$": ["fan_system"],
                },
            )

        def is_applicable(self, context, data=None):
            hvac_b = context.baseline
            hvac_id_b = hvac_b["id"]
            applicable_hvac_sys_ids = data["applicable_hvac_sys_ids"]

            return hvac_id_b in applicable_hvac_sys_ids

        def get_calc_vals(self, context, data=None):
            hvac_b = context.baseline
            hvac_id_b = hvac_b["id"]

            hvac_map = data["hvac_map"][hvac_id_b]

            zonal_exhaust_fan_elec_power_b = hvac_map["zonal_exhaust_fan_elec_power_b"]
            zones_served_by_hvac_has_non_mech_cooling_bool_p = hvac_map[
                "zones_served_by_hvac_has_non_mech_cooling_bool_p"
            ]
            zone_hvac_has_non_mech_cooling_p = data["zone_hvac_has_non_mech_cooling_p"]

            fan_sys_b = hvac_b["fan_system"]

            fan_sys_info_b = (
                get_fan_system_object_supply_return_exhaust_relief_total_power_flow(
                    fan_sys_b
                )
            )
            supply_fans_qty_b = fan_sys_info_b["supply_fans_qty"]
            more_than_one_supply_fan_b = True if supply_fans_qty_b > 1 else False

            assert_(
                supply_fans_qty_b < 1,
                f"No supply fan is found in HVAC {hvac_id_b} fan system.",
            )

            total_fan_power_b = (
                fan_sys_info_b["supply_fans_total_fan_power"]
                + fan_sys_info_b["return_fans_total_fan_power"]
                + fan_sys_info_b["exhaust_fans_total_fan_power"]
                + fan_sys_info_b["relief_fans_total_fan_power"]
                + zonal_exhaust_fan_elec_power_b
            )

            supply_fan_flow_b = fan_sys_info_b["supply_fans_airflow"]

            assert_(
                supply_fan_flow_b > 0, f"Supply fan air flow in HVAC {hvac_id_b} is 0."
            )

            fan_power_per_flow_b = (
                total_fan_power_b / supply_fan_flow_b
                if supply_fan_flow_b != ZERO.FLOW
                else ZERO.POWER_PER_FLOW
            )

            return {
                "zones_served_by_hvac_has_non_mech_cooling_bool_p": zones_served_by_hvac_has_non_mech_cooling_bool_p,
                "zone_hvac_has_non_mech_cooling_p": zone_hvac_has_non_mech_cooling_p,
                "more_than_one_supply_fan_b": more_than_one_supply_fan_b,
                "fan_power_per_flow_b": fan_power_per_flow_b,
            }

        def manual_check_required(self, context, calc_vals=None, data=None):
            more_than_one_supply_fan_b = calc_vals["more_than_one_supply_fan_b"]
            zone_hvac_has_non_mech_cooling_p = calc_vals[
                "zone_hvac_has_non_mech_cooling_p"
            ]
            zones_served_by_hvac_has_non_mech_cooling_bool_p = calc_vals[
                "zones_served_by_hvac_has_non_mech_cooling_bool_p"
            ]

            return (
                more_than_one_supply_fan_b
                or zone_hvac_has_non_mech_cooling_p
                or zones_served_by_hvac_has_non_mech_cooling_bool_p
            )

        def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
            hvac_b = context.baseline
            hvac_id_b = hvac_b["id"]
            more_than_one_supply_fan_b = data["more_than_one_supply_fan_b"]

            if more_than_one_supply_fan_b:
                UNDERMINED_MSG = f"{hvac_id_b} has more than one supply fan associated with the HVAC system in the baseline and therefore this check could not be conducted for this HVAC sytem. Conduct manual check for compliance with G3.1.2.9."
            else:
                UNDERMINED_MSG = f"{hvac_id_b} has zone(s) with non-mechanical cooling in the proposed design, conduct a manual check that the baseline building design includes a fan power allowance of <insert IP or SI version as applicable Pfan = CFMnmc × 0.054, where, CFMnmc = the baseline non-mechanical cooling fan airflow, cfm for the non-mechanical cooling fan in additional to the 0.3 W/CFM allowance for the HVAC system>."

            return UNDERMINED_MSG

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
                and std_equal(REQ_FAN_POWER_FLOW_RATIO, fan_power_per_flow_b)
            ) or (fan_power_per_flow_b < REQ_FAN_POWER_FLOW_RATIO,)

        def get_fail_msg(self, context, calc_vals=None, data=None):
            hvac_b = context.baseline
            hvac_id_b = hvac_b["id"]
            more_than_one_supply_fan_b = calc_vals["more_than_one_supply_fan_b"]
            fan_power_per_flow_b = calc_vals["fan_power_per_flow_b"]
            fan_power_per_flow_b = fan_power_per_flow_b.to(ureg("W/cfm"))

            fail_msg = ""
            if (
                not more_than_one_supply_fan_b
                and fan_power_per_flow_b < REQ_FAN_POWER_FLOW_RATIO
            ):
                fail_msg = f"ule evaluation fails with a conservative outcome. The fan power airflow (W/cfm) for {hvac_id_b} is modeled as {fan_power_per_flow_b} W/cfm which is less than the expected W/cfm."

            return fail_msg
