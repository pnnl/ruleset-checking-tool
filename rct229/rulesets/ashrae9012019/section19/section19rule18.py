from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.data_fns.table_G3_9_1_fins import table_G3_9_1_lookup
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
from rct229.schema.config import ureg
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all, find_one
from rct229.utils.pint_utils import ZERO
from rct229.utils.std_comparisons import std_equal

ENERGY_RECOVERY = SchemaEnums.schema_enums["EnergyRecoveryOptions"]
APPLICABLE_SYS_TYPES = [
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
CONSTANT_VOLUME_SYS_TYPES = [
    HVAC_SYS.SYS_3,
    HVAC_SYS.SYS_4,
    HVAC_SYS.SYS_12,
    HVAC_SYS.SYS_13,
]
VARIABLE_VOLUME_SYS_TYPES = [
    HVAC_SYS.SYS_5,
    HVAC_SYS.SYS_6,
    HVAC_SYS.SYS_7,
    HVAC_SYS.SYS_8,
]


class PRM9012019Rule49c09(RuleDefinitionListIndexedBase):
    """Rule 18 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(PRM9012019Rule49c09, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012019Rule49c09.HVACRule(),
            index_rmd=BASELINE_0,
            id="19-18",
            description="For baseline systems 3 through 8, and 11, 12, and 13, the system fan electrical power for supply, return, exhaust, "
            "and relief shall be Pfan = bhp × 746/fan motor efficiency. Where, bhp = brake horsepower of baseline fan motor from Table G3.1.2.9; fan motor efficiency = the efficiency from Table G3.9.1 for the next motor size greater than the bhp using a totally enclosed fan cooled motor at 1800 rpm..",
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
        applicable_hvac_sys_ids = [
            hvac_id
            for sys_type in baseline_system_types_dict
            for target_sys_type in APPLICABLE_SYS_TYPES
            if baseline_system_type_compare(sys_type, target_sys_type, False)
            for hvac_id in baseline_system_types_dict[sys_type]
        ]

        zones_and_terminal_units_served_by_hvac_sys_dict_b = (
            get_dict_of_zones_and_terminal_units_served_by_hvac_sys(rmd_b)
        )

        zonal_exhaust_fan_elec_power_b = {}
        for hvac_id_b in find_all(
            "$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*].id",
            rmd_b,
        ):
            zonal_exhaust_fan_elec_power_b[hvac_id_b] = ZERO.POWER
            for zone_id_b in zones_and_terminal_units_served_by_hvac_sys_dict_b[
                hvac_id_b
            ]["zone_list"]:
                zonal_exhaust_fan_b = find_one(
                    f'$.buildings[*].building_segments[*].zones[*][?(@.id="{zone_id_b}")].zonal_exhaust_fan',
                    rmd_b,
                )
                if zonal_exhaust_fan_b:
                    zonal_exhaust_fan_elec_power_b[
                        hvac_id_b
                    ] += get_fan_object_electric_power(zonal_exhaust_fan_b)

        return {
            "baseline_system_types_dict": baseline_system_types_dict,
            "applicable_hvac_sys_ids": applicable_hvac_sys_ids,
            "zones_and_terminal_units_served_by_hvac_sys_dict_b": zones_and_terminal_units_served_by_hvac_sys_dict_b,
            "zonal_exhaust_fan_elec_power_b": zonal_exhaust_fan_elec_power_b,
        }

    class HVACRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule49c09.HVACRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={
                    "$": ["fan_system"],
                },
                precision={
                    "total_fan_power_b": {
                        "precision": 1,
                        "unit": "W",
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
            hvac_b_id = hvac_b["id"]

            baseline_system_types_dict = data["baseline_system_types_dict"]
            zonal_exhaust_fan_elec_power_b = data["zonal_exhaust_fan_elec_power_b"][
                hvac_b_id
            ]

            sys_type_b = next(
                (
                    key
                    for key, values in baseline_system_types_dict.items()
                    if hvac_b_id in values
                ),
                None,
            )

            fan_sys_b = hvac_b["fan_system"]
            fan_sys_info_b = (
                get_fan_system_object_supply_return_exhaust_relief_total_power_flow(
                    fan_sys_b
                )
            )
            supply_flow_b = fan_sys_info_b["supply_fans_airflow"].to(ureg.cfm)

            exactly_one_supply_fan = fan_sys_info_b["supply_fans_qty"] == 1
            total_fan_power_b = (
                (
                    fan_sys_info_b["supply_fans_power"]
                    + fan_sys_info_b["return_fans_power"]
                    + fan_sys_info_b["exhaust_fans_power"]
                    + fan_sys_info_b["relief_fans_power"]
                    + zonal_exhaust_fan_elec_power_b
                )
                if exactly_one_supply_fan
                else ZERO.POWER
            ).to(ureg.hp)

            A = 0.0
            more_than_one_exhaust_fan_and_energy_rec_is_relevant_b = False
            if (
                fan_sys_b.get("air_energy_recovery")
                and fan_sys_b["air_energy_recovery"].get("type") != ENERGY_RECOVERY.NONE
                and fan_sys_info_b["exhaust_fans_qty"] > 1
            ):
                more_than_one_exhaust_fan_and_energy_rec_is_relevant_b = True
                enthalpy_reco_ratio_b = getattr_(
                    fan_sys_b,
                    "fan_system",
                    "air_energy_recovery",
                    "enthalpy_recovery_ratio",
                )
                ERV_OA_air_flow_b = getattr_(
                    fan_sys_b, "fan_system", "air_energy_recovery", "outdoor_airflow"
                ).to(ureg.cfm)
                ERV_EX_air_flow_b = getattr_(
                    fan_sys_b, "fan_system", "air_energy_recovery", "exhaust_airflow"
                ).to(ureg.cfm)
                A = (
                    (2.2 * enthalpy_reco_ratio_b - 0.5)
                    * (ERV_OA_air_flow_b + ERV_EX_air_flow_b)
                    / 4131
                )

            MERV_rating = (
                fan_sys_b["air_filter_merv_rating"]
                if fan_sys_b.get("air_filter_merv_rating") is not None
                else 0
            )

            if 9 <= MERV_rating <= 12:
                MERV_adj = 0.5
            elif MERV_rating > 12:
                MERV_adj = 0.9
            else:
                MERV_adj = 0.0

            A += MERV_adj * supply_flow_b / 4131
            if any(
                [
                    baseline_system_type_compare(sys_type_b, target_sys_type, False)
                    for target_sys_type in CONSTANT_VOLUME_SYS_TYPES
                ]
            ):
                expected_BHP_b = (0.00094 * supply_flow_b + A).m * ureg("hp")
                min_BHP_b = (0.00094 * supply_flow_b).m * ureg("hp")
            elif any(
                [
                    baseline_system_type_compare(sys_type_b, target_sys_type, False)
                    for target_sys_type in VARIABLE_VOLUME_SYS_TYPES
                ]
            ):
                expected_BHP_b = (0.0013 * supply_flow_b + A).m * ureg("hp")
                min_BHP_b = (0.0013 * supply_flow_b).m * ureg("hp")
            else:
                expected_BHP_b = (0.00062 * supply_flow_b + A).m * ureg("hp")
                min_BHP_b = (0.00062 * supply_flow_b).m * ureg("hp")

            expected_motor_efficiency_b = table_G3_9_1_lookup(expected_BHP_b)[
                "full_load_motor_efficiency_for_modeling"
            ]
            min_motor_efficiency_b = table_G3_9_1_lookup(min_BHP_b)[
                "full_load_motor_efficiency_for_modeling"
            ]

            expected_fan_wattage_b = expected_BHP_b / expected_motor_efficiency_b
            min_fan_wattage_b = min_BHP_b / min_motor_efficiency_b

            return {
                "exactly_one_supply_fan": exactly_one_supply_fan,
                "more_than_one_exhaust_fan_and_energy_rec_is_relevant_b": more_than_one_exhaust_fan_and_energy_rec_is_relevant_b,
                "total_fan_power_b": total_fan_power_b,
                "expected_fan_wattage_b": expected_fan_wattage_b,
                "min_fan_wattage_b": min_fan_wattage_b,
            }

        def manual_check_required(self, context, calc_vals=None, data=None):
            exactly_one_supply_fan = calc_vals["exactly_one_supply_fan"]
            more_than_one_exhaust_fan_and_energy_rec_is_relevant_b = calc_vals[
                "more_than_one_exhaust_fan_and_energy_rec_is_relevant_b"
            ]
            total_fan_power_b = calc_vals["total_fan_power_b"]
            expected_fan_wattage_b = calc_vals["expected_fan_wattage_b"]

            return (
                not exactly_one_supply_fan
                or more_than_one_exhaust_fan_and_energy_rec_is_relevant_b
                or (total_fan_power_b > expected_fan_wattage_b)
            )

        def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
            hvac_b = context.BASELINE_0
            hvac_id_b = hvac_b["id"]

            more_than_one_exhaust_fan_and_energy_rec_is_relevant_b = calc_vals[
                "more_than_one_exhaust_fan_and_energy_rec_is_relevant_b"
            ]
            exactly_one_supply_fan = calc_vals["exactly_one_supply_fan"]
            expected_fan_wattage_b = calc_vals["expected_fan_wattage_b"]

            black_word = (
                ""
                if more_than_one_exhaust_fan_and_energy_rec_is_relevant_b
                else "energy recovery"
            )

            undetermined_msg = ""
            if (
                not exactly_one_supply_fan
                or more_than_one_exhaust_fan_and_energy_rec_is_relevant_b
            ):
                undetermined_msg = (
                    f"{hvac_id_b} has more than one supply fan and/or more than one exhaust fan associated with the HVAC system in the baseline and "
                    f"therefore this check could not be conducted for this HVAC system. Conduct manual check for compliance with G3.1.2.9."
                )
            else:
                undetermined_msg = (
                    f"Fan power for {hvac_id_b} is greater than expected per Section and Table G3.1.2.9 assuming no pressure drop adjustments (e.g., sound attenuation, air filtration, fully ducted return "
                    f"when required by code, airflow control devices, carbon and other gas-phase air cleaners, coil runaround loops, evaporative humidifier/coolers in series with another cooling coil, "
                    f"exhaust systems serving fume hoods, and laboratory and vivarium exhaust systems in high-rise buildings) per Table 6.5.3.1-2 other than {black_word} and "
                    f"MERV filters defined in the RMD (if modeled). Expected Wattage = {expected_fan_wattage_b.to(ureg.kW)} kW. however not all pressure drop adjustments are able to be captured in the RMD so conduct manual check."
                )

            return undetermined_msg

        def rule_check(self, context, calc_vals=None, data=None):
            total_fan_power_b = calc_vals["total_fan_power_b"]
            expected_fan_wattage_b = calc_vals["expected_fan_wattage_b"]

            return self.precision_comparison["total_fan_power_b"](
                total_fan_power_b,
                expected_fan_wattage_b,
            )

        def is_tolerance_fail(self, context, calc_vals=None, data=None):
            total_fan_power_b = calc_vals["total_fan_power_b"]
            expected_fan_wattage_b = calc_vals["expected_fan_wattage_b"]

            return std_equal(
                total_fan_power_b,
                expected_fan_wattage_b,
            )

        def get_fail_msg(self, context, calc_vals=None, data=None):
            total_fan_power_b = calc_vals["total_fan_power_b"]
            min_fan_wattage_b = calc_vals["min_fan_wattage_b"]

            return (
                f"The total fan power for <insert hvac.id> is modeled as {total_fan_power_b.to(ureg.kW)} kW which is less than the expected including pressure drop adjustments "
                f"for exhaust air energy recovery and MERV filters as applicable which was calculated as {min_fan_wattage_b.to(ureg.kW)} kW ."
            )
