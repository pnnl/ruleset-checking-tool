def does_hvac_system_serve_single_zone(rmd_b, zone_id_list):
    """Returns TRUE if the HVAC system serves a single zone. Returns FALSE if the HVAC system serves multiple zones.

    Parameters
    ----------
    rmd_b : json
        RMD at RuleSetModelDescription level
    zone_id_list : str
         list of zone IDs associated with the HVAC system to be evaluated

    Returns
    -------
    bool
        True: HVAC system serves a single zone
        False: HVAC system serves multiple zones
    """
    return len(zone_id_list) == 1
