from rct229.data.schema_enums import schema_enums
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    find_exactly_one_terminal_unit,
)

TERMINAL_FAN_CONFIGURATION = schema_enums["TerminalFanConfigurationOptions"]


def are_all_terminal_fan_configs_parallel(rmi_b, terminal_unit_id_list):
    """Returns TRUE if the fan configuration associated with all terminal units input to this function are parallel.
    It returns FALSE if any terminal unit has a fan configuration other than parallel.

    ----------
    rmi_b : json
        RMD at RuleSetModelInstance level
    terminal_unit_id_list : list
        List of terminal units IDs
    Returns
    -------
    bool
        True: fan configuration associated with all terminal units input to this function are parallel
        False: any terminal unit has a fan configuration other than parallel
    """
    # all terminal's fan configuration should be parallel, and false otherwise.
    return all(
        find_exactly_one_terminal_unit(rmi_b, terminal_b_id).get("fan_configuration")
        == TERMINAL_FAN_CONFIGURATION.PARALLEL
        for terminal_b_id in terminal_unit_id_list
    )
