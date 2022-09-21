from rct229.data.schema_enums import schema_enums
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_cool_sources_none_or_null import (
    are_all_terminal_cool_sources_none_or_null,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_fans_null import (
    are_all_terminal_fans_null,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_heat_sources_hot_water import (
    are_all_terminal_heat_sources_hot_water,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_heating_loops_attached_to_boiler import (
    are_all_terminal_heating_loops_attached_to_boiler,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_heating_loops_purchased_heating import (
    are_all_terminal_heating_loops_purchased_heating,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_types_VAV import (
    are_all_terminal_types_VAV,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.does_each_zone_have_only_one_terminal import (
    does_each_zone_have_only_one_terminal,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_cooling_type_fluid_loop import (
    is_hvac_sys_cooling_type_fluid_loop,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_fan_sys_VSD import (
    is_hvac_sys_fan_sys_vsd,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_fluid_loop_attached_to_chiller import (
    is_hvac_sys_fluid_loop_attached_to_chiller,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_fluid_loop_purchased_CHW import (
    is_hvac_sys_fluid_loop_purchased_chw,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_preheat_fluid_loop_attached_to_boiler import (
    is_hvac_sys_preheat_fluid_loop_attached_to_boiler,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_preheat_fluid_loop_purchased_heating import (
    is_hvac_sys_preheat_fluid_loop_purchased_heating,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_preheating_type_fluid_loop import (
    is_hvac_sys_preheating_type_fluid_loop,
)
from rct229.ruleset_functions.baseline_systems.baseline_system_util import HVAC_SYS
from rct229.utils.jsonpath_utils import find_exactly_one_with_field_value, find_one

HEATING_SYSTEM = schema_enums["HeatingSystemOptions"]


def is_baseline_system_7(rmi_b, hvac_b_id, terminal_unit_id_list, zone_id_list):
    """
    Get either Sys-7, Sys-7a, Sys-7b, Sys-7c or Not_Sys_7 string output which indicates whether the HVAC system is
    ASHRAE 90.1 2019 Appendix G system 7 (VAV with Reheat), system 7a (system 7 with purchased CHW), system 7b (
    system 7 with purchased heating), or system 7c (system 7 with purchased heating and purchased CHW).

    Parameters
    ----------
    rmi_b: JSON, To evaluate if the hvac system is modeled as either Sys-7, Sys-7a, Sys-7b, Sys-7c or Not_Sys_7 in the B_RMR.
    hvac_b_id: String, The id of the hvac system to evaluate.
    terminal_unit_id_list: List<String>, list of terminal unit IDs associated with the HVAC system to be evaluated. These are
                            sent to this function from the master get_baseline_system_types function.
    zone_id_list: List<String>, list of zone IDs associated with the HVAC system to be evaluated. These are sent to this
                        function from the master get_baseline_system_types function.

    Returns: The function returns either Sys-7, Sys-7a, Sys-7b, Sys-7c or Not_Sys_7 string output which indicates
    whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 7 (VAV with Reheat), system 7a (system 7 with
    purchased CHW), system 7b (system 7 with purchased heating), pr system 7c (system 7 with purchased heating and
    purchased CHW). -------
    """
    is_baseline_system_7_str = HVAC_SYS.UNMATCHED

    # Get the hvac system
    hvac_b = find_exactly_one_with_field_value(
        "buildings[*].building_segments[*].heating_ventilation_air_conditioning_systems[*]",
        "id",
        hvac_b_id,
        rmi_b,
    )

    # check if the hvac system has the required sub systems for system type 7
    has_required_sys = (
        hvac_b.get("preheat_system") is not None
        and hvac_b.get("cooling_system") is not None
        and
        # heating system shall be None or heating system type shall be None (the heating_system_type =
        # HEATING_SYSTEM.NONE)
        (
            hvac_b.get("heating_system") is None
            or find_one(
                f'heating_system[?(@.heating_system_type="{HEATING_SYSTEM.NONE}")]',
                hvac_b,
            )
            is not None
        )
    )

    are_sys_data_matched = (
        # sub functions handles missing required sys, and return False.
        is_hvac_sys_preheating_type_fluid_loop(rmi_b, hvac_b_id)
        and is_hvac_sys_cooling_type_fluid_loop(rmi_b, hvac_b_id)
        and is_hvac_sys_fan_sys_vsd(rmi_b, hvac_b_id)
        and does_each_zone_have_only_one_terminal(rmi_b, zone_id_list)
        and are_all_terminal_heat_sources_hot_water(rmi_b, terminal_unit_id_list)
        and are_all_terminal_cool_sources_none_or_null(rmi_b, terminal_unit_id_list)
        and are_all_terminal_fans_null(rmi_b, terminal_unit_id_list)
        and are_all_terminal_types_VAV(rmi_b, terminal_unit_id_list)
    )

    if has_required_sys and are_sys_data_matched:
        # Confirm required data for Sys-7, now to decide which system type 7
        is_hvac_sys_fluid_loop_attached_to_chiller_flag = (
            is_hvac_sys_fluid_loop_attached_to_chiller(rmi_b, hvac_b_id)
        )
        is_hvac_sys_fluid_loop_purchased_chw_flag = (
            is_hvac_sys_fluid_loop_purchased_chw(rmi_b, hvac_b_id)
        )
        if is_hvac_sys_preheat_fluid_loop_attached_to_boiler(
            rmi_b, hvac_b_id
        ) and are_all_terminal_heating_loops_attached_to_boiler(
            rmi_b, terminal_unit_id_list
        ):
            if is_hvac_sys_fluid_loop_attached_to_chiller_flag:
                is_baseline_system_7_str = HVAC_SYS.SYS_7
            elif is_hvac_sys_fluid_loop_purchased_chw_flag:
                is_baseline_system_7_str = HVAC_SYS.SYS_7A
        elif is_hvac_sys_preheat_fluid_loop_purchased_heating(
            rmi_b, hvac_b_id
        ) and are_all_terminal_heating_loops_purchased_heating(
            rmi_b, terminal_unit_id_list
        ):
            if is_hvac_sys_fluid_loop_attached_to_chiller_flag:
                is_baseline_system_7_str = HVAC_SYS.SYS_7B
            elif is_hvac_sys_fluid_loop_purchased_chw_flag:
                is_baseline_system_7_str = HVAC_SYS.SYS_7C

    return is_baseline_system_7_str
