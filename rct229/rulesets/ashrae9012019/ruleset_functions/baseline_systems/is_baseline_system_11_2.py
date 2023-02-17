from rct229.rulesets.ashrae9012019.data.schema_enums import schema_enums
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_cool_sources_none_or_null import (
    are_all_terminal_cool_sources_none_or_null,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_fans_null import (
    are_all_terminal_fans_null,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_heat_sources_none_or_null import (
    are_all_terminal_heat_sources_none_or_null,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_types_VAV import (
    are_all_terminal_types_VAV,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.does_each_zone_have_only_one_terminal import (
    does_each_zone_have_only_one_terminal,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.does_hvac_system_serve_single_zone import (
    does_hvac_system_serve_single_zone,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_cooling_type_fluid_loop import (
    is_hvac_sys_cooling_type_fluid_loop,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_fan_sys_VSD import (
    is_hvac_sys_fan_sys_vsd,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_fluid_loop_attached_to_boiler import (
    is_hvac_sys_fluid_loop_attached_to_boiler,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_fluid_loop_attached_to_chiller import (
    is_hvac_sys_fluid_loop_attached_to_chiller,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_fluid_loop_purchased_CHW import (
    is_hvac_sys_fluid_loop_purchased_chw,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
    has_preheat_system,
)

HEATING_SYSTEM = schema_enums["HeatingSystemOptions"]


def is_baseline_system_11_2(rmi_b, hvac_b_id, terminal_unit_id_list, zone_id_list):
    """
    Get either Sys-11.2, Sys-11.2a or Not_Sys_11.2 string output which indicates whether the HVAC system is ASHRAE
    90.1 2019 Appendix G system 11.2 (Single Zone VAV System with Hot Water Heating (Boiler)) or system 11.2a (system
    11.2 with purchased CHW).

    Parameters
    ----------
    rmi_b: json To evaluate if the hvac system is modeled as either Sys-11.2, Sys-11.2a or Not_Sys_11.2 in the B_RMR.
    hvac_b_id: String, The id of the hvac system to evaluate.
    terminal_unit_id_list: List<String>, list of terminal unit IDs associated with the HVAC system to be evaluated. These are
                            sent to this function from the master get_baseline_system_types function.
    zone_id_list: List<String>, list of zone IDs associated with the HVAC system to be evaluated. These are sent to this
                        function from the master get_baseline_system_types function.

    Returns string The function returns either Sys-11.2, Sys-11.2a or Not_Sys string output which indicates
    whether the HVAC system is ASHRAE 90.1 2019 Appendix G 11.2 (Single Zone VAV System with Hot Water Heating (
    Boiler)) or system 11.2a (system 11.2 with purchased CHW). -------
    """
    is_baseline_system_11_2_str = HVAC_SYS.UNMATCHED

    # check if the hvac system has the required sub systems for system type 11.2
    # if preheat system DOESN'T exist, has_required_sys=True, else, False
    has_required_sys = not has_preheat_system(rmi_b, hvac_b_id)

    are_sys_data_matched = (
        has_required_sys
        and is_hvac_sys_cooling_type_fluid_loop(rmi_b, hvac_b_id)
        and is_hvac_sys_fan_sys_vsd(rmi_b, hvac_b_id)
        and does_hvac_system_serve_single_zone(rmi_b, zone_id_list)
        and does_each_zone_have_only_one_terminal(rmi_b, zone_id_list)
        and are_all_terminal_cool_sources_none_or_null(rmi_b, terminal_unit_id_list)
        and are_all_terminal_heat_sources_none_or_null(rmi_b, terminal_unit_id_list)
        and are_all_terminal_fans_null(rmi_b, terminal_unit_id_list)
        and are_all_terminal_types_VAV(rmi_b, terminal_unit_id_list)
    )

    if are_sys_data_matched and is_hvac_sys_fluid_loop_attached_to_boiler(
        rmi_b, hvac_b_id
    ):
        if is_hvac_sys_fluid_loop_attached_to_chiller(rmi_b, hvac_b_id):
            is_baseline_system_11_2_str = HVAC_SYS.SYS_11_2
        elif is_hvac_sys_fluid_loop_purchased_chw(rmi_b, hvac_b_id):
            is_baseline_system_11_2_str = HVAC_SYS.SYS_11_2A

    return is_baseline_system_11_2_str
