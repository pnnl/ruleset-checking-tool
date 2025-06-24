from pint import Quantity

from rct229.rule_engine.rulesets import LeapYear
from rct229.rulesets.ashrae9012019.ruleset_functions.get_spaces_served_by_swh_use import (
    get_spaces_served_by_swh_use,
)
from rct229.schema.config import ureg
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import assert_, getattr_
from rct229.utils.jsonpath_utils import find_all, find_exactly_one_with_field_value
from rct229.utils.pint_utils import ZERO
from rct229.utils.utility_functions import (
    find_exactly_one_schedule,
    find_exactly_one_service_water_heating_distribution_system,
    find_exactly_one_space,
    find_exactly_one_service_water_heating_use,
)

SERVICE_WATER_HEATING_USE_UNIT = SchemaEnums.schema_enums[
    "ServiceWaterHeatingUseUnitOptions"
]

REQUIRED_USE_UNIT = [
    SERVICE_WATER_HEATING_USE_UNIT.POWER,
    SERVICE_WATER_HEATING_USE_UNIT.VOLUME,
]

VOLUME_BASED_USE_UNIT = [
    SERVICE_WATER_HEATING_USE_UNIT.VOLUME_PER_PERSON,
    SERVICE_WATER_HEATING_USE_UNIT.VOLUME_PER_AREA,
    SERVICE_WATER_HEATING_USE_UNIT.VOLUME,
]

WATER_DENSITY = 8.3452 * ureg("lb/gallon")
WATER_SPECIFIC_HEAT = 1.001 * ureg("Btu/lb/delta_degF")


def get_energy_required_to_heat_swh_use(
    swh_use_id: str, rmd: dict, building_segment_id: str
) -> dict[str, Quantity | None]:
    """
    This function calculates the total energy required to heat the SWH use over the course of a year.  Note - this function does not work for service water heating uses with use_units == "OTHER".  In this case, it will return 0 Btu.

    Parameters
    ----------
    swh_use_id: str, id of service_water_heating_uses
    rmd: dict, RMD at RuleSetModelDescription level
    building_segment_id: str, id of building_segment


    Returns
    ----------
    energy_required_by_space: A dict where the keys are space_ids and values are the total energy required to heat the swh_use for that space.  If a swh_use is not assigned to any spaces, the key will be "no_spaces_assigned; if the swh_use.use_units == 'OTHER', the total energy required will be set to None"

    """
    swh_use = find_exactly_one_service_water_heating_use(rmd, swh_use_id)
    building_segment = find_exactly_one_with_field_value(
        "$.buildings[*].building_segments[*]", "id", building_segment_id, rmd
    )
    hourly_multiplier_schedule_id = swh_use.get("use_multiplier_schedule")
    hourly_multiplier_schedule = (
        find_exactly_one_schedule(rmd, hourly_multiplier_schedule_id)
        if hourly_multiplier_schedule_id is not None
        else None
    )

    is_heat_recovered_by_drain = swh_use.get("is_heat_recovered_by_drain", False)
    use_units = getattr_(swh_use, "service_water_heating_uses", "use_units")
    distribution_system = None
    inlet_temperature_hourly_values = None
    drain_heat_recovery_efficiency = 0.0
    supply_temperature = None
    if use_units in VOLUME_BASED_USE_UNIT or is_heat_recovered_by_drain:
        distribution_system_id = getattr_(
            swh_use, "service_water_heating_uses", "served_by_distribution_system"
        )
        distribution_system = (
            find_exactly_one_service_water_heating_distribution_system(
                rmd, distribution_system_id
            )
        )
    if use_units in VOLUME_BASED_USE_UNIT:
        supply_temperature = getattr_(
            distribution_system,
            "service_water_heating_distribution_systems",
            "design_supply_temperature",
        )
        inlet_temperature_schedule_id = getattr_(
            distribution_system,
            "service_water_heating_distribution_systems",
            "entering_water_mains_temperature_schedule",
        )
        inlet_temperature_schedule = find_exactly_one_schedule(
            rmd, inlet_temperature_schedule_id
        )
        inlet_temperature_hourly_values = getattr_(
            inlet_temperature_schedule, "schedules", "hourly_values"
        )
    if is_heat_recovered_by_drain:
        drain_heat_recovery_efficiency = getattr_(
            distribution_system,
            "service_water_heating_distribution_systems",
            "drain_heat_recovery_efficiency",
        )

        assert_(
            0.0 <= drain_heat_recovery_efficiency <= 1.0,
            "`drain_heat_recovery_efficiency` value must be between 0 and 1.",
        )

    space_id_list = get_spaces_served_by_swh_use(rmd, swh_use["id"])
    space_within_building_segment_id_list = find_all(
        "$.zones[*].spaces[*].id", building_segment
    )
    spaces = [
        find_exactly_one_space(rmd, space_id)
        for space_id in space_id_list
        if space_id in space_within_building_segment_id_list
    ]

    if not spaces and use_units not in REQUIRED_USE_UNIT:
        spaces = find_all("$.zones[*].spaces[*]", building_segment)

    # Infer number of hours in the year (from any valid schedule)
    num_hours = None
    for sched in find_all("$.schedules[*].hourly_values", rmd):
        if isinstance(sched, list) and len(sched) > 0:
            num_hours = len(sched)
            break
    if num_hours is None:
        num_hours = 8760  # fallback default

    hourly_multiplier_values = (
        getattr_(hourly_multiplier_schedule, "hourly_schedule", "hourly_values")
        if hourly_multiplier_schedule is not None
        else [1] * num_hours
    )
    equivalent_load_hours = sum(hourly_multiplier_values) * ureg("hr")

    swh_use_value = swh_use.get("use", 0.0)
    energy_required_by_space = {}
    for space in spaces:
        volume = ZERO.VOLUME
        space_id = space["id"]
        if use_units == SERVICE_WATER_HEATING_USE_UNIT.POWER_PER_PERSON:
            energy_required_by_space[space_id] = (
                swh_use_value
                * ureg("W")
                * space.get("number_of_occupants", 0)
                * equivalent_load_hours
                * (1 - drain_heat_recovery_efficiency)
            )

        elif use_units == SERVICE_WATER_HEATING_USE_UNIT.POWER_PER_AREA:
            energy_required_by_space[space_id] = (
                swh_use_value
                * ureg("W/m2")
                * space.get("floor_area", ZERO.AREA)
                * equivalent_load_hours
                * (1 - drain_heat_recovery_efficiency)
            )

        elif use_units == SERVICE_WATER_HEATING_USE_UNIT.POWER:
            energy_required_by_space[space_id] = (
                (swh_use_value * ureg("W"))
                * equivalent_load_hours
                * (1 - drain_heat_recovery_efficiency)
            )

        elif use_units == SERVICE_WATER_HEATING_USE_UNIT.VOLUME_PER_PERSON:
            volume = swh_use_value * ureg("L/hr") * space.get("number_of_occupants", 0)

        elif use_units == SERVICE_WATER_HEATING_USE_UNIT.VOLUME_PER_AREA:
            volume = (
                swh_use_value * ureg("L/hr/m2") * space.get("floor_area", ZERO.AREA)
            )

        elif use_units == SERVICE_WATER_HEATING_USE_UNIT.VOLUME:
            volume = swh_use_value * ureg("L/h")

        else:
            energy_required_by_space[space_id] = None

        # If unit is volume based
        if space_id not in energy_required_by_space:
            energy_required_by_space[space_id] = sum(
                [
                    (
                        volume
                        * hourly_value
                        * ureg("hr")
                        * (1 - drain_heat_recovery_efficiency)
                    )
                    * WATER_DENSITY
                    * WATER_SPECIFIC_HEAT
                    * (
                        supply_temperature
                        - inlet_temperature_hourly_values[index] * ureg("degC")
                    )
                    for index, hourly_value in enumerate(hourly_multiplier_values)
                ],
                ZERO.ENERGY,
            )

    if not spaces:  # Empty list: falsey
        if use_units == SERVICE_WATER_HEATING_USE_UNIT.OTHER:
            energy_required_by_space["no_spaces_assigned"] = None
        elif use_units == SERVICE_WATER_HEATING_USE_UNIT.POWER:
            energy_required_by_space["no_spaces_assigned"] = (
                (swh_use_value * ureg("W"))
                * equivalent_load_hours
                * (1 - drain_heat_recovery_efficiency)
            )

        elif use_units == SERVICE_WATER_HEATING_USE_UNIT.VOLUME:
            energy_required_by_space["no_spaces_assigned"] = sum(
                [
                    (
                        swh_use_value
                        * ureg("L")
                        * hourly_value
                        * ureg("hr")
                        * (1 - drain_heat_recovery_efficiency)
                    )
                    * WATER_DENSITY
                    * WATER_SPECIFIC_HEAT
                    * (
                        supply_temperature
                        - inlet_temperature_hourly_values[index] * ureg("degC")
                    )
                    for index, hourly_value in enumerate(hourly_multiplier_values)
                ],
                ZERO.ENERGY,
            )

    return energy_required_by_space
