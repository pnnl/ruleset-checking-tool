from rct229.data.schema_enums import schema_enums
from rct229.utils.jsonpath_utils import find_exactly_one_with_field_value

TERMINAL_TYPE = schema_enums["TerminalOptions"]


def are_all_terminal_types_VAV(rmi_b, terminal_unit_id_list):
    """Returns TRUE if all of the terminal unit types input to this function are variable air volume (VAV). It returns FALSE if any of the terminal units are of a type other than variable air volume (VAV).

    Parameters
    ----------
    rmi_b : json
        RMD at RuleSetModelInstance level
    terminal_unit_id_list : list
        List of terminal units IDs

    Returns
    -------
    bool
        True: all of the terminal unit types input to this function are variable air volume (VAV)
        False: any of the terminal units are of a type other than variable air volume (VAV)
    """
    are_all_terminal_types_VAV_flag = True

    for terminal_b_id in terminal_unit_id_list:
        terminal_b = find_exactly_one_with_field_value(
            "$.buildings[*].building_segments[*].zones[*].terminals[*]",
            "id",
            terminal_b_id,
            rmi_b,
        )
        if terminal_b.get("type") != TERMINAL_TYPE.VARIABLE_AIR_VOLUME:
            are_all_terminal_types_VAV_flag = False
            break

    return are_all_terminal_types_VAV_flag
