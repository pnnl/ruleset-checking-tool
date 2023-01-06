from rct229.data.schema_enums import schema_enums
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_cool_sources_none_or_null import (
    are_all_terminal_cool_sources_none_or_null,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_fans_null import (
    are_all_terminal_fans_null,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_heat_sources_none_or_null import (
    are_all_terminal_heat_sources_none_or_null,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_types_CAV import (
    are_all_terminal_types_cav,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.does_each_zone_have_only_one_terminal import (
    does_each_zone_have_only_one_terminal,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.does_hvac_system_serve_single_zone import (
    does_hvac_system_serve_single_zone,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_cooling_type_fluid_loop import (
    is_hvac_sys_cooling_type_fluid_loop,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_fan_sys_CV import (
    is_hvac_sys_fan_sys_cv,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_fluid_loop_attached_to_chiller import (
    is_hvac_sys_fluid_loop_attached_to_chiller,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_fluid_loop_purchased_CHW import (
    is_hvac_sys_fluid_loop_purchased_chw,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_heating_type_elec_resistance import (
    is_hvac_sys_heating_type_elec_resistance,
)
from rct229.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
    find_exactly_one_hvac_system,
)

HEATING_SYSTEM = schema_enums["HeatingSystemOptions"]


def is_baseline_system_13(rmi_b, hvac_b_id, terminal_unit_id_list, zone_id_list):
    """
    Get either Sys-13, Sys-13a, or Not_Sys_13 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 13
    (Single Zone Constant Volume System with CHW and Electric Resistance) or system 13a (system 13 with purchased CHW).

    Parameters
    ----------
    rmi_b: json
        To evaluate if the hvac system is modeled as either Sys-13, Sys-13a,or Not_Sys_13 in the B_RMI.

    hvac_b_id: list
        The id of the hvac system to evaluate.

    terminal_unit_id_list: list
        List of terminal unit IDs associated with the HVAC system to be evaluated. These are sent to this function from the mater get_baseline_system_types function.

    zone_id_list: list
        list of zone IDs associated with the HVAC system to be evaluated. These are sent to this function from the mater get_baseline_system_types function.

    Returns
    -------
        The function returns either Sys-13, Sys-13a, or Not_Sys_13 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 13 (Single Zone Constant Volume System with CHW and Electric Resistance) or system 13a (system 13 with purchased CHW).
    """

    is_baseline_system_13 = HVAC_SYS.UNMATCHED

    hvac_b = find_exactly_one_hvac_system(rmi_b, hvac_b_id)
    # check if the hvac system has the required sub systems for system type 13
    preheat_system = hvac_b.get("preheat_system")
    has_required_sys = (
        preheat_system is None
        or preheat_system.get("heating_system_type") is None
        or preheat_system["heating_system_type"] == HEATING_SYSTEM.NONE
    )

    are_sys_data_matched = (
        # short-circuit the logic if no required data is found.
        has_required_sys
        # sub functions handles missing required sys, and return False.
        and is_hvac_sys_heating_type_elec_resistance(rmi_b, hvac_b_id)
        and is_hvac_sys_cooling_type_fluid_loop(rmi_b, hvac_b_id)
        and is_hvac_sys_fan_sys_cv(rmi_b, hvac_b_id)
        and does_hvac_system_serve_single_zone(rmi_b, zone_id_list)
        and does_each_zone_have_only_one_terminal(rmi_b, zone_id_list)
        and are_all_terminal_heat_sources_none_or_null(rmi_b, terminal_unit_id_list)
        and are_all_terminal_cool_sources_none_or_null(rmi_b, terminal_unit_id_list)
        and are_all_terminal_fans_null(rmi_b, terminal_unit_id_list)
        and are_all_terminal_types_cav(rmi_b, terminal_unit_id_list)
    )

    if are_sys_data_matched:
        if is_hvac_sys_fluid_loop_attached_to_chiller(rmi_b, hvac_b_id):
            is_baseline_system_13 = HVAC_SYS.SYS_13
        elif is_hvac_sys_fluid_loop_purchased_chw(rmi_b, hvac_b_id):
            is_baseline_system_13 = HVAC_SYS.SYS_13A

    return is_baseline_system_13
