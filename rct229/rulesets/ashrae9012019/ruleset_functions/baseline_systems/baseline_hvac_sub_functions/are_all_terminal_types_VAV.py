from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.utility_functions import find_exactly_one_terminal_unit

TERMINAL_TYPE = SchemaEnums.schema_enums["TerminalOptions"]


def are_all_terminal_types_VAV(rmd: dict, terminal_unit_id_list: list[str]) -> bool:
    """It returns FALSE if no terminal unit in the list or any of the terminal units are of a type other than variable air volume (VAV) or null.

    Parameters
    ----------
    rmd : dict
        RMD at RuleSetModelDescription level
    terminal_unit_id_list : list
        List of terminal units IDs

    Returns
    -------
    bool
        True: all of the terminal unit types input to this function are variable air volume (VAV)
        False: any of the terminal units are of a type other than variable air volume (VAV)
    """

    return len(terminal_unit_id_list) > 0 and all(
        [
            find_exactly_one_terminal_unit(rmd, terminal_id).get("type")
            in [None, TERMINAL_TYPE.VARIABLE_AIR_VOLUME]
            for terminal_id in terminal_unit_id_list
        ]
    )
