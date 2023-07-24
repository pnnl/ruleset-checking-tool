from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    find_exactly_one_zone,
    find_exactly_one_schedule,
)
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import ZERO


def get_zone_peak_internal_load_floor_area_dict(rmi, zone_id):
    """
    Finds the peak coincident internal loads of a zone and returns the value with a load unit.
    The function returns a dict giving 2 values: {"peak":total peak (load unit) in the zone, "area":total zone area} the
    total peak is the internal non-coincident peak loads in all spaces in the zone

    The function does not raise exception for missing values rather it applies default values.

    Parameters
    ----------
    rmi: dict
    A dictionary representing a RuleModelInstance object as defined by the ASHRAE229 schema
    zone_id: string
    zone id

    Returns
    -------
    result: dict
    a dictionary that contains two keys, peak, and area.
    """
    zone = find_exactly_one_zone(rmi, zone_id)
    zone_area = ZERO.AREA
    zone_load = ZERO.POWER

    for space in find_all("$.spaces[*]", zone):
        space_area = space.get("floor_area", ZERO.AREA)
        zone_area += space_area
        for light in find_all("$.interior_lighting[*]", space):
            # default value
            lighting_max_schedule_fraction = 1.0
            if light.get("lighting_multiplier_schedule"):
                lighting_max_schedule_fraction = max(
                    getattr_(
                        find_exactly_one_schedule(
                            rmi,
                            light["lighting_multiplier_schedule"],
                        ),
                        "Schedule",
                        "hourly_cooling_design_day",
                    )
                )

            zone_load += (
                light.get("power_per_area", ZERO.POWER_PER_AREA)
                * space_area
                * lighting_max_schedule_fraction
            )

        for equipment in find_all("$.miscellaneous_equipment[*]", space):
            # default value
            equipment_max_schedule_fraction = 1.0
            if equipment.get("multiplier_schedule"):
                equipment_max_schedule_fraction = max(
                    getattr_(
                        find_exactly_one_schedule(
                            rmi,
                            equipment["multiplier_schedule"],
                        ),
                        "Schedule",
                        "hourly_cooling_design_day",
                    )
                )

            zone_load += (
                equipment.get("power", ZERO.POWER) * equipment_max_schedule_fraction
            )

        # allows no occupants data in a zone
        occupant_max_schedule_fraction = 1.0
        if space.get("occupant_multiplier_schedule"):
            occupant_max_schedule_fraction = max(
                getattr_(
                    find_exactly_one_schedule(
                        rmi, space["occupant_multiplier_schedule"]
                    ),
                    "Schedule",
                    "hourly_cooling_design_day",
                )
            )
        zone_load += (
            space.get("occupant_sensible_heat_gain", ZERO.POWER)
            + space.get("occupant_latent_heat_gain", ZERO.POWER)
        ) * occupant_max_schedule_fraction

    return {"peak": zone_load, "area": zone_area}
