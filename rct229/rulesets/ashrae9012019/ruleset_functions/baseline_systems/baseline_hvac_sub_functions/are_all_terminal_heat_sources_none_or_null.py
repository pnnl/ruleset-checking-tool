from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.utility_functions import find_exactly_one_terminal_unit

HEATING_SOURCE = SchemaEnums.schema_enums["HeatingSourceOptions"]


def are_all_terminal_heat_sources_none_or_null(rmd_b, terminal_unit_id_list):
    """Returns TRUE if the heat source associated with all terminal units input to this function are None or Null. It returns FALSE if any terminal unit has a heat source other than None or Null.

    Parameters
    ----------
    rmd_b : json
        RMD at RuleSetModelDescription level
    terminal_unit_id_list : list
        List of terminal units IDs

    Returns
    -------
    bool
        True: the heat source associated with all terminal units input to this function are None or Null
        False: any terminal unit has a heat source other than None or Null
    """
    are_all_terminal_heat_sources_none_or_null_flag = True
    for terminal_b_id in terminal_unit_id_list:
        terminal_b = find_exactly_one_terminal_unit(rmd_b, terminal_b_id)
        if terminal_b.get("heating_source") not in [None, HEATING_SOURCE.NONE]:
            are_all_terminal_heat_sources_none_or_null_flag = False
            break

    return are_all_terminal_heat_sources_none_or_null_flag
