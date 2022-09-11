from rct229.utils.jsonpath_utils import find_exactly_one_with_field_value


def are_all_terminal_fans_null(rmi_b, terminal_unit_id_list):
    """Returns TRUE if the fan data element associated with all terminal units input to this function are equal to Null. It returns FALSE if any terminal unit has a fan data element not equal to Null.
    ----------
    rmi_b : json
        RMD at RuleSetModelInstance level
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
        terminal_b = find_exactly_one_with_field_value(
            "$.buildings[*].building_segments[*].zones[*].terminals",
            "id",
            terminal_b_id,
            rmi_b,
        )
        if terminal_b.get("fan") is not None:
            are_all_terminal_fans_null_flag = False
            break

    return are_all_terminal_fans_null_flag
