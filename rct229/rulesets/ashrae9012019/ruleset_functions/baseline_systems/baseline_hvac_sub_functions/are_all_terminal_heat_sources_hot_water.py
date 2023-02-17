from rct229.data.schema_enums import schema_enums
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    find_exactly_one_terminal_unit,
)

HEATING_SOURCE = schema_enums["HeatingSourceOptions"]


def are_all_terminal_heat_sources_hot_water(rmi_b, terminal_unit_id_list):
    """Returns TRUE if the heat source associated with all terminal units input to this function is HOT_WATER. It returns FALSE if any terminal unit has a heat source other than HOT_WATER.

    Parameters
    ----------
    rmi_b : json
        RMD at RuleSetModelInstance level
    terminal_unit_id_list : list
        List of terminal units IDs

    Returns
    -------
    bool
        True: the heat source associated with all terminal units input to this function is HOT_WATER
        False: any terminal unit has a heat source other than HOT_WATER.
    """
    are_all_terminal_heat_sources_hot_water_flag = True
    for terminal_b_id in terminal_unit_id_list:
        terminal_b = find_exactly_one_terminal_unit(rmi_b, terminal_b_id)
        if terminal_b.get("heating_source") != HEATING_SOURCE.HOT_WATER:
            are_all_terminal_heat_sources_hot_water_flag = False
            break

    return all(
        find_exactly_one_terminal_unit(rmi_b, terminal_b_id).get("heating_source")
        == HEATING_SOURCE.HOT_WATER
        for terminal_b_id in terminal_unit_id_list
    )
