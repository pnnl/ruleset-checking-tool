from pydash import flow, map_
from rct229.rule_engine.rulesets import LeapYear
from rct229.rulesets.ashrae9012019.ruleset_functions.get_list_hvac_systems_associated_with_zone import (
    get_list_hvac_systems_associated_with_zone,
)
from rct229.utils.assertions import assert_
from rct229.utils.jsonpath_utils import find_all, find_one
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
    """
    provides the equivalent full load hours of the zone. Equivalent full load hours are defined as: any hour where
    the occupancy fraction is greater than 5% AND the HVAC system is in occupied mode. For this function,
    we are recognizing the HVAC system as being in occupied mode if ANY of the HVAC systems serving the zone are in
    occupied mode.

    Applicability Note: hvac_system.fan_system.operation_schedule is being used as the HVAC operation
    schedule. Therefore, this check will not work for radiant systems or other systems that do not include a fan

    Parameters
    ----------
    rmd dict
        A dictionary representing a ruleset model description as defined by the ASHRAE229 schema
    zone_id str
        zone id

    Returns
    -------
    flh int a number equal to the total equivalent full load hours for the year
    """
    # 1. get data needed for processing
    thermal_zone = find_exactly_one_zone(rmd, zone_id)
    hvac_systems_list = get_list_hvac_systems_associated_with_zone(rmd, zone_id)

    num_hours = None
    for hvac_id in hvac_systems_list:
        hvac = find_exactly_one_hvac_system(rmd, hvac_id)
        sched_id = find_one("$.fan_system.operating_schedule", hvac)
        values = find_one(f'$.schedules[*][?(@.id="{sched_id}")].hourly_values', rmd)
        if values:
            num_hours = len(values)
            break

    if num_hours is None:
        for space in find_all("$.spaces[*]", thermal_zone):
            sched_id = space.get("occupant_multiplier_schedule")
            values = find_one(
                f'$.schedules[*][?(@.id="{sched_id}")].hourly_values', rmd
            )
            if values:
                num_hours = len(values)
                break

    if num_hours is None:
        num_hours = 8760  # fallback default

    # 2. functions
    # get fan operation schedule from an HVAC,
    # missing data (fan) is handled and return as [1.0] * num_hours
    get_fan_operation_schedule_func = flow(
        lambda hvac_id: find_exactly_one_hvac_system(rmd, hvac_id),
        lambda hvac: find_one("$.fan_system.operating_schedule", hvac),
        lambda operation_schedule_id: find_one(
            f'$.schedules[*][?(@.id="{operation_schedule_id}")].hourly_values', rmd
        ),
        lambda hourly_values: hourly_values if hourly_values else [1.0] * num_hours,
    )

    # 3. Calculating values
    # list of list of HVAC annual operation schedule
    # [[0,0,0,1,1,1,...], [0,0,0,1,1,1,...]...]
    hvac_operation_schedule_list = list(
        map(lambda hvac_id: get_fan_operation_schedule_func(hvac_id), hvac_systems_list)
    )

    # make sure all operation schedule has the same hours and they are equal to num_hours
    assert_(
        all(
            map(
                lambda schedule: len(schedule) == num_hours,
                hvac_operation_schedule_list,
            )
        ),
        f"Not all HVAC operation schedules have ${num_hours} hours",
    )

    # list of integers that contains the maximum number of occupants per space.
    # [10,12,22...]
    num_of_occupant_per_space_list = list(
        map(
            lambda space: max(
                get_max_schedule_multiplier_hourly_value_or_default(
                    rmd, find_one("$.occupant_multiplier_schedule", space), 1.0
                ),
                get_max_schedule_multiplier_heating_design_hourly_value_or_default(
                    rmd, find_one("$.occupant_multiplier_schedule", space), 1.0
                ),
                get_max_schedule_multiplier_cooling_design_hourly_value_or_default(
                    rmd, find_one("$.occupant_multiplier_schedule", space), 1.0
                ),
                1.0,
            )
            * find_one("$.number_of_occupants", space, 0.0),
            find_all("$.spaces[*]", thermal_zone),
        )
    )

    # sum of the maximum number of occupants
    total_zone_occupants = sum(num_of_occupant_per_space_list)

    # list of list of annual hourly_values per space.
    # this shall guarantee the num_hours length per hourly_values list.
    # [[0,0,0.2,0.2...], [0,0,0.2,0.2...]...]
    occupant_annual_hourly_value_per_space_list = list(
        map(
            lambda space: get_schedule_multiplier_hourly_value_or_default(
                rmd, space.get("occupant_multiplier_schedule"), [1.0] * num_hours
            ),
            find_all("$.spaces[*]", thermal_zone),
        )
    )

    # make sure all operation schedules have the same hours
    assert_(
        all(
            map(
                lambda schedule: len(schedule) == num_hours,
                occupant_annual_hourly_value_per_space_list,
            )
        ),
        f"Not all occupant schedules have {num_hours} hours",
    )

    flh = 0
    for hour in range(num_hours):
        # at this hour, the total number of occupants from spaces.
        occupants_this_hour = sum(
            [
                num_occupant * hourly_values[hour]
                for num_occupant, hourly_values in zip(
                    num_of_occupant_per_space_list,
                    occupant_annual_hourly_value_per_space_list,
                )
            ]
        )

        # 0.0 is falsy, 1.0 is truthy
        hvac_systems_operational_this_hour = any(
            map(lambda schedule: schedule[hour], hvac_operation_schedule_list)
        )

        # Allow plenum as indirectly conditioned zone but has 0.0 occupants.
        # In such case, we do not add flh value
        if (
            total_zone_occupants > 0
            and occupants_this_hour / total_zone_occupants
            > ZONE_OCCUPANTS_RATIO_THRESHOLD
            and hvac_systems_operational_this_hour
        ):
            flh += 1
    return flh
