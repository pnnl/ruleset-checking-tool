from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import find_exactly_one_zone


def does_zone_meet_g_3_1_1f(rmi, zone_id):
    """
    Determines whether a given zone meets the G3_1_1f exception "If the baseline HVAC system type is 9 or 10,
    use additional system types for all HVAC zones that are mechanically cooled in the proposed design." - this
    function is only called if the expected baseline system type has already been confirmed to be system type 9 or 10

    Parameters
    ----------
    rmi dict
        A dictionary representing a ruleset model instance as defined by the ASHRAE229 schema
    zone_id str
        zone id

    Returns
    -------
    Boolean True meet False otherwise
    """
    zone_p = find_exactly_one_zone(rmi, zone_id)
    return False