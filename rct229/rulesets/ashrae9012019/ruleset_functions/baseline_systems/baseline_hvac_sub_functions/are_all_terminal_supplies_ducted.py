from rct229.utils.utility_functions import find_exactly_one_terminal_unit


def are_all_terminal_supplies_ducted(rmd_b, terminal_unit_id_list):
    """Returns TRUE if all of the terminal supplies are ducted (i.e., is_supply_ducted = TRUE) for the list of
    terminal units input to the function. It returns FALSE if any of the terminal supplies are not ducted (i.e.,
    is_supply_ducted = FALSE).

        Parameters
        ----------
        rmd_b : json
            RMD at RuleSetModelDescription level
        terminal_unit_id_list : list
            List of terminal units IDs

        Returns
        -------
        bool
            True: all of the terminal supplies are ducted (i.e., is_supply_ducted = TRUE) for the list of terminal units input to the function
            False: any of the terminal supplies are not ducted (i.e., is_supply_ducted = FALSE)
    """
    are_all_terminal_supplies_ducted_flag = True
    for terminal_b_id in terminal_unit_id_list:
        terminal_b = find_exactly_one_terminal_unit(rmd_b, terminal_b_id)
        # Set flag to False if is_suppy_ducted is False or is missing
        if not terminal_b.get("is_supply_ducted"):
            are_all_terminal_supplies_ducted_flag = False
            break

    return are_all_terminal_supplies_ducted_flag
