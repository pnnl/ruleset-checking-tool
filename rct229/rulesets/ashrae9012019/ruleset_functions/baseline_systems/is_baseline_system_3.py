from rct229.schema.schema_enums import SchemaEnums
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_cool_sources_none_or_null import (
    are_all_terminal_cool_sources_none_or_null,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_fans_null import (
    are_all_terminal_fans_null,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_heat_sources_none_or_null import (
    are_all_terminal_heat_sources_none_or_null,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_supplies_ducted import (
    are_all_terminal_supplies_ducted,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_types_CAV import (
    are_all_terminal_types_cav,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.does_each_zone_have_only_one_terminal import (
    does_each_zone_have_only_one_terminal,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.does_hvac_system_serve_single_zone import (
    does_hvac_system_serve_single_zone,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_cooling_type_DX import (
    is_hvac_sys_cooling_type_dx,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_cooling_type_fluid_loop import (
    is_hvac_sys_cooling_type_fluid_loop,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_fan_sys_CV import (
    is_hvac_sys_fan_sys_cv,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_fluid_loop_purchased_CHW import (
    is_hvac_sys_fluid_loop_purchased_chw,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_fluid_loop_purchased_heating import (
    is_hvac_sys_fluid_loop_purchased_heating,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_heating_type_fluid_loop import (
    is_hvac_sys_heating_type_fluid_loop,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_heating_type_furnace import (
    is_hvac_sys_heating_type_furnace,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.utils.utility_functions import has_preheat_system

HEATING_SYSTEM = SchemaEnums.schema_enums["HeatingSystemOptions"]


def is_baseline_system_3(rmi_b, hvac_b_id, terminal_unit_id_list, zone_id_list):
    """
    Get either Sys-3, Sys-3a, Sys-3b, Sys-3c, or Not_Sys_3 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 3 (PSZ), system 3a (system 3 with purchased CHW),
    system 3b (system 3 with purchased heating), system 3c (system 3 with purchased CHW and purchased HW).

    Parameters
    ----------
    rmi_b json
        To evaluate if the hvac system is modeled as either Sys-3, Sys-3a, Sys-3b, Sys-3c, or Not_Sys_3 in the B_RMI.

    hvac_b_id list
        The id of the hvac system to evaluate.

    terminal_unit_id_list
        List list of terminal unit IDs associated with the HVAC system to be evaluated. These are sent to this function from the master get_baseline_system_types function.

    zone_id_list list
        list of zone IDs associated with the HVAC system to be evaluated. These are sent to this function from the master get_baseline_system_types function.

    Returns
    -------
    The function returns either Sys-3, Sys-3a, Sys-3b, Sys-3c, or Not_Sys_3 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 3 (PSZ),
    system 3a (system 3 with purchased CHW), system 3b (system 3 with purchased heating), system 3c (system 3 with purchased CHW and purchased HW).
    """
    is_baseline_system_3 = HVAC_SYS.UNMATCHED

    # check if the hvac system has the required sub systems for system type 3
    # if preheat DOESN'T exist, has_required_sys=True, else, False
    has_required_sys = not has_preheat_system(rmi_b, hvac_b_id)

    are_sys_data_matched = (
        # short-circuit the logic if no required data is found.
        has_required_sys
        # sub functions handles missing required sys, and return False.
        and is_hvac_sys_fan_sys_cv(rmi_b, hvac_b_id)
        and does_hvac_system_serve_single_zone(rmi_b, zone_id_list)
        and does_each_zone_have_only_one_terminal(rmi_b, zone_id_list)
        and are_all_terminal_heat_sources_none_or_null(rmi_b, terminal_unit_id_list)
        and are_all_terminal_cool_sources_none_or_null(rmi_b, terminal_unit_id_list)
        and are_all_terminal_fans_null(rmi_b, terminal_unit_id_list)
        and are_all_terminal_types_cav(rmi_b, terminal_unit_id_list)
        and are_all_terminal_supplies_ducted(rmi_b, terminal_unit_id_list)
    )

    if are_sys_data_matched:
        if is_hvac_sys_cooling_type_dx(rmi_b, hvac_b_id):
            if is_hvac_sys_heating_type_furnace(rmi_b, hvac_b_id):
                is_baseline_system_3 = HVAC_SYS.SYS_3
            elif is_hvac_sys_heating_type_fluid_loop(
                rmi_b, hvac_b_id
            ) and is_hvac_sys_fluid_loop_purchased_heating(rmi_b, hvac_b_id):
                is_baseline_system_3 = HVAC_SYS.SYS_3B
        elif is_hvac_sys_cooling_type_fluid_loop(
            rmi_b, hvac_b_id
        ) and is_hvac_sys_fluid_loop_purchased_chw(rmi_b, hvac_b_id):
            if is_hvac_sys_heating_type_furnace(rmi_b, hvac_b_id):
                is_baseline_system_3 = HVAC_SYS.SYS_3A
            elif is_hvac_sys_fluid_loop_purchased_heating(rmi_b, hvac_b_id):
                is_baseline_system_3 = HVAC_SYS.SYS_3C

    return is_baseline_system_3
