from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.utility_functions import find_exactly_one_terminal_unit

COOLING_SOURCE = SchemaEnums.schema_enums["CoolingSourceOptions"]


def are_all_terminal_cool_sources_none_or_null(rmd_b, terminal_unit_id_list):
    """Returns TRUE if the cool source associated with all terminal units input to this function are None or Null. It returns FALSE if any terminal unit has a cool source other than None or Null.
    ----------
    rmd_b : json
        RMD at RuleSetModelDescription level
    terminal_unit_id_list : list
        List of terminal units IDs
    Returns
    -------
    bool
        True: the cool source associated with all terminal units input to this function are None or Null
        False: any terminal unit has a cool source other than None or Null
    """
    are_all_terminal_cool_sources_none_or_null_flag = True
    for terminal_b_id in terminal_unit_id_list:
        terminal_b = find_exactly_one_terminal_unit(rmd_b, terminal_b_id)
        if terminal_b.get("cooling_source") not in [None, COOLING_SOURCE.NONE]:
            are_all_terminal_cool_sources_none_or_null_flag = False
            break

    return are_all_terminal_cool_sources_none_or_null_flag
