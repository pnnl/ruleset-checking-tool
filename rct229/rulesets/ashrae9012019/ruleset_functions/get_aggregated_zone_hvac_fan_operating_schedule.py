from typing import Optional

import pandas as pd
from rct229.rule_engine.rulesets import LeapYear
from rct229.rulesets.ashrae9012019.ruleset_functions.get_list_hvac_systems_associated_with_zone import (
    get_list_hvac_systems_associated_with_zone,
)
from rct229.utils.assertions import assert_, getattr_
from rct229.utils.jsonpath_utils import find_one
from rct229.utils.utility_functions import find_exactly_one_hvac_system


def get_aggregated_zone_hvac_fan_operating_schedule(
    rmd: dict, zone_id: str, is_leap_year: Optional[bool] = False
) -> list:
    """
     This function loops through all of the HVAC system fan operating schedules associated with a specific zone and
     creates an aggregated fan operating schedule for the zone. More specifically, if any of the fan operating schedules
     associated with any of the hvac systems serving the zone have a 1 for a particular hour of the year then the aggregated schedule will equal 1
     for that particular hour of the year. The function will check this for each hour of the year and return an 8760 aggregated fan operating schedule.

    Parameters
    ----------
    rmd: dict A zone id associated with the rmd for which to create the aggregated fan operating schedule as described above.
    zone_id: str A zone id associated with the rmd for which to create the aggregated fan operating schedule as described above.
    is_leap_year: bool, indicate whether the comparison is in a leap year or not. True / False


    Returns
    ----------
    aggregated_zone_hvac_fan_operating_schedule: 8760 aggregated fan operating schedule for the zone.
    """
    num_hours = (
        LeapYear.LEAP_YEAR_HOURS if is_leap_year else LeapYear.REGULAR_YEAR_HOURS
    )

    schedules = []
    for hvac_id in get_list_hvac_systems_associated_with_zone(rmd, zone_id):
        hvac = find_exactly_one_hvac_system(rmd, hvac_id)
        fan_sys = getattr_(hvac, "hvac", "fan_system")

        fan_sys_operating_sch = fan_sys.get("operating_schedule")
        if fan_sys_operating_sch:
            schedules.append(
                getattr_(
                    find_one(
                        f'$.schedules[*][?(@.id = "{fan_sys_operating_sch}")]', rmd
                    ),
                    "schedules",
                    "hourly_values",
                )
            )
        else:
            schedules.append([1] * num_hours)

    assert_(
        len(schedules) > 0,
        "Please make sure the provided ZONE 'zone_id' is connected with at least one HVAC system",
    )

    # determine if all the schedules operate. If so, assign 1, else 0.
    schedules_df = pd.DataFrame(schedules)
    aggregated_zone_hvac_fan_operating_schedule = (
        (schedules_df.gt(0).all(axis=0)).astype(int).tolist()
    )

    return aggregated_zone_hvac_fan_operating_schedule
