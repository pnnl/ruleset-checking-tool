import pandas as pd
from rct229.rulesets.ashrae9012019.ruleset_functions.get_list_hvac_systems_associated_with_zone import (
    get_list_hvac_systems_associated_with_zone,
)
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_one


def get_aggregated_zone_hvac_fan_operating_schedule(rmd, zone_id):
    """
     This function loops through all of the HVAC system fan operating schedules associated with a specific zone and
     creates an aggregated fan operating schedule for the zone. More specifically, if any of the fan operating schedules
     associated with any of the hvac systems serving the zone have a 1 for a particular hour of the year then the aggregated schedule will equal 1
     for that particular hour of the year. The function will check this for each hour of the year and return an 8760 aggregated fan operating schedule.

    Parameters
    ----------
    rmd: dict A zone id associated with the RMR for which to create the aggregated fan operating schedule as described above.
    zone_id: str A zone id associated with the RMR for which to create the aggregated fan operating schedule as described above.

    Returns
    ----------
    aggregated_zone_hvac_fan_operating_schedule: 8760 aggregated fan operating schedule for the zone.
    """

    schedules = []
    for hvac_id in get_list_hvac_systems_associated_with_zone(rmd, zone_id):
        fan_sys = find_one(
            f'$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*][?(@.id = "{hvac_id}")].fan_system',
            rmd,
        )
        fan_sys_operating_sch = getattr_(fan_sys, "fan_system", "operating_schedule")
        fan_sys_sch = find_one(
            f'$.schedules[*][?(@.id = "{fan_sys_operating_sch}")]', rmd
        )

        if fan_sys_sch is None:
            schedules.append([1] * 8760)
        else:
            schedules.append(
                getattr_(
                    fan_sys_sch,
                    "schedules",
                    "hourly_values",
                )
            )

    # determine if all the schedules operate. If so, assign 1, else 0.
    schedules_df = pd.DataFrame(schedules)
    aggregated_zone_hvac_fan_operating_schedule = (
        (schedules_df.sum(axis=0) == len(schedules_df)).astype(int).tolist()
    )

    return aggregated_zone_hvac_fan_operating_schedule
