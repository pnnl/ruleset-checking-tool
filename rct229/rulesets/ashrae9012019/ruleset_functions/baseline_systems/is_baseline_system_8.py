from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_cool_sources_none_or_null import (
    are_all_terminal_cool_sources_none_or_null,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_fan_configs_parallel import (
    are_all_terminal_fan_configs_parallel,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_heat_sources_electric import (
    are_all_terminal_heat_sources_electric,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_heat_sources_hot_water import (
    are_all_terminal_heat_sources_hot_water,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_heating_loops_purchased_heating import (
    are_all_terminal_heating_loops_purchased_heating,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_types_VAV import (
    are_all_terminal_types_VAV,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.do_all_terminals_have_one_fan import (
    do_all_terminals_have_one_fan,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.does_each_zone_have_only_one_terminal import (
    does_each_zone_have_only_one_terminal,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_cooling_type_fluid_loop import (
    is_hvac_sys_cooling_type_fluid_loop,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_fan_sys_VSD import (
    is_hvac_sys_fan_sys_vsd,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_fluid_loop_attached_to_chiller import (
    is_hvac_sys_fluid_loop_attached_to_chiller,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_fluid_loop_purchased_CHW import (
    is_hvac_sys_fluid_loop_purchased_chw,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_preheat_fluid_loop_purchased_heating import (
    is_hvac_sys_preheat_fluid_loop_purchased_heating,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_preheating_type_elec_resistance import (
    is_hvac_sys_preheating_type_elec_resistance,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_preheating_type_fluid_loop import (
    is_hvac_sys_preheating_type_fluid_loop,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.utility_functions import has_heating_system, has_preheat_system

HEATING_SYSTEM = SchemaEnums.schema_enums["HeatingSystemOptions"]


def is_baseline_system_8(rmi_b, hvac_b_id, terminal_unit_id_list, zone_id_list):
    """
    Get either Sys-8, Sys-8a, Sys-8b, Sys-8c, or Not_Sys_8 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 8 (VAV with Parallel Fan-Powered Boxes and Reheat), system 8a (system 8 with purchased CHW), system 8b (system 8 with purchased heating), or 8c (system 8 with purchased heating and purchased chilled water).

    Parameters
    ----------
    rmi_b json
         To evaluate if the hvac system is modeled as either Sys-8, Sys-8a, Sys-8b, Sys-8c, or Not_Sys_8 in the B_RMI.
     hvac_b_id list
         The id of the hvac system to evaluate.
     terminal_unit_id_list
         List list of terminal unit IDs associated with the HVAC system to be evaluated. These are sent to this function from the master get_baseline_system_types function.
     zone_id_list list
         list of zone IDs associated with the HVAC system to be evaluated. These are sent to this function from the master get_baseline_system_types function.

    Returns
    -------
    The function returns either Sys-8, Sys-8a, Sys-8b, Sys-8c, or Not_Sys_8 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 8 (VAV with Parallel Fan-Powered Boxes and Reheat ), system 8a (system 8 with purchased CHW), system 8b (system 8 with purchased heating), or 8c (system 8 with purchased heating and purchased chilled water).
    """

    is_baseline_system_8 = HVAC_SYS.UNMATCHED

    # check if the hvac system has the required sub systems for system type 8
    # If heating system DOESN'T exist and preheat system exists, has_required_sys=True, else, False
    has_required_sys = not has_heating_system(rmi_b, hvac_b_id) and has_preheat_system(
        rmi_b, hvac_b_id
    )

    are_sys_data_matched = (
        # short-circuit the logic if no required data is found.
        has_required_sys
        # sub functions handles missing required sys, and return False.
        and is_hvac_sys_cooling_type_fluid_loop(rmi_b, hvac_b_id)
        and is_hvac_sys_fan_sys_vsd(rmi_b, hvac_b_id)
        and does_each_zone_have_only_one_terminal(rmi_b, zone_id_list)
        and are_all_terminal_cool_sources_none_or_null(rmi_b, terminal_unit_id_list)
        and do_all_terminals_have_one_fan(rmi_b, terminal_unit_id_list)
        and are_all_terminal_types_VAV(rmi_b, terminal_unit_id_list)
        and are_all_terminal_fan_configs_parallel(rmi_b, terminal_unit_id_list)
    )

    if are_sys_data_matched:
        if is_hvac_sys_preheating_type_elec_resistance(
            rmi_b, hvac_b_id
        ) and are_all_terminal_heat_sources_electric(rmi_b, terminal_unit_id_list):
            if is_hvac_sys_fluid_loop_attached_to_chiller(rmi_b, hvac_b_id):
                is_baseline_system_8 = HVAC_SYS.SYS_8
            elif is_hvac_sys_fluid_loop_purchased_chw(rmi_b, hvac_b_id):
                is_baseline_system_8 = HVAC_SYS.SYS_8A
        elif is_hvac_sys_preheating_type_fluid_loop(rmi_b, hvac_b_id):
            if (
                is_hvac_sys_preheat_fluid_loop_purchased_heating(rmi_b, hvac_b_id)
                and are_all_terminal_heat_sources_hot_water(
                    rmi_b, terminal_unit_id_list
                )
                and are_all_terminal_heating_loops_purchased_heating(
                    rmi_b, terminal_unit_id_list
                )
            ):
                if is_hvac_sys_fluid_loop_attached_to_chiller(rmi_b, hvac_b_id):
                    is_baseline_system_8 = HVAC_SYS.SYS_8B
                elif is_hvac_sys_fluid_loop_purchased_chw(rmi_b, hvac_b_id):
                    is_baseline_system_8 = HVAC_SYS.SYS_8C

    return is_baseline_system_8
