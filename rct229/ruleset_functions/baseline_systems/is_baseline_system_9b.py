from rct229.data.schema_enums import schema_enums
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_heat_sources_hot_water import (
    are_all_terminal_heat_sources_hot_water,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_heating_loops_purchased_heating import (
    are_all_terminal_heating_loops_purchased_heating,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.are_all_terminal_types_CAV_with_none_equal_to_null import (
    are_all_terminal_types_cav_with_none_equal_to_null,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.do_all_terminals_have_one_fan import (
    do_all_terminals_have_one_fan,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.does_each_zone_have_only_one_terminal import (
    does_each_zone_have_only_one_terminal,
)
from rct229.ruleset_functions.baseline_systems.baseline_hvac_sub_functions.is_hvac_sys_cooling_type_none import (
    is_hvac_sys_cooling_type_none,
)
from rct229.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
    find_exactly_one_hvac_system,
)

HEATING_SYSTEM = schema_enums["HeatingSystemOptions"]


def is_baseline_system_9b(rmi_b, hvac_b_id, terminal_unit_id_list, zone_id_list):
    """
    Returns true or false to whether the baseline system type is 9b (system 9 with purchased HW).

    Parameters
     ----------
     rmi_b json
         To evaluate if the hvac system is modeled as either Sys-9bin the B_RMI.
     hvac_b_id list
         The id of the hvac system to evaluate.
     terminal_unit_id_list
         List list of terminal unit IDs associated with the HVAC system to be evaluated. These are sent to this function from the master get_baseline_system_types function.
     zone_id_list list
         list of zone IDs associated with the HVAC system to be evaluated. These are sent to this function from the master get_baseline_system_types function.

    Returns
     -------
     Returns true or false to whether the baseline system type is 9b (system 9 with purchased HW).
    """

    is_baseline_system_9b = HVAC_SYS.UNMATCHED

    # Get the hvac system
    hvac_b = find_exactly_one_hvac_system(rmi_b, hvac_b_id)

    preheat_system = hvac_b.get("preheat_system")
    has_required_preheat_sys = (
        preheat_system is None
        or preheat_system.get("heating_system_type") is None
        or preheat_system["heating_system_type"] == HEATING_SYSTEM.NONE
    )

    heating_system = hvac_b.get("heating_system")
    has_required_heating_sys = (
        heating_system is None
        or heating_system.get("heating_system_type") is None
        or heating_system["heating_system_type"] == HEATING_SYSTEM.NONE
    )

    has_required_fan_sys = hvac_b.get("fan_system") is None

    return (
        has_required_preheat_sys
        and has_required_heating_sys
        and has_required_fan_sys
        # sub functions handles missing required sys, and return False.
        and is_hvac_sys_cooling_type_none(rmi_b, hvac_b_id)
        and does_each_zone_have_only_one_terminal(rmi_b, zone_id_list)
        and are_all_terminal_heat_sources_hot_water(rmi_b, terminal_unit_id_list)
        and do_all_terminals_have_one_fan(rmi_b, terminal_unit_id_list)
        and are_all_terminal_types_cav_with_none_equal_to_null(
            rmi_b, terminal_unit_id_list
        )
        and are_all_terminal_heating_loops_purchased_heating(
            rmi_b, terminal_unit_id_list
        )
    )
