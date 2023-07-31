from pydash import flow, flat_map, for_each, chain, reduce_, map_

from rct229.rule_engine.rulesets import LeapYear
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    find_exactly_one_hvac_system,
    find_exactly_one_zone,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_list_hvac_systems_associated_with_zone import (
    get_list_hvac_systems_associated_with_zone,
)
from rct229.utils.assertions import assert_
from rct229.utils.jsonpath_utils import find_one, find_all

ZONE_OCCUPANTS_RATIO_THRESHOLD = 0.05


def get_zone_eflh(rmi: dict, zone_id: str, is_leap_year: bool):
    """
    provides the equivalent full load hours of the zone. Equivalent full load hours are defined as: any hour where
    the occupancy fraction is greater than 5% AND the HVAC system is in occupied mode. For this function,
    we are recognizing the HVAC system as being in occupied mode if ANY of the HVAC systems serving the zone are in
    occupied mode.

    Applicability Note: hvac_system.fan_system.operation_schedule is being used as the HVAC operation
    schedule. Therefore, this check will not work for radiant systems or other systems that do not include a fan

    Parameters
    ----------
    rmi dict
        A dictionary representing a ruleset model instance as defined by the ASHRAE229 schema
    zone_id str
        zone id

    Returns
    -------
    flh int a number equal to the total equivalent full load hours for the year
    """
    # 1. get data needed for processing
    num_hours = (
        LeapYear.LEAP_YEAR_HOURS if is_leap_year else LeapYear.REGULAR_YEAR_HOURS
    )
    thermal_zone = find_exactly_one_zone(rmi, zone_id)
    hvac_systems_list = get_list_hvac_systems_associated_with_zone(rmi, zone_id)

    # 2. functions
    # function to get the maximum schedule value in an hourly schedule or 1.0
    multiplier_annual_hourly_values_func = flow(
        lambda schedule_id: find_one(
            f'$.schedules[*][?(@.id="{schedule_id}")].hourly_values', rmi
        ),
        lambda hourly_values: hourly_values if hourly_values else [1.0] * num_hours,
    )
    # function get hourly_values list from heating_design_day, it is either the
    # hourly_values from schedule or [1.0]
    multiplier_heating_design_hourly_values_func = flow(
        lambda schedule_id: find_one(
            f'$.schedules[*][?(@.id="{schedule_id}")].hourly_heating_design_day', rmi
        ),
        lambda hourly_values: hourly_values if hourly_values else [1.0],
    )
    # function get hourly_values list from cooling_design_day, it is either the
    # hourly_values from schedule or [1.0]
    multiplier_cooling_design_hourly_values_func = flow(
        lambda schedule_id: find_one(
            f'$.schedules[*][?(@.id="{schedule_id}")].hourly_cooling_design_day', rmi
        ),
        lambda hourly_values: hourly_values if hourly_values else [1.0],
    )

    # get fan operation schedule from an HVAC,
    # missing data (fan) is handled and return as [0.0] * num_hours
    get_fan_operation_schedule_func = flow(
        lambda hvac_id: find_exactly_one_hvac_system(rmi, hvac_id),
        lambda hvac: find_one("$.fan_system", hvac),
        # fan could be None
        lambda fan: fan.get("operating_schedule", None) if fan else None,
        lambda operation_schedule_id: find_one(
            f'$.schedules[*][?(@.id="{operation_schedule_id}")].hourly_values', rmi
        ),
        lambda hourly_values: hourly_values if hourly_values else [0.0] * num_hours,
    )

    # 3. Calculating values
    # list of list of HVAC annual operation schedule
    # [[0,0,0,1,1,1,...], [0,0,0,1,1,1,...]...]
    hvac_operation_schedule_list = map_(
        hvac_systems_list, lambda hvac_id: get_fan_operation_schedule_func(hvac_id)
    )

    # make sure all operation schedule has the same hours and they are equal to num_hours
    assert_(
        all(
            flat_map(
                hvac_operation_schedule_list,
                lambda schedule: len(schedule) == num_hours,
            )
        ),
        f"Not all HVAC operation schedules have ${num_hours} hours",
    )

    # list of integers that contains the maximum number of occupants per space.
    # [10,12,22...]
    num_of_occupant_per_space_list = flat_map(
        find_all("$.spaces[*]", thermal_zone),
        lambda space: max(
            max(
                multiplier_annual_hourly_values_func(
                    find_one("$.occupant_multiplier_schedule", space)
                )
            ),
            max(
                multiplier_heating_design_hourly_values_func(
                    find_one("$.occupant_multiplier_schedule", space)
                )
            ),
            max(
                multiplier_cooling_design_hourly_values_func(
                    find_one("$.occupant_multiplier_schedule", space)
                )
            ),
            1.0,
        )
        * find_one("$.number_of_occupants", space, 0.0),
    )
    # sum of the maximum number of occupants
    total_zone_occupants = sum(num_of_occupant_per_space_list)

    # list of list of annual hourly_values per space.
    # this shall guarantee the num_hours length per hourly_values list.
    # [[0,0,0.2,0.2...], [0,0,0.2,0.2...]...]
    occupant_annual_hourly_value_per_space_list = map_(
        find_all("$.spaces[*].occupant_multiplier_schedule", thermal_zone),
        lambda occupant_multiplier_schedule_id: multiplier_annual_hourly_values_func(
            occupant_multiplier_schedule_id
        ),
    )

    # make sure all operation schedule has the same hours and they are equal to num_hours
    assert_(
        all(
            flat_map(
                occupant_annual_hourly_value_per_space_list,
                lambda schedule: len(schedule) == num_hours,
            )
        ),
        f"Not all occupant schedules have ${num_hours} hours",
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
            flat_map(hvac_operation_schedule_list, lambda schedule: schedule[hour])
        )

        if (
            occupants_this_hour / total_zone_occupants > ZONE_OCCUPANTS_RATIO_THRESHOLD
            and hvac_systems_operational_this_hour
        ):
            flh += 1
    return flh
