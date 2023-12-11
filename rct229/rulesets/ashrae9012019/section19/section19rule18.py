from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_instance
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.schema.schema_enums import SchemaEnums
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
from rct229.utils.assertions import assert_
from rct229.utils.jsonpath_utils import find_all, find_one
from rct229.utils.pint_utils import ZERO
from rct229.utils.std_comparisons import std_equal
from rct229.utils.utility_functions import (
    find_exactly_one_hvac_system,
    find_exactly_one_zone,
)

APPLICABLE_SYS_TYPES = [
HVAC_SYS.SYS_3, HVAC_SYS.SYS_4, HVAC_SYS.SYS_5, HVAC_SYS.SYS_6, HVAC_SYS.SYS_7, HVAC_SYS.SYS_8, HVAC_SYS.SYS_11_1, HVAC_SYS.SYS_12, HVAC_SYS.SYS_13
]
CV_system_types = [HVAC_SYS.SYS_3, HVAC_SYS.SYS_4,HVAC_SYS.SYS_12, HVAC_SYS.SYS_13]


COOLING_SYSTEM = SchemaEnums.schema_enums["CoolingSystemOptions"]
REQ_FAN_POWER_FLOW_RATIO = 0.3 * ureg("W/cfm")


class Section19Rule18(RuleDefinitionListIndexedBase):
    """Rule 18 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(Section19Rule18, self).__init__(
            rmrs_used=produce_ruleset_model_instance(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=Section19Rule18.HVACRule(),
            index_rmr=BASELINE_0,
            id="19-18",
            description="For baseline systems 3 through 8, and 11, 12, and 13, the system fan electrical power for supply, return, exhaust, "
                        "and relief shall be Pfan = bhp × 746/fan motor efficiency. Where, bhp = brake horsepower of baseline fan motor from Table G3.1.2.9; fan motor efficiency = the efficiency from Table G3.9.1 for the next motor size greater than the bhp using a totally enclosed fan cooled motor at 1800 rpm..",
            ruleset_section_title="HVAC - General",
            standard_section="Section G3.1.2.9",
            is_primary_rule=True,
            rmr_context="ruleset_model_descriptions/0",
            list_path="$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
        )

    def is_applicable(self, context, data=None):
        rmd_b = context.BASELINE_0
        baseline_system_types_dict = get_baseline_system_types(rmd_b)

        return any(
            [
                baseline_system_type_compare(system_type, applicable_sys_type, False)
                for system_type in baseline_system_types_dict
                for applicable_sys_type in APPLICABLE_SYS_TYPES
            ]
        )

    def create_data(self, context, data):
        rmd_b = context.BASELINE_0
        rmd_p = context.PROPOSED

        baseline_system_types_dict = get_baseline_system_types(rmd_b)
        applicable_hvac_sys_ids = [ ##
            hvac_id
            for sys_type in baseline_system_types_dict
            for target_sys_type in APPLICABLE_SYS_TYPES
            if baseline_system_type_compare(sys_type, target_sys_type, False)
            for hvac_id in baseline_system_types_dict[sys_type]
        ]

        dict_of_zones_and_terminal_units_served_by_hvac_sys_b = (
            get_dict_of_zones_and_terminal_units_served_by_hvac_sys(rmd_b)
        )


        return {
            "applicable_hvac_sys_ids": applicable_hvac_sys_ids,
            "dict_of_zones_and_terminal_units_served_by_hvac_sys_b": dict_of_zones_and_terminal_units_served_by_hvac_sys_b,
        }

    def list_filter(self, context_item, data): ##
        applicable_hvac_sys_ids = data["applicable_hvac_sys_ids"]

        return context_item.BASELINE_0["id"] in applicable_hvac_sys_ids

    class HVACRule(RuleDefinitionBase):
        def __init__(self):
            super(Section19Rule18.HVACRule, self).__init__(
                rmrs_used=produce_ruleset_model_instance(
                    USER=False, BASELINE_0=True, PROPOSED=True
                ),
                required_fields={
                    "$": ["fan_system"],
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


            zone_list_b = dict_of_zones_and_terminal_units_served_by_hvac_sys_b[hvac_id_b]["zone_list"]

            fan_sys_b = hvac_b["fan_system"]
            fan_sys_info_b = (
                get_fan_system_object_supply_return_exhaust_relief_total_power_flow(
                    fan_sys_b
                )
            )
            supply_flow_b = fan_sys_info_b["supply_fans_airflow"]
            total_exhaust_airflow_b = fan_sys_info_b["exhaust_fans_airflow"]
            more_than_one_supply_fan_b = False if fan_sys_info_b["supply_fans_qty"] > 1 else True

            total_fan_power_b = (
                    fan_sys_info_b["supply_fans_power"]
                    + fan_sys_info_b["return_fans_power"]
                    + fan_sys_info_b["exhaust_fans_power"]
                    + fan_sys_info_b["relief_fans_power"]
                    + zonal_exhaust_fan_elec_power_b
            )


            if fan_sys_b.get("air_energy_recovery") is None and fan_sys_info_b["exhaust_fans_qty"] ==1:
                more_than_one_exhaust_fan_and_energy_rec_is_relevant = False
                enthalpy_rec_ratio = getattr(fan_sys_b, "", "air_energy_recovery", "enthalpy_recovery_ratio")
                ERV_OA_air_flow = getattr(fan_sys_b, "", "air_energy_recovery", "outside_air_flow")
                ERV_Ex_air_flow  = getattr(fan_sys_b, "", "air_energy_recovery", "exhaust_air_flow")
                A = (((2.2*enthalpy_rec_ratio)-0.5) *(ERV_Ex_air_flow + ERV_OA_air_flow))/4131

            MERV_rating = getattr(fan_sys_b, "", "air_filter_merv_rating") if fan_sys_b.get("air_filter_merv_rating") is not None else 0

            if 9 <= MERV_rating  <= 12:
                MERV_adj  = 0.5
            elif MERV_rating > 23:
                MERV_adj = 0.9
            else:
                MERV_adj = 0

            A += (MERV_adj * supply_flow_b/4131)

            if any(baseline_system_type_compare(sys_type, target_sys_type, False) for target_system_type in  CV_system_types):
                expected_BHP = (0.00094 * supply_flow_b) + A
                minimum_BHP = (0.00094 * supply_flow_b)
            elif any(baseline_system_type_compare(sys_type, target_sys_type, False) for target_system_type in [HVAC_SYS.SYS_5, HVAC_SYS.SYS_6, HVAC_SYS.SYS_7, HVAC_SYS.SYS_8]):
                expected_BHP = (0.0013 * supply_flow_b) + A
                minimum_BHP = (0.0013 * supply_flow_b)
            else:
                expected_BHP = (0.00062 * supply_flow_b) + A
                minimum_BHP = (0.00062 * supply_flow_b)

            motor_eff_ex =
            motor_eff_min =

            fan_Wattage_expected = expected_BHP * 746 * (1 / motor_eff_ex)
            fan_Wattage_minimim = minimum_BHP * 746 * (1 / motor_eff_min)

            return {

            }

        def manual_check_required(self, context, calc_vals=None, data=None):

            return

        def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
            hvac_b = context.BASELINE_0
            hvac_id_b = hvac_b["id"]

            return

        def rule_check(self, context, calc_vals=None, data=None):
            more_than_one_exhaust_fan_and_energy_rec_is_relevant = calc_vals["more_than_one_exhaust_fan_and_energy_rec_is_relevant"]
            more_than_one_supply_fan = calc_vals["more_than_one_supply_fan"]
            total_fan_power_b = calc_vals["total_fan_power_b"]
            fan_Wattage_expected = calc_vals["fan_Wattage_expected"]

            return not more_than_one_exhaust_fan_and_energy_rec_is_relevant and not more_than_one_supply_fan and std_equal(total_fan_power_b, fan_Wattage_expected) or (
                    not more_than_one_exhaust_fan_and_energy_rec_is_relevant and total_fan_power_b < fan_Wattage_expected
            )
        def get_pass_msg(self, context, calc_vals=None, data=None):
            hvac_b = context.BASELINE_0
            hvac_id_b = hvac_b["id"]
            more_than_one_exhaust_fan_and_energy_rec_is_relevant = calc_vals[
                "more_than_one_exhaust_fan_and_energy_rec_is_relevant"]
            total_fan_power_b = calc_vals["total_fan_power_b"]
            fan_Wattage_expected = calc_vals["fan_Wattage_expected"]
            fan_Wattage_minimim = calc_vals["fan_Wattage_minimim"]


            if  not more_than_one_exhaust_fan_and_energy_rec_is_relevant and total_fan_power_b < fan_Wattage_expected:
                pass_msg = f"The total fan power for {hvac_id_b} is modeled as {total_fan_power_b} kW which is less than the expected including pressure drop adjustments " \
                           f"for exhaust air energy recovery and MERV filters as applicable which was calculated as {fan_Wattage_minimim} kW. Pass because this is generally considered more conservative."
            else:
                pass_msg = ""

            return pass_msg

        def get_fail_msg(self, context, calc_vals=None, data=None):
            total_fan_power_b = calc_vals["total_fan_power_b"]
            fan_Wattage_minimim = calc_vals["fan_Wattage_minimim"]

            return f"The total fan power for <insert hvac.id> is modeled as {total_fan_power_b} kW which is less than the expected including pressure drop adjustments " \
                   f"for exhaust air energy recovery and MERV filters as applicable which was calculated as {fan_Wattage_minimim} kW ."
