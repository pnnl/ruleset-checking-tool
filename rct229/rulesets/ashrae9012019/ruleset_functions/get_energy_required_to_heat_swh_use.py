import numpy as np
from pint import Quantity

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
    This function calculates the total energy required to heat the SWH use over the course of a year.  Note - this function does not work for service water heating uses with use_units == "OTHER".  In this case, it will return None.

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

    is_power_mode = use_units in {
        SERVICE_WATER_HEATING_USE_UNIT.POWER_PER_PERSON,
        SERVICE_WATER_HEATING_USE_UNIT.POWER_PER_AREA,
        SERVICE_WATER_HEATING_USE_UNIT.POWER,
    }
    is_volume_mode = use_units in {
        SERVICE_WATER_HEATING_USE_UNIT.VOLUME_PER_PERSON,
        SERVICE_WATER_HEATING_USE_UNIT.VOLUME_PER_AREA,
        SERVICE_WATER_HEATING_USE_UNIT.VOLUME,
    }

    # Common scalars
    swh_use_value_num = float(swh_use.get("use", 0.0))
    eq_hours_q = (
        equivalent_load_hours
        if hasattr(equivalent_load_hours, "to")
        else float(equivalent_load_hours) * ureg.hour
    )

    # Space vectors
    space_ids = [s["id"] for s in spaces]
    occupants = np.asarray(
        [s.get("number_of_occupants", 0) for s in spaces], dtype=float
    )
    areas_m2 = np.asarray(
        [
            (
                fa.to("m^2").magnitude
                if hasattr(fa := s.get("floor_area", ZERO.AREA), "to")
                else float(fa)
            )
            for s in spaces
        ],
        dtype=float,
    )

    energies_j = np.full(len(spaces), np.nan, dtype=float)

    # ---------------- POWER MODES (no ΔT) ----------------
    if is_power_mode:
        if use_units == SERVICE_WATER_HEATING_USE_UNIT.POWER_PER_PERSON:
            power_w = swh_use_value_num * ureg.watt
            energies_q = (
                (power_w * occupants)
                * eq_hours_q
                * (1 - drain_heat_recovery_efficiency)
            )
            energies_j = energies_q.to("J").magnitude

        elif use_units == SERVICE_WATER_HEATING_USE_UNIT.POWER_PER_AREA:
            pden_wm2 = swh_use_value_num * ureg("W/m^2")
            area_q = areas_m2 * ureg("m^2")
            energies_q = (
                (pden_wm2 * area_q) * eq_hours_q * (1 - drain_heat_recovery_efficiency)
            )
            energies_j = energies_q.to("J").magnitude

        elif use_units == SERVICE_WATER_HEATING_USE_UNIT.POWER:
            power_w = swh_use_value_num * ureg.watt
            energy_each = (
                (power_w * eq_hours_q * (1 - drain_heat_recovery_efficiency))
                .to("J")
                .magnitude
            )
            energies_j = np.full(len(spaces), energy_each, dtype=float)

    # ---------------- VOLUME MODES (ΔT needed) ----------------
    elif is_volume_mode:
        if (supply_temperature is not None) and (
            inlet_temperature_hourly_values is not None
        ):
            k = (
                (1 - drain_heat_recovery_efficiency)
                * WATER_DENSITY
                * WATER_SPECIFIC_HEAT
            ).to("J/(m^3*K)")
            k_mag = k.magnitude

            supply_c = (
                supply_temperature.to("degC").magnitude
                if hasattr(supply_temperature, "to")
                else float(supply_temperature)
            )

            inlet_c = np.asarray(
                [
                    (t.to("degC").magnitude if hasattr(t, "to") else float(t))
                    for t in inlet_temperature_hourly_values
                ],
                dtype=float,
            )

            hourly = np.asarray(hourly_multiplier_values, dtype=float)
            sum_hourly_delta_t = float(np.dot(hourly, (supply_c - inlet_c)))  # K·hr

            if use_units == SERVICE_WATER_HEATING_USE_UNIT.VOLUME_PER_PERSON:
                flow_m3_per_hr_per_person = (
                    (swh_use_value_num * ureg("L/hr")).to("m^3/hr").magnitude
                )
                volrate_m3_per_hr = flow_m3_per_hr_per_person * occupants
                energies_j = volrate_m3_per_hr * sum_hourly_delta_t * k_mag

            elif use_units == SERVICE_WATER_HEATING_USE_UNIT.VOLUME_PER_AREA:
                flow_m3_per_hr_per_m2 = (
                    (swh_use_value_num * ureg("L/hr/m^2")).to("m^3/hr/m^2").magnitude
                )
                volrate_m3_per_hr = flow_m3_per_hr_per_m2 * areas_m2
                energies_j = volrate_m3_per_hr * sum_hourly_delta_t * k_mag

            elif use_units == SERVICE_WATER_HEATING_USE_UNIT.VOLUME:
                volrate_m3_per_hr = (
                    (swh_use_value_num * ureg("L/hr")).to("m^3/hr").magnitude
                )
                energies_j = np.full(
                    len(spaces),
                    volrate_m3_per_hr * sum_hourly_delta_t * k_mag,
                    dtype=float,
                )

    energy_required_by_space = {}
    for space_id, energy_j in zip(space_ids, energies_j):
        energy_required_by_space[space_id] = (
            (energy_j * ureg.joule) if np.isfinite(energy_j) else None
        )

    if not spaces:  # Empty list: falsey

        energy_required_by_space["no_spaces_assigned"] = None

        if use_units == SERVICE_WATER_HEATING_USE_UNIT.OTHER:
            pass

        elif use_units == SERVICE_WATER_HEATING_USE_UNIT.POWER:
            power = swh_use.get("use", 0.0) * ureg.watt
            energy_required_by_space["no_spaces_assigned"] = (
                power * equivalent_load_hours * (1 - drain_heat_recovery_efficiency)
            )

        elif use_units == SERVICE_WATER_HEATING_USE_UNIT.VOLUME:
            if (supply_temperature is not None) and (
                inlet_temperature_hourly_values is not None
            ):
                k_mag = (
                    (
                        (1 - drain_heat_recovery_efficiency)
                        * WATER_DENSITY
                        * WATER_SPECIFIC_HEAT
                    )
                    .to("J/(m^3*K)")
                    .magnitude
                )

                supply_c = (
                    supply_temperature.to("degC").magnitude
                    if hasattr(supply_temperature, "to")
                    else float(supply_temperature)
                )

                inlet_c = np.asarray(
                    [
                        (t.to("degC").magnitude if hasattr(t, "to") else float(t))
                        for t in inlet_temperature_hourly_values
                    ],
                    dtype=float,
                )

                hourly = np.asarray(hourly_multiplier_values, dtype=float)
                if hourly.shape != inlet_c.shape:
                    raise ValueError(
                        "hourly_multiplier_values and inlet_temperature_hourly_values must have same length"
                    )

                # sum(hourly * ΔT)  (K·hr)
                sum_hourly_delta_t = float(np.dot(hourly, (supply_c - inlet_c)))

                # Volume mode uses a flow rate (L/hr)
                volrate_m3_per_hr = (
                    (swh_use.get("use", 0.0) * ureg("L/hr")).to("m^3/hr").magnitude
                )

                energy_j = volrate_m3_per_hr * sum_hourly_delta_t * k_mag
                energy_required_by_space["no_spaces_assigned"] = energy_j * ureg.joule

    return energy_required_by_space
