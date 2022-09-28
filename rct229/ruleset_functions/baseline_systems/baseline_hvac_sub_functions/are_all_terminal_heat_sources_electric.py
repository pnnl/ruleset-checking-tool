from rct229.data.schema_enums import schema_enums
from rct229.ruleset_functions.baseline_systems.baseline_system_util import (
    find_exact_one_terminal_unit,
)

HEATING_SOURCE = schema_enums["HeatingSourceOptions"]


def are_all_terminal_heat_sources_electric(rmi_b, terminal_unit_id_list):
    """Returns TRUE if the heat source associated with all terminal units input to this function are electric. It
    returns FALSE if any terminal unit has a heat source other than electric.

    Parameters
    ----------
    rmi_b : json
        RMD at RuleSetModelInstance level
    terminal_unit_id_list : list
        List of terminal units IDs

    Returns
    -------
    bool
        True: heat source associated with all terminal units input to this function are electric
        False: any terminal unit has a heat source other than electric
    """
    are_all_terminal_heat_sources_electric_flag = True
    for terminal_b_id in terminal_unit_id_list:
        terminal_b = find_exact_one_terminal_unit(rmi_b, terminal_b_id)
        if terminal_b.get("heating_source") != HEATING_SOURCE.ELECTRIC:
            are_all_terminal_heat_sources_electric_flag = False
            break

    return are_all_terminal_heat_sources_electric_flag
