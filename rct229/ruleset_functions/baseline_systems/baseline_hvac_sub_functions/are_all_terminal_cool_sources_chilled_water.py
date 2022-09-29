from rct229.data.schema_enums import schema_enums
from rct229.ruleset_functions.baseline_systems.baseline_system_util import (
    find_exact_one_terminal_unit,
)

COOLING_SOURCE = schema_enums["CoolingSourceOptions"]


def are_all_terminal_cool_sources_chilled_water(rmi_b, terminal_unit_id_list):
    """Returns TRUE if the cool source associated with all terminal units is CHILLED_WATER. It returns FALSE if any terminal unit has a cool source other than CHILLED_WATER.
    ----------
    rmi_b : json
        RMD at RuleSetModelInstance level
    terminal_unit_id_list : list
        List of terminal units IDs
    Returns
    -------
    bool
        True: cool source associated with all terminal units sent to this function is CHILLED_WATER
        False: any terminal unit has a cool source other than CHILLED_WATER
    """
    are_all_terminal_cool_sources_chilled_water_flag = True
    for terminal_b_id in terminal_unit_id_list:
        terminal_b = find_exact_one_terminal_unit(rmi_b, terminal_b_id)
        if terminal_b.get("cooling_source") != COOLING_SOURCE.CHILLED_WATER:
            are_all_terminal_cool_sources_chilled_water_flag = False
            break

    return are_all_terminal_cool_sources_chilled_water_flag
