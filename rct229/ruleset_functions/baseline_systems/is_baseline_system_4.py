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
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_supplies_ducted import (
    are_all_terminal_supplies_ducted,
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
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_heating_type_heat_pump import (
    is_hvac_sys_heating_type_heat_pump,
)
from rct229.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
    find_exactly_one_hvac_system,
)

HEATING_SYSTEM = schema_enums["HeatingSystemOptions"]


def is_baseline_system_4(rmi_b, hvac_b_id, terminal_unit_id_list, zone_id_list):

    is_baseline_system_4 = HVAC_SYS.UNMATCHED

    # Get the hvac system
    hvac_b = find_exactly_one_hvac_system(rmi_b, hvac_b_id)

    # check if the hvac system has the required sub systems for system type 11.1
    has_required_sys = (
        hvac_b.get("preheat_system") is None
        or hvac_b["preheat_system"].get("heating_system_type") is None
        or hvac_b["preheat_system"]["heating_system_type"] == HEATING_SYSTEM.NONE
    )

    are_sys_data_matched = (
        # short-circuit the logic if no required data is found.
        has_required_sys
        # sub functions handles missing required sys, and return False.
        and is_hvac_sys_heating_type_heat_pump(rmi_b, hvac_b_id)
        and is_hvac_sys_cooling_type_dx(rmi_b, hvac_b_id)
        and is_hvac_sys_fan_sys_cv(rmi_b, hvac_b_id)
        and does_hvac_system_serve_single_zone(rmi_b, zone_id_list)
        and does_each_zone_have_only_one_terminal(rmi_b, zone_id_list)
        and are_all_terminal_heat_sources_none_or_null(rmi_b, terminal_unit_id_list)
        and are_all_terminal_cool_sources_none_or_null(rmi_b, terminal_unit_id_list)
        and are_all_terminal_fans_null(rmi_b, terminal_unit_id_list)
        and are_all_terminal_supplies_ducted(rmi_b, terminal_unit_id_list)
        and are_all_terminal_types_cav(rmi_b, terminal_unit_id_list)
    )

    if are_sys_data_matched:
        is_baseline_system_4 = HVAC_SYS.SYS_4

    return is_baseline_system_4
