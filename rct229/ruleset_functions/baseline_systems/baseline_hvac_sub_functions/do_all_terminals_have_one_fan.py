from rct229.ruleset_functions.baseline_systems.baseline_system_util import (
    find_exactly_one_terminal_unit,
)


def do_all_terminals_have_one_fan(rmi_b, terminal_unit_id_list):
    """Returns TRUE if the fan data element associated with all terminal units input to this function are equal to one (i.e., there is only one fan associated with the terminal unit). It returns FALSE if any terminal unit has a fan data element not equal to one (i.e., there is NOT only one fan associated with the terminal unit).

    Parameters
    ----------
    rmi_b: json
        RMD at RuleSetModelInstance level
    terminal_unit_id_list: list
        List of terminal_units IDs

    Returns
    -------
    bool
        True: the fan data element associated with all terminal units input to this function are equal to one (i.e., there is only one fan associated with the terminal unit).
        False: any terminal unit has a fan data element not equal to one (i.e., there is NOT only one fan associated with the terminal unit).
    """

    do_all_terminals_have_one_fan = True

    for terminal_b_id in terminal_unit_id_list:
        terminal_b = find_exactly_one_terminal_unit(rmi_b, terminal_b_id)
        if terminal_b.get("fan") == None:
            do_all_terminals_have_one_fan = False
            break

    return do_all_terminals_have_one_fan
