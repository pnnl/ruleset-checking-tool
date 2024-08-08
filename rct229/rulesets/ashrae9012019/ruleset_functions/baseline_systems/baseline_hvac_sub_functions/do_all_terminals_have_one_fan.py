from rct229.utils.utility_functions import find_exactly_one_terminal_unit


def do_all_terminals_have_one_fan(rmd_b, terminal_unit_id_list):
    """Returns TRUE if a fan data element associated with all terminal units input to this function.
     It returns FALSE if any terminal unit has no fan data element not equal to one.

    ----------
    rmd_b : json
        RMD at RuleSetModelDescription level
    terminal_unit_id_list : list
        List of terminal units IDs
    Returns
    -------
    bool
        True: there is a fan data element associated with all terminal units input to this function.
        False: any terminal unit a no fan data.
    """

    return all(
        [
            find_exactly_one_terminal_unit(rmd_b, terminal_b_id).get("fan") is not None
            for terminal_b_id in terminal_unit_id_list
        ]
    )
