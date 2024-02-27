from pydash import map_
from rct229.rulesets.ashrae9012019.ruleset_functions.get_list_hvac_systems_associated_with_zone import (
    get_list_hvac_systems_associated_with_zone,
)
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.utility_functions import find_exactly_one_schedule


def get_aggregated_zone_hvac_fan_operating_schedule(rmi, zone_id):
    """
     This function loops through all of the HVAC system fan operating schedules associated with a specific zone and
     creates an aggregated fan operating schedule for the zone. More specifically, if any of the fan operating schedules
     associated with any of the hvac systems serving the zone have a 1 for a particular hour of the year then the aggregated schedule will equal 1
     for that particular hour of the year. The function will check this for each hour of the year and return an 8760 aggregated fan operating schedule.

    Parameters
    ----------
    rmi: dict A zone id associated with the RMR for which to create the aggregated fan operating schedule as described above.
    zone_id: str A zone id associated with the RMR for which to create the aggregated fan operating schedule as described above.

    Returns
    ----------
    aggregated_zone_hvac_fan_operating_schedule_x: 8760 aggregated fan operating schedule for the zone.
    """

    aggregated_zone_hvac_fan_operating_schedule = {}
    for HVAC_id in get_list_hvac_systems_associated_with_zone(rmi, zone_id):
        for HVAC in find_all(
            f'$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*][?(@.id = "{HVAC_id}")]',
            rmi,
        ):
            fan_sys = getattr_(HVAC, "HVAC", "fan_system")
            fan_sch = getattr_(
                find_exactly_one_schedule(
                    rmi, getattr_(fan_sys, "fan_system", "operating_schedule")
                ),
                "schedules",
                "hourly_values",
            )
            aggregated_zone_hvac_fan_operating_schedule[fan_sys["id"]] = map_(
                fan_sch, lambda x: 1.0 if x == 1 else 0
            )

    return aggregated_zone_hvac_fan_operating_schedule
