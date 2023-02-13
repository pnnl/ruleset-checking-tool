from rct229.data.schema_enums import schema_enums
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_cool_sources_none_or_null import (
    are_all_terminal_cool_sources_none_or_null,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_fan_configs_parallel import (
    are_all_terminal_fan_configs_parallel,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_heat_sources_electric import (
    are_all_terminal_heat_sources_electric,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_heat_sources_hot_water import (
    are_all_terminal_heat_sources_hot_water,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_heating_loops_purchased_heating import (
    are_all_terminal_heating_loops_purchased_heating,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_types_VAV import (
    are_all_terminal_types_VAV,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.do_all_terminals_have_one_fan import (
    do_all_terminals_have_one_fan,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.does_each_zone_have_only_one_terminal import (
    does_each_zone_have_only_one_terminal,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_cooling_type_DX import (
    is_hvac_sys_cooling_type_dx,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_fan_sys_VSD import (
    is_hvac_sys_fan_sys_vsd,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_preheat_fluid_loop_purchased_heating import (
    is_hvac_sys_preheat_fluid_loop_purchased_heating,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_preheating_type_elec_resistance import (
    is_hvac_sys_preheating_type_elec_resistance,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_preheating_type_fluid_loop import (
    is_hvac_sys_preheating_type_fluid_loop,
)
from rct229.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
    has_cooling_system,
    has_heating_system,
    has_preheat_system,
)

HEATING_SYSTEM = schema_enums["HeatingSystemOptions"]
COOLING_SYSTEM = schema_enums["CoolingSystemOptions"]


def is_baseline_system_6(rmi_b, hvac_b_id, terminal_unit_id_list, zone_id_list):
    """
    Get either Sys-6, Sys-6b, or Not_Sys_6 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 6 (Package VAV with PFP Boxes) or system 6b (system 6 with purchased heating).

    Parameters
    ----------
    rmi_b json
         To evaluate if the hvac system is modeled as either Sys-6, Sys-6b, or Not_Sys_6 in the B_RMI.
     hvac_b_id list
         The id of the hvac system to evaluate.
     terminal_unit_id_list
         List list of terminal unit IDs associated with the HVAC system to be evaluated. These are sent to this function from the master get_baseline_system_types function.
     zone_id_list list
         list of zone IDs associated with the HVAC system to be evaluated. These are sent to this function from the master get_baseline_system_types function.

    Returns
    -------
    The function returns either Sys-6, Sys-6b, or Not_Sys_6 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 6 (Package VAV with PFP Boxes) or system 6b (system 6 with purchased heating).
    """

    is_baseline_system_6 = HVAC_SYS.UNMATCHED

    # check if the hvac system has the required sub systems for system type 6
    # if heating system DOESN'T exist and preheat/cooling systems exist, has_required_sys=True, else, False.
    has_required_sys = (
        has_preheat_system(rmi_b, hvac_b_id)
        and not has_heating_system(rmi_b, hvac_b_id)
        and has_cooling_system(rmi_b, hvac_b_id)
    )

    are_sys_data_matched = (
        # short-circuit the logic if no required data is found.
        has_required_sys
        # sub functions handles missing required sys, and return False.
        and is_hvac_sys_cooling_type_dx(rmi_b, hvac_b_id)
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
            is_baseline_system_6 = HVAC_SYS.SYS_6
        elif (
            is_hvac_sys_preheating_type_fluid_loop(rmi_b, hvac_b_id)
            and is_hvac_sys_preheat_fluid_loop_purchased_heating(rmi_b, hvac_b_id)
            and are_all_terminal_heat_sources_hot_water(rmi_b, terminal_unit_id_list)
            and are_all_terminal_heating_loops_purchased_heating(
                rmi_b, terminal_unit_id_list
            )
        ):
            is_baseline_system_6 = HVAC_SYS.SYS_6B

    return is_baseline_system_6
