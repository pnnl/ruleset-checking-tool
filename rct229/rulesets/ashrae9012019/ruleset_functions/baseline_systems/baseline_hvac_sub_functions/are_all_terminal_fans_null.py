from rct229.utils.utility_functions import find_exactly_one_terminal_unit


def are_all_terminal_fans_null(rmd_b, terminal_unit_id_list):
    """Returns TRUE if the fan data element associated with all terminal units input to this function are equal to Null. It returns FALSE if any terminal unit has a fan data element not equal to Null.
    ----------
    rmd_b : json
        RMD at RuleSetModelDescription level
    terminal_unit_id_list : list
        List of terminal units IDs
    Returns
    -------
    bool
        True: fan data element associated with all terminal units input to this function are equal to Null
        False: any terminal unit has a fan data element not equal to Null.
    """
    are_all_terminal_fans_null_flag = True
    for terminal_b_id in terminal_unit_id_list:
        terminal_b = find_exactly_one_terminal_unit(rmd_b, terminal_b_id)
        if terminal_b.get("fan") is not None:
            are_all_terminal_fans_null_flag = False
            break

    return are_all_terminal_fans_null_flag
