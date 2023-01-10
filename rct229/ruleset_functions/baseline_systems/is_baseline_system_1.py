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
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_cooling_type_DX import (
    is_hvac_sys_cooling_type_dx,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_fan_sys_CV import (
    is_hvac_sys_fan_sys_cv,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_fluid_loop_attached_to_boiler import (
    is_hvac_sys_fluid_loop_attached_to_boiler,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_fluid_loop_purchased_heating import (
    is_hvac_sys_fluid_loop_purchased_heating,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_heating_type_fluid_loop import (
    is_hvac_sys_heating_type_fluid_loop,
)
from rct229.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
    has_preheat_system,
)
from rct229.ruleset_functions.baseline_systems.is_baseline_system_1_a import (
    is_baseline_system_1_a,
)
from rct229.ruleset_functions.baseline_systems.is_baseline_system_1_c import (
    is_baseline_system_1_c,
)

HEATING_SYSTEM = schema_enums["HeatingSystemOptions"]


def is_baseline_system_1(rmi_b, hvac_b_id, terminal_unit_id_list, zone_id_list):
    """
    Get either Sys-1, Sys-1a, Sys-1b, Sys-1c, or Not_Sys_1 string output which indicates whether the HVAC system is
    ASHRAE 90.1 2019 Appendix G system 1 (PTAC), system 1a (system 1 with purchased CHW), system 1b (system 1 with
    purchased heating), system 1c (system 1 with purchased CHW and purchased HW).

    Parameters
    ----------
    rmi_b JSON, To evaluate if the hvac system is modeled as either Sys-1, Sys-1a, Sys-1b, Sys-1c, or Not_Sys_1 in the B_RMD.
    hvac_b_id String, The id of the hvac system to evaluate.
    terminal_unit_id_list List<String>, list of terminal unit IDs associated with the HVAC system to be evaluated. These are
                            sent to this function from the master get_baseline_system_types function.
    zone_id_list  List<String>, list of zone IDs associated with the HVAC system to be evaluated. These are sent to this
                        function from the master get_baseline_system_types function.

    Returns The function returns either Sys-1, Sys-1a, Sys-1b, Sys-1c, or Not_Sys_1 string output which indicates
    whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 1 (PTAC), system 1a (system 1 with purchased CHW),
    system 1b (system 1 with purchased heating), system 1c (system 1 with purchased CHW and purchased HW). -------

    """

    is_baseline_system_1_str = HVAC_SYS.UNMATCHED
    # Get the hvac system

    if is_baseline_system_1_c(rmi_b, hvac_b_id, terminal_unit_id_list, zone_id_list):
        is_baseline_system_1_str = HVAC_SYS.SYS_1C
    elif is_baseline_system_1_a(rmi_b, hvac_b_id, terminal_unit_id_list, zone_id_list):
        is_baseline_system_1_str = HVAC_SYS.SYS_1A
    else:
        # check if the hvac system has the required sub systems for system type 1
        has_required_sys = not has_preheat_system(rmi_b, hvac_b_id)

        are_sys_data_matched = (
            has_required_sys
            # sub functions handles missing required sys, and return False.
            and is_hvac_sys_heating_type_fluid_loop(rmi_b, hvac_b_id)
            and is_hvac_sys_fan_sys_cv(rmi_b, hvac_b_id)
            and does_hvac_system_serve_single_zone(rmi_b, zone_id_list)
            and does_each_zone_have_only_one_terminal(rmi_b, zone_id_list)
            and are_all_terminal_heat_sources_none_or_null(rmi_b, terminal_unit_id_list)
            and are_all_terminal_cool_sources_none_or_null(rmi_b, terminal_unit_id_list)
            and are_all_terminal_fans_null(rmi_b, terminal_unit_id_list)
            and are_all_terminal_types_cav(rmi_b, terminal_unit_id_list)
            and is_hvac_sys_cooling_type_dx(rmi_b, hvac_b_id)
        )
        if are_sys_data_matched:
            if is_hvac_sys_fluid_loop_attached_to_boiler(rmi_b, hvac_b_id):
                is_baseline_system_1_str = HVAC_SYS.SYS_1
            elif is_hvac_sys_fluid_loop_purchased_heating(rmi_b, hvac_b_id):
                is_baseline_system_1_str = HVAC_SYS.SYS_1B
    return is_baseline_system_1_str
