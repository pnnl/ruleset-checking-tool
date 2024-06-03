
## get_energy_required_to_heat_swh_use

Description: This function calculates the total energy required to heat the SWH use over the course of a year in btu

Inputs:
- **swh_use**
- **space**

Returns:
- **energy_required**: A fixnum indicating the total btu required to heat the water indicated by the swh_use

Function Call:

- 

Data Lookup: None

Logic:

- get the schedule: `hourly_schedule = swh_use.use_multiplier_schedule`
- get the temperature at fixture: `temp_at_fixture = shw_use.temperature_at_fixture`
- get the distribution system: `distribution_system = shw_use.served_by_distribution_system`
- get the water used: `swh_use_value = swh_use.use`
- get the inlet water temperature: `inlet_T_sched = distribution_system.entering_water_mains_temperature_schedule`
- set the drain heat recovery efficiency to 0: `drain_heat_recovery_efficiency = 0`
- get the drain heat recovery efficiency if heat is recovered by drain: `if(swh_use.is_heat_recovered_by_drain): drain_heat_recovery_efficiency = distribution_system.drain_heat_recovery_efficiency`
- get the use_units: `use_units = swh_use.use_units`
- convert the shw_water_used from whatever units it's currently in to volume (assumed to be gallons) OR, if the use units are one of the power types, calculate the energy required directly
- if the use_units is POWER_PER_PERSON: `if use_units == "POWER_PER_PERSON":`
  - set power equal to the swh_use_value * space.number_of_occupants: `power = swh_use_value * space.number_of_occupants`
  - in this case, swh_use_value is assumed to have units of btu/hr/person, so calculate energy_required by multiplying power (btu/hr) by the sum of the hourly_schedule: `energy_required = power * sum(hourly_schedule)`
  - return energy_required: `return energy_required`
- otherwise if use_units is POWER_PER_AREA: `elsif use_units == "POWER_PER_AREA":`
  - set power equal to the swh_use_value * space.floor_area: `power = swh_use_value * space.floor_area`
  - in this case, swh_use_value is assumed to have units of btu/hr/ft2, so calculate energy_required by multiplying power (btu/hr) by the sum of the hourly_schedule: `energy_required = power * sum(hourly_schedule)`
  - return energy_required: `return energy_required`
- otherwise if use_units is POWER: `elsif use_units == "POWER":`
  - in this case, swh_use_value is assumed to have units of btu/hr, so calculate energy_required by multiplying swh_use_value by the sum of the hourly_schedule: `energy_required = swh_use_value * sum(hourly_schedule)`
  - return energy_required: `return energy_required`
- otherwise if use_units is VOLUME_PER_PERSON: `elsif use_units == "VOLUME_PER_PERSON":`
  - in this case swh_use_value is assumed to have the units of gallons/hr/person:
  - set volume_flow_rate equal to swh_use_value * space.number_of_occupants: `volume_flow_rate = swh_use_value * space.number_of_occupants`
- otherwise if use_units is VOLUME_PER_AREA: `elsif use_units == "VOLUME_PER_AREA":`
  - in this case swh_use_value is assumed to have the units of gallons/hr/ft2:
  - set volume_flow_rate equal to swh_use_value * space.area: `volume_flow_rate = swh_use_value * space.area`
- otherwise if use_units is VOLUME: `elsif use_units == "VOLUME":`
  - in this case swh_use_value is assumed to have the units gallons/hr
  - set volume_flow_rate equal to swh_use_value: `volume_flow_rate = swh_use_value`

- set energy_required to 0: `energy_required = 0`
- iterate through each hourly value of the hourly_schedule: `for index, hourly_value in enumerate(hourly_schedule):`
  - set volume_this_hour equal to volume_flow_rate * hourly_value: `volume_this_hour = volume_flow_rate * hourly_value`
  - reduce volume_this hour by the recovery efficiency: `volume_this_hour = volume_this_hour * (1-drain_heat_recovery_efficiency)`
  - calculate the dT for the hour: `dT = temp_at_fixture - inlet_T_sched[index]`
  - now calculate the energy use to heat volume (gallons) of water - 1 Btu/lb/°F and 8.34 lb/gal of water: `energy_to_heat_water = volume_this_hour * 8.3452 * dT`
  - add the energy_to_heat_water to energy_required: `energy_required += energy_to_heat_water`

**Returns** energy_required

**[Back](../_toc.md)**

**Notes:**

1.  if use_units is OTHER - we need to be able to raise an error.
2.  

