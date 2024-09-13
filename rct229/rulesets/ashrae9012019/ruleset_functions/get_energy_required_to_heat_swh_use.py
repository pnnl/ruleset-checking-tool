from rct229.rulesets.ashrae9012019.ruleset_functions.get_spaces_served_by_swh_use import (
    get_spaces_served_by_swh_use,
)
from rct229.schema.config import ureg
from rct229.schema.schema_enums import SchemaEnums
from pint import Quantity
from rct229.utils.assertions import assert_
from rct229.utils.jsonpath_utils import find_exactly_one_with_field_value, find_all
from rct229.utils.pint_utils import ZERO
from rct229.utils.utility_functions import find_exactly_one_schedule

SERVICE_WATER_HEATING_USE_UNIT = SchemaEnums.schema_enums[
    "ServiceWaterHeatingUseUnitOptions"
]

REQUIRED_USE_UNIT = [
    SERVICE_WATER_HEATING_USE_UNIT.POWER,
    SERVICE_WATER_HEATING_USE_UNIT.VOLUME,
]


def get_energy_required_to_heat_swh_use(
    swh_use: dict, rmd: dict, building_segment: dict
) -> dict[str, Quantity]:
    """
    This function calculates the total energy required to heat the SWH use over the course of a year in btu.  Note - this function does not work for service water heating uses with use_units == "OTHER".  In this case, it will return 0.

    Parameters
    ----------
    swh_use: dict, service_water_heating_uses
    rmd: dict, RMD at RuleSetModelDescription level
    building_segment: dict, building_segment

    Returns
    ----------
    energy_required_by_space: A dict where the keys are space_ids and values are the total energy required to heat the swh_use for that space.  If a swh_use is not assigned to any spaces, the key will be "NO_SPACES_ASSIGNED"

    """

    hourly_schedule_id = swh_use.get("use_multiplier_schedule")
    hourly_schedule = (
        find_exactly_one_schedule(rmd, hourly_schedule_id)
        if hourly_schedule_id is not None
        else None
    )

    distribution_system_id = swh_use.get("served_by_distribution_system", "")
    distribution_system = find_exactly_one_with_field_value(
        "$.service_water_heating_distribution_systems[*]",
        "id",
        distribution_system_id,
        rmd,
    )
    supply_temperature = distribution_system.get("design_supply_temperature")
    assert_(
        supply_temperature is not None,
        "A service water heating supply temperature must be provided",
    )
    swh_use_value = swh_use.get("use", 0)
    inlet_temperature_schedule_id = distribution_system.get(
        "entering_water_mains_temperature_schedule", ""
    )
    inlet_temperature_schedule = find_exactly_one_schedule(
        rmd, inlet_temperature_schedule_id
    )

    inlet_temperature_hourly_values = inlet_temperature_schedule.get("hourly_values")
    assert_(
        inlet_temperature_hourly_values is not None,
        "A service water heating inlet hourly temperature schedule must be provided",
    )

    drain_heat_recovery_efficiency = (
        distribution_system.get("drain_heat_recovery_efficiency")
        if (swh_use.get("is_heat_recovered_by_drain"))
        else 0
    )
    use_units = swh_use.get("use_units")
    assert_(use_units is not None, "A use unit must be provided")

    space_ids = get_spaces_served_by_swh_use(rmd, swh_use["id"])
    space_within_building_segment_ids = [
        space["id"] for space in find_all("$.zones[*].spaces[*]", building_segment)
    ]
    spaces = [
        find_exactly_one_with_field_value(
            "$.buildings[*].building_segments[*].zones[*].spaces[*]",
            "id",
            space_id,
            rmd,
        )
        for space_id in space_ids
        if space_id in space_within_building_segment_ids
    ]

    if len(spaces) == 0 and use_units not in REQUIRED_USE_UNIT:
        spaces = find_all("$.zones[*].spaces[*]", building_segment)

    energy_required_by_space = {}
    volume_flow_rate = 0
    hourly_values = (
        hourly_schedule.get("hourly_values")
        if hourly_schedule is not None
        else [1] * len(inlet_temperature_schedule)
    )
    for space in spaces:
        if use_units == SERVICE_WATER_HEATING_USE_UNIT.POWER_PER_PERSON:
            power = swh_use_value * space.get("number_of_occupants", 0)
            energy_required = (
                power
                * sum(hourly_values)
                * (1 - drain_heat_recovery_efficiency)
                * ureg("Btu")
            )
            energy_required_by_space[space["id"]] = energy_required

        elif use_units == SERVICE_WATER_HEATING_USE_UNIT.POWER_PER_AREA:
            power = swh_use_value * space.get("floor_area", ZERO.AREA).magnitude
            energy_required = (
                power
                * sum(hourly_values)
                * (1 - drain_heat_recovery_efficiency)
                * ureg("Btu")
            )
            energy_required_by_space[space["id"]] = energy_required

        elif use_units == SERVICE_WATER_HEATING_USE_UNIT.POWER:
            energy_required_by_space[space["id"]] = (
                swh_use_value
                * sum(hourly_values)
                * (1 - drain_heat_recovery_efficiency)
                * ureg("Btu")
            )

        elif use_units == SERVICE_WATER_HEATING_USE_UNIT.VOLUME_PER_PERSON:
            volume_flow_rate += swh_use_value * space.get("number_of_occupants", 0)

        elif use_units == SERVICE_WATER_HEATING_USE_UNIT.VOLUME_PER_AREA:
            volume_flow_rate += (
                swh_use_value * space.get("floor_area", ZERO.AREA).magnitude
            )

        elif use_units == SERVICE_WATER_HEATING_USE_UNIT.VOLUME:
            volume_flow_rate += swh_use_value

        else:
            energy_required_by_space[space["id"]] = "UNDETERMINED"

        if energy_required_by_space.get(space["id"]) is None:
            energy_required = 0 * ureg("Btu")
            for index, hourly_value in enumerate(hourly_values):
                volume_this_hour = volume_flow_rate * hourly_value
                volume_this_hour = volume_this_hour * (
                    1 - drain_heat_recovery_efficiency
                )

                # covert dT in Celsius to Fahrenheit
                dT = (
                    supply_temperature.magnitude
                    - inlet_temperature_hourly_values[index]
                ) * 1.8
                energy_to_heat_water = volume_this_hour * 8.3452 * dT * ureg("Btu")
                energy_required += energy_to_heat_water
            energy_required_by_space[space["id"]] = energy_required

    if len(spaces) == 0:
        if swh_use.get("use_units") == "OTHER":
            energy_required_by_space["NO_SPACES_ASSIGNED"] = "UNDETERMINED"
        elif swh_use.get("use_units") == "POWER":
            energy_required_by_space["NO_SPACES_ASSIGNED"] = swh_use_value * ureg("Btu")
        elif swh_use.get("use_units") == "VOLUME":
            energy_required = 0 * ureg("Btu")
            for index, hourly_value in enumerate(hourly_values):
                volume_this_hour = swh_use_value * hourly_value
                volume_this_hour = volume_this_hour * (
                    1 - drain_heat_recovery_efficiency
                )
                dT = (
                    supply_temperature.magnitude
                    - inlet_temperature_hourly_values[index]
                ) * 1.8
                energy_to_heat_water = volume_this_hour * 8.3452 * dT * ureg("Btu")
                energy_required += energy_to_heat_water
            energy_required_by_space["NO_SPACES_ASSIGNED"] = energy_required

    return energy_required_by_space
