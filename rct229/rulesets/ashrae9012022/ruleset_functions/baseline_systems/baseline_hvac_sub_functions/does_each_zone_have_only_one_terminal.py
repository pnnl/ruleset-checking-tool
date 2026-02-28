from rct229.utils.utility_functions import find_exactly_one_zone


def does_each_zone_have_only_one_terminal(rmd_b, zone_id_list):
    """Returns TRUE if each zone input to this function only has one terminal unit. It returns FALSE if any zone has more than one terminal unit.
    ----------
    rmd_b : json
        RMD at RuleSetModelDescription level
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
        zone = find_exactly_one_zone(rmd_b, zone_id)
        if zone.get("terminals") is None or len(zone["terminals"]) != 1:
            does_each_zone_have_only_one_terminal_flag = False
            break
    return does_each_zone_have_only_one_terminal_flag
