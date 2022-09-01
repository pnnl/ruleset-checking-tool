def is_hvac_sys_heating_type_fluid_loop(rmi_b, hvac_b_id):
    """Returns TRUE if the HVAC system heating system heating type is fluid loop. Returns FALSE if the HVAC system
    heating system has anything other than fluid loop or if it has more than 1 heating system.

    Parameters
    ----------
    rmi_b : json
        RMD at RuleSetModelInstance level
    hvac_b_id : str
        The HVAC system ID.

    Returns
    -------
    bool
        True: HVAC system heating system has fluid loop as the heating type AND only one heating system is associated with the HVAC system
        False: HVAC system has a heating system type other than fluid loop or if it has more than one heating system.
    """
    is_hvac_sys_heating_type_fluid_loop_flag = False
