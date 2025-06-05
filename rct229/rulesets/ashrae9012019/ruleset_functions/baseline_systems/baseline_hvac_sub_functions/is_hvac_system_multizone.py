def is_hvac_system_multizone(rmd_b, zone_id_list):
    """
    Returns TRUE if the HVAC system serves multiple zones. Returns FALSE if the HVAC system serves a single or no zones.

    Parameters
    ----------
    rmd_b: json
    zone_id_list: list[string] zone ids

    Returns
    -------
    bool
        True: HVAC system serves a multiple zones.
        False: HVAC system serves zero or one zone.
    """
    return len(zone_id_list) > 1
