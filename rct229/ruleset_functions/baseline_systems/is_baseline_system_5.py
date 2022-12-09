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
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_cooling_type_DX import (
    is_hvac_sys_cooling_type_dx,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_fan_sys_VSD import (
    is_hvac_sys_fan_sys_vsd,
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
from rct229.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
    find_exactly_one_hvac_system,
)

HEATING_SYSTEM = schema_enums["HeatingSystemOptions"]
COOLING_SYSTEM = schema_enums["CoolingSystemOptions"]


def is_baseline_system_5(rmi_b, hvac_b_id, terminal_unit_id_list, zone_id_list):

    is_baseline_system_5 = HVAC_SYS.UNMATCHED

    hvac_b = find_exactly_one_hvac_system(rmi_b, hvac_b_id)
    # check if the hvac system has the required sub systems for system type 11.1
    has_required_heating_sys = (
        hvac_b.get("heating_system") is None
        or hvac_b["heating_system"].get("heating_system_type") is None
        or hvac_b["heating_system"]["heating_system_type"] == HEATING_SYSTEM.NONE
    )

    has_required_preheat_sys = (
        hvac_b.get("preheat_system")
        is not None  # if preheat system exists, the number must be 1.
    )

    has_required_cooling_sys = (
        hvac_b.get("cooling_system") is not None
        or hvac_b["cooling_system"].get("cooling_system_type") is not None
        or hvac_b["cooling_system"]["cooling_system_type"] != COOLING_SYSTEM.NONE
    )

    are_sys_data_matched = (
        # short-circuit the logic if no required data is found.
        has_required_heating_sys
        and has_required_preheat_sys
        and has_required_cooling_sys
        # sub functions handles missing required sys, and return False.
        and is_hvac_sys_preheating_type_fluid_loop(rmi_b, hvac_b_id)
        and is_hvac_sys_cooling_type_dx(rmi_b, hvac_b_id)
        and is_hvac_sys_fan_sys_vsd(rmi_b, hvac_b_id)
        and does_each_zone_have_only_one_terminal(rmi_b, zone_id_list)
        and are_all_terminal_heat_sources_hot_water(rmi_b, terminal_unit_id_list)
        and are_all_terminal_cool_sources_none_or_null(rmi_b, terminal_unit_id_list)
        and are_all_terminal_fans_null(rmi_b, terminal_unit_id_list)
        and are_all_terminal_types_VAV(rmi_b, terminal_unit_id_list)
    )
    if are_sys_data_matched:
        if is_hvac_sys_preheat_fluid_loop_attached_to_boiler(
            rmi_b, hvac_b_id
        ) and are_all_terminal_heating_loops_attached_to_boiler(
            rmi_b, terminal_unit_id_list
        ):
            is_baseline_system_5 = HVAC_SYS.SYS_5
        elif is_hvac_sys_preheat_fluid_loop_purchased_heating(
            rmi_b, hvac_b_id
        ) and are_all_terminal_heating_loops_purchased_heating(
            rmi_b, terminal_unit_id_list
        ):
            is_baseline_system_5 = HVAC_SYS.SYS_5B

    return is_baseline_system_5
