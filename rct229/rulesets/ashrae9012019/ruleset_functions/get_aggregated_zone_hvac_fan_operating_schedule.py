from typing import Optional

import pandas as pd
from rct229.rule_engine.rulesets import LeapYear
from rct229.rulesets.ashrae9012019.ruleset_functions.get_list_hvac_systems_associated_with_zone import (
    get_list_hvac_systems_associated_with_zone,
)
from rct229.utils.assertions import assert_, getattr_
from rct229.utils.jsonpath_utils import find_one
from rct229.utils.utility_functions import find_exactly_one_hvac_system


def get_aggregated_zone_hvac_fan_operating_schedule(rmd: dict, zone_id: str) -> list:
    """
    This function loops through all of the HVAC system fan operating schedules associated with a specific zone and
    creates an aggregated fan operating schedule for the zone. If any schedule has a 1 for a particular hour, the
    aggregated schedule will also have a 1 at that hour. Returns an aggregated schedule matching the schedule length.
    If any HVAC system lacks a schedule, a constant schedule of 1s is assumed for that system.
    """
    schedules = []
    assume_constant = False

    for hvac_id in get_list_hvac_systems_associated_with_zone(rmd, zone_id):
        hvac = find_exactly_one_hvac_system(rmd, hvac_id)
        fan_sys = getattr_(hvac, "hvac", "fan_system")

        fan_sys_operating_sch = fan_sys.get("operating_schedule")
        if fan_sys_operating_sch:
            schedule_values = getattr_(
                find_one(f'$.schedules[*][?(@.id = "{fan_sys_operating_sch}")]', rmd),
                "schedules",
                "hourly_values",
            )
            schedules.append(schedule_values)
        else:
            assume_constant = True

    assert_(
        len(schedules) > 0 or assume_constant,
        f"No fan operating schedules found for zone '{zone_id}', and no fallback assumed.",
    )

    # If any schedule is missing, use constant 1s schedule of same length as existing schedules
    if assume_constant:
        # Try to get the reference length from existing schedules
        schedule_length = (
            len(schedules[0]) if schedules else 8760
        )  # fallback to 8760 if none exist
        schedules.append([1] * schedule_length)

    schedules_df = pd.DataFrame(schedules)
    aggregated_zone_hvac_fan_operating_schedule = (
        (schedules_df.gt(0).any(axis=0)).astype(int).tolist()
    )

    return aggregated_zone_hvac_fan_operating_schedule
