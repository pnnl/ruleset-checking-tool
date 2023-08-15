def does_zone_meet_G3_1_1c(rmi, zone_id):
    """
    Determines whether a given zone meets the G3_1_1c exception "If the baseline HVAC system type is 5, 6, 7,
    8 use separate single-zone systems conforming with the requirements of system 3 or system 4 (depending on
    building heating source) for any spaces that have occupancy or process loads or schedules that differ
    significantly from the rest of the building. Peak thermal loads that differ by 10 Btu/h·ft2 (2.930710 W/sf) or
    more from the average of other spaces served by the system, or schedules that differ by more than 40 equivalent
    full-load hours per week from other spaces served by the system, are considered to differ significantly. Examples
    where this exception may be applicable include but are not limited to natatoriums and continually occupied
    security areas. This exception does not apply to computer rooms.

    Parameters
    ----------
    rmi dict
        A dictionary representing a ruleset model instance as defined by the ASHRAE229 schema
    zone_id str
        zone id

    Returns
    -------
    boolean, true or false
    """
