from typing import Literal

from pint import Quantity
from rct229.utils.assertions import assert_
from rct229.utils.pint_utils import ZERO
from rct229.utils.utility_functions import find_exactly_one_zone


def get_cooling_design_schedule_values(schedule: dict) -> list:
    has_day = "hourly_cooling_design_day" in schedule
    has_year = "hourly_cooling_design_year" in schedule

    assert_(
        has_day or has_year,
        "Schedule must contain either 'hourly_cooling_design_day' or 'hourly_cooling_design_year'",
    )

    assert_(
        not (has_day and has_year),
        "Schedule must not contain both 'hourly_cooling_design_day' and 'hourly_cooling_design_year'",
    )

    return (
        schedule["hourly_cooling_design_day"]
        if has_day
        else schedule["hourly_cooling_design_year"]
    )


def get_zone_peak_internal_load_floor_area_dict(
    rmd: dict, zone_id: str
) -> dict[Literal["peak", "area"], Quantity]:
    """
    Finds the peak coincident internal loads of a zone and returns the value with a load unit.
    Returns {"peak": total peak load, "area": total zone area}.
    """

    # ------------------------------------------------------------------
    # Resolve zone and build schedule lookup once
    # ------------------------------------------------------------------
    zone = find_exactly_one_zone(rmd, zone_id)
    schedules_map = {sch.get("id"): sch for sch in rmd.get("schedules", [])}

    zone_area = ZERO.AREA
    zone_load = ZERO.POWER

    spaces = zone.get("spaces", [])

    # ------------------------------------------------------------------
    # Iterate spaces
    # ------------------------------------------------------------------
    for space in spaces:
        space_area = space.get("floor_area", ZERO.AREA)
        zone_area += space_area

        # --------------------------------------------------------------
        # Interior lighting
        # --------------------------------------------------------------
        for light in space.get("interior_lighting", []):
            sched_id = light.get("lighting_multiplier_schedule")
            schedule = schedules_map.get(sched_id, {})
            values = get_cooling_design_schedule_values(schedule)
            max_fraction = max(
                values, default=1.0
            )  # if values is empty, default to 1.0 (full load)

            zone_load += (
                light.get("power_per_area", ZERO.POWER_PER_AREA)
                * space_area
                * max_fraction
            )

        # --------------------------------------------------------------
        # Miscellaneous equipment
        # --------------------------------------------------------------
        for equipment in space.get("miscellaneous_equipment", []):
            sched_id = equipment.get("multiplier_schedule")
            schedule = schedules_map.get(sched_id, {})
            values = get_cooling_design_schedule_values(schedule)
            max_fraction = max(
                values, default=1.0
            )  # if values is empty, default to 1.0 (full load)

            zone_load += equipment.get("power", ZERO.POWER) * max_fraction

        # --------------------------------------------------------------
        # Occupants (allowed missing)
        # --------------------------------------------------------------
        sched_id = space.get("occupant_multiplier_schedule")
        schedule = schedules_map.get(sched_id, {})
        values = get_cooling_design_schedule_values(schedule)
        max_fraction = max(
            values, default=1.0
        )  # if values is empty, default to 1.0 (full load)

        zone_load += (
            space.get("occupant_sensible_heat_gain", ZERO.POWER)
            + space.get("occupant_latent_heat_gain", ZERO.POWER)
        ) * max_fraction

    return {"peak": zone_load, "area": zone_area}
