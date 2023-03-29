from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    find_exactly_one_zone,
)


def does_each_zone_have_only_one_terminal(rmi_b, zone_id_list):
    """Returns TRUE if each zone input to this function only has one terminal unit. It returns FALSE if any zone has more than one terminal unit.
    ----------
    rmi_b : json
        RMD at RuleSetModelInstance level
    zone_id_list : list
        List of zones to evaluate.
    Returns
    -------
    bool
        True: each zone input to this function only has one terminal unit or no terminal
        False: any zone has more than one terminal
    """
    does_each_zone_have_only_one_terminal_flag = True
    for zone_id in zone_id_list:
        zone = find_exactly_one_zone(rmi_b, zone_id)
        if zone.get("terminals") is None or len(zone["terminals"]) != 1:
            does_each_zone_have_only_one_terminal_flag = False
            break
    return does_each_zone_have_only_one_terminal_flag
