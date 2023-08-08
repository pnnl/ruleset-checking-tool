from rct229.rulesets.ashrae9012019.data.schema_enums import schema_enums
from rct229.utils.utility_functions import find_exactly_one_terminal_unit

TERMINAL_TYPE = schema_enums["TerminalOptions"]


def are_all_terminal_types_cav_with_none_equal_to_null(rmi_b, terminal_unit_id_list):
    """Returns TRUE if all of the terminal unit types input to this function are constant air volume (CAV).
    It returns FALSE if any of the terminal units are of a type other than constant air volume (CAV).

        Parameters
        ----------
        rmi_b : json
            RMD at RuleSetModelInstance level
        terminal_unit_id_list : list
            List of terminal units IDs

        Returns
        -------
        bool
            True: all of the terminal unit types input to this function are constant air volume (CAV) (null or missing is false)
            False: any of the terminal units are of a type other than constant air volume (CAV).
    """

    return all(
        find_exactly_one_terminal_unit(rmi_b, terminal_b_id).get("type")
        == TERMINAL_TYPE.CONSTANT_AIR_VOLUME
        for terminal_b_id in terminal_unit_id_list
    )
