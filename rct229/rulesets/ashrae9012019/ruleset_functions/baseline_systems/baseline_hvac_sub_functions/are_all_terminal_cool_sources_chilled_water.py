from rct229.schema.schema_enums import schema_enums
from rct229.utils.utility_functions import find_exactly_one_terminal_unit

COOLING_SOURCE = schema_enums["CoolingSourceOptions"]


def are_all_terminal_cool_sources_chilled_water(rmi_b, terminal_unit_id_list):
    """Returns TRUE if the cool source associated with all terminal units is CHILLED_WATER. It returns FALSE if any terminal unit has a cool source other than CHILLED_WATER.
    ----------
    rmi_b : json
        RMD at RuleSetModelInstance level
    terminal_unit_id_list : list
        List of terminal units IDs
    Returns
    -------
    bool
        True: cool source associated with all terminal units sent to this function is CHILLED_WATER
        False: any terminal unit has a cool source other than CHILLED_WATER
    """
    # all terminal cool sources should be chilled water, false otherwise
    return all(
        find_exactly_one_terminal_unit(rmi_b, terminal_b_id).get("cooling_source")
        == COOLING_SOURCE.CHILLED_WATER
        for terminal_b_id in terminal_unit_id_list
    )
