from typing import Literal

from pint import Quantity
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import ZERO
from rct229.utils.utility_functions import (
    find_exactly_one_schedule,
    find_exactly_one_zone,
)


def get_zone_peak_internal_load_floor_area_dict(
    rmd: dict, zone_id: str
) -> dict[Literal["peak", "area"], Quantity]:
    """
    Finds the peak coincident internal loads of a zone and returns the value in btu/h/ft2
    The function returns a dict giving 2 values: {"PEAK":total peak btu/h/ft2 in the zone, "AREA":total zone area} the
    total peak btu/sf is the internal non-coincident peak loads in all spaces in the zone

    The function does not raise exception for missing values rather it applies default values.

    Parameters
    ----------
    rmd: dict
    A dictionary representing a RuleModelInstance object as defined by the ASHRAE229 schema
    zone_id: string
        zone id

    Returns
    -------
    result: dict
    a dictionary that contains two keys, peak, and area.
    """
    zone = find_exactly_one_zone(rmd, zone_id)
    zone_area = ZERO.AREA
    zone_load = ZERO.POWER

    for space in find_all("$.spaces[*]", zone):
        space_area = space.get("floor_area", ZERO.AREA)
        zone_area += space_area
        for light in find_all("$.interior_lighting[*]", space):
            lighting_design_schedule = find_exactly_one_schedule(
                rmd,
                getattr_(light, "interior_lighting", "lighting_multiplier_schedule"),
            )
            lighting_max_schedule_fraction = max(
                getattr_(
                    lighting_design_schedule,
                    "lighting_multiplier_schedule",
                    "hourly_cooling_design_day",
                )
            )
            zone_load += (
                light.get("power_per_area", ZERO.POWER_PER_AREA)
                * space_area
                * lighting_max_schedule_fraction
            )

        for equipment in find_all("$.miscellaneous_equipment[*]", space):
            equipment_design_schedule = find_exactly_one_schedule(
                rmd,
                getattr_(equipment, "miscellaneous_equipment", "multiplier_schedule"),
            )
            equipment_max_schedule_fraction = max(
                getattr_(
                    equipment_design_schedule,
                    "multiplier_schedule",
                    "hourly_cooling_design_day",
                )
            )
            zone_load += (
                equipment.get("power", ZERO.POWER) * equipment_max_schedule_fraction
            )

        # allows no occupants data in a zone
        occupant_max_schedule_fraction = 0.0
        if space.get("occupant_multiplier_schedule"):
            occupant_design_schedule = find_exactly_one_schedule(
                rmd, space["occupant_multiplier_schedule"]
            )
            occupant_max_schedule_fraction = max(
                getattr_(
                    occupant_design_schedule,
                    "occupant_multiplier",
                    "hourly_cooling_design_day",
                )
            )
        zone_load += (
            space.get("occupant_sensible_heat_gain", ZERO.POWER)
            + space.get("occupant_latent_heat_gain", ZERO.POWER)
        ) * occupant_max_schedule_fraction

    return {"peak": zone_load, "area": zone_area}
