from rct229.rulesets.ashrae9012022.ruleset_functions.get_list_hvac_systems_associated_with_zone import (
    get_list_hvac_systems_associated_with_zone,
)
from rct229.utils.assertions import assert_
from rct229.utils.schedule_utils import (
    get_max_schedule_multiplier_cooling_design_hourly_value_or_default,
    get_max_schedule_multiplier_heating_design_hourly_value_or_default,
    get_max_schedule_multiplier_hourly_value_or_default,
    get_schedule_multiplier_hourly_value_or_default,
)
from rct229.utils.utility_functions import (
    find_exactly_one_hvac_system,
    find_exactly_one_zone,
)

ZONE_OCCUPANTS_RATIO_THRESHOLD = 0.05


def get_zone_eflh(rmd: dict, zone_id: str) -> int:
    # ------------------------------------------------------------------
    # Resolve core objects once
    # ------------------------------------------------------------------
    zone = find_exactly_one_zone(rmd, zone_id)
    hvac_ids = get_list_hvac_systems_associated_with_zone(rmd, zone_id)

    schedules_map = {sch.get("id"): sch for sch in rmd.get("schedules", [])}
    spaces = zone.get("spaces", [])

    # ------------------------------------------------------------------
    # Determine number of hours
    # ------------------------------------------------------------------
    num_hours = None

    for hvac_id in hvac_ids:
        hvac = find_exactly_one_hvac_system(rmd, hvac_id)
        sched_id = hvac.get("fan_system", {}).get("operating_schedule")
        values = schedules_map.get(sched_id, {}).get("hourly_values")
        if values:
            num_hours = len(values)
            break

    if num_hours is None:
        for space in spaces:
            sched_id = space.get("occupant_multiplier_schedule")
            values = schedules_map.get(sched_id, {}).get("hourly_values")
            if values:
                num_hours = len(values)
                break

    if num_hours is None:
        num_hours = 8760

    # ------------------------------------------------------------------
    # HVAC fan operation schedules
    # ------------------------------------------------------------------
    hvac_operation_schedule_list = []

    for hvac_id in hvac_ids:
        hvac = find_exactly_one_hvac_system(rmd, hvac_id)
        sched_id = hvac.get("fan_system", {}).get("operating_schedule")
        values = schedules_map.get(sched_id, {}).get("hourly_values")
        hvac_operation_schedule_list.append(values if values else [1.0] * num_hours)

    assert_(
        all(len(s) == num_hours for s in hvac_operation_schedule_list),
        f"Not all HVAC operation schedules have {num_hours} hours",
    )

    # ------------------------------------------------------------------
    # Max occupants per space
    # ------------------------------------------------------------------
    num_of_occupant_per_space_list = []

    for space in spaces:
        sched_id = space.get("occupant_multiplier_schedule")
        base_occupants = space.get("number_of_occupants", 0.0)

        max_multiplier = max(
            get_max_schedule_multiplier_hourly_value_or_default(rmd, sched_id, 1.0),
            get_max_schedule_multiplier_heating_design_hourly_value_or_default(
                rmd, sched_id, 1.0
            ),
            get_max_schedule_multiplier_cooling_design_hourly_value_or_default(
                rmd, sched_id, 1.0
            ),
            1.0,
        )

        num_of_occupant_per_space_list.append(max_multiplier * base_occupants)

    total_zone_occupants = sum(num_of_occupant_per_space_list)

    # ------------------------------------------------------------------
    # Hourly occupant schedules per space
    # ------------------------------------------------------------------
    occupant_annual_hourly_value_per_space_list = [
        get_schedule_multiplier_hourly_value_or_default(
            rmd,
            space.get("occupant_multiplier_schedule"),
            [1.0] * num_hours,
        )
        for space in spaces
    ]

    assert_(
        all(len(s) == num_hours for s in occupant_annual_hourly_value_per_space_list),
        f"Not all occupant schedules have {num_hours} hours",
    )

    # ------------------------------------------------------------------
    # Compute FLH
    # ------------------------------------------------------------------
    flh = 0

    for hour in range(num_hours):
        occupants_this_hour = sum(
            occ * sched[hour]
            for occ, sched in zip(
                num_of_occupant_per_space_list,
                occupant_annual_hourly_value_per_space_list,
            )
        )

        hvac_operational = any(sched[hour] for sched in hvac_operation_schedule_list)

        if (
            total_zone_occupants > 0
            and occupants_this_hour / total_zone_occupants
            > ZONE_OCCUPANTS_RATIO_THRESHOLD
            and hvac_operational
        ):
            flh += 1

    return flh
