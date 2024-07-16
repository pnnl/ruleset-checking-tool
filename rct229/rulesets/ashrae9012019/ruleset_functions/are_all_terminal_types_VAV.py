from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import assert_
from rct229.utils.utility_functions import find_exactly_one_terminal_unit

TERMINAL_TYPE = SchemaEnums.schema_enums["TerminalOptions"]


def are_all_terminal_types_VAV(rmd: dict, terminal_unit_id_list: list[str]) -> bool:
    """
    Returns TRUE if all of the terminal unit types input to this function are variable air volume (VAV) or are equal to null.
    It returns FALSE if any of the terminal units are of a type other than variable air volume (VAV) or null.

    Parameters
    ----------
    rmd: dict,
        To evaluate if the terminal unit types are variable air volume (VAV).
    terminal_unit_id_list: list[str],
        List of terminal units to assess.

    Returns bool,
        The function returns TRUE if all of the terminal unit types input to this function are variable air volume (VAV) or are equal to null.
        It returns FALSE if any of the terminal units are of a type other than variable air volume (VAV) or null.
    """

    # check `terminal_unit_id_list` type
    assert_(
        isinstance(terminal_unit_id_list, list)
        and all(
            isinstance(terminal_unit_id, str)
            for terminal_unit_id in terminal_unit_id_list
        ),
        "Please make sure the `terminal_unit_id_list` type is list and has list of strings",
    )

    return all(
        [
            find_exactly_one_terminal_unit(rmd, terminal_id).get("type") is None
            or find_exactly_one_terminal_unit(rmd, terminal_id).get("type")
            == TERMINAL_TYPE.VARIABLE_AIR_VOLUME
            for terminal_id in terminal_unit_id_list
        ]
    )
