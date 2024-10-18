## get_energy_required_to_heat_swh_use

Description: This function calculates the total energy required to heat the SWH use over the course of a year in btu.  Note - this function does not work for service water heating uses with use_units == "OTHER".  In this case, it will return 0 Btu.

Inputs:
- **swh_use_id**
- **RMD**
- **building_segment_id**
- **is_leap_year**

Returns:
- **energy_required_by_space**: A dict where the keys are space_ids and values are the total energy required to heat the swh_use for that space.  If a swh_use is not assigned to any spaces, the key will be "NO_SPACES_ASSIGNED"

Function Call:

- get_spaces_served_by_SWH_use
- get_obj_by_id

Data Lookup: None

Logic:

- get the schedule: `hourly_schedule = swh_use.use_multiplier_schedule`
- get the distribution system: `distribution_system = swh_use.served_by_distribution_system`
- get the temperature at fixture: `supply_temperature = distribution_system.design_supply_temperature`
- get the water used: `swh_use_value = swh_use.use`
- get the inlet water temperature: `inlet_T_sched = distribution_system.entering_water_mains_temperature_schedule`
- set the drain heat recovery efficiency to 0: `drain_heat_recovery_efficiency = 0`
- get the drain heat recovery efficiency if heat is recovered by drain: `if(swh_use.is_heat_recovered_by_drain): drain_heat_recovery_efficiency = distribution_system.drain_heat_recovery_efficiency`
- get the use_units: `use_units = swh_use.use_units`

- now we need to get all of the spaces that the swh_use is applied to.  The convention is that if any spaces reference the swh_use, then the service water heating use applies to only those spaces. If no spaces reference the service water heating use, it applies to all spaces in the building segment.
- get the ids of spaces served by this swh_use: `space_ids = get_spaces_served_by_SWH_use(RMD, swh_use)`
- convert the space ids to spaces: `spaces = [get_obj_by_id(space_id, RMD) for space_id in space_ids]`
- if there are no spaces, and the use_units are anything other than POWER and VOLUME, the spaces list should include all spaces in the building segment: `if len(spaces) == 0 and use_units not in ["POWER","VOLUME"]: spaces = building_segment.spaces`
- create the dictionary: `energy_required_by_space = {}`
- calculate the energy for each space: `for space in spaces:`
  - convert the swh_water_used from whatever units it's currently in to volume (assumed to be gallons) OR, if the use units are one of the power types, calculate the energy required directly
  - if the use_units is POWER_PER_PERSON: `if use_units == "POWER_PER_PERSON":`
    - set power equal to the swh_use_value * number of occupants in the space: `power = swh_use_value * space.number_of_occupants`
    - in this case, swh_use_value is assumed to have units of btu/hr/person, so calculate energy_required by multiplying power (btu/hr) by the sum of the hourly_schedule: `energy_required = power * sum(hourly_schedule) * (1-drain_heat_recovery_efficiency)`
    - add this space to the dictionary: `energy_required_by_space[space.id] = energy_required`
  - otherwise if use_units is POWER_PER_AREA: `elsif use_units == "POWER_PER_AREA":`
    - set power equal to the swh_use_value * the floor area in the space: `power = swh_use_value * space.floor_area`
    - in this case, swh_use_value is assumed to have units of btu/hr/ft2, so calculate energy_required by multiplying power (btu/hr) by the sum of the hourly_schedule: `energy_required = power * sum(hourly_schedule) * (1-drain_heat_recovery_efficiency)`
    - add this space to the dictionary: `energy_required_by_space[space.id] = energy_required`
  - otherwise if use_units is POWER: `elsif use_units == "POWER":`
    - add this space to the dictionary - for power, the energy_required is equal to the swh_use_value times the hourly schedule: `energy_required_by_space[space.id] = swh_use_value * sum(hourly_schedule) * (1-drain_heat_recovery_efficiency)`
  - otherwise if use_units is VOLUME_PER_PERSON: `elsif use_units == "VOLUME_PER_PERSON":`
    - in this case swh_use_value is assumed to have the units of gallons/hr/person:
    - set volume_flow_rate equal to swh_use_value * the number occupants in the space: `volume_flow_rate = swh_use_value * space.number_of_occupants`
  - otherwise if use_units is VOLUME_PER_AREA: `elsif use_units == "VOLUME_PER_AREA":`
    - in this case swh_use_value is assumed to have the units of gallons/hr/ft2:
    - set volume_flow_rate equal to swh_use_value * the floor area of the space: `volume_flow_rate = swh_use_value * space.floor_area`
  - otherwise if use_units is VOLUME: `elsif use_units == "VOLUME":`
    - in this case swh_use_value is assumed to have the units gallons/hr
    - set volume_flow_rate equal to swh_use_value: `volume_flow_rate = swh_use_value`
  - if use_units is OTHER, set the result to UNDETERMINED: `if swh_use.use_units == "OTHER": energy_required_by_space[space.id] = "UNDETERMINED"`
  
  - at this point, either energy_required has been calculated or volume_flow_rate has been calculated.  If it's not energy_required, we need to calculate the energy required from volume_flow_rate: `if energy_required_by_space[space.id] == NULL:`
  - set energy_required to 0: `energy_required = 0`
  - iterate through each hourly value of the hourly_schedule: `for index, hourly_value in enumerate(hourly_schedule):`
    - set volume_this_hour equal to volume_flow_rate * hourly_value: `volume_this_hour = volume_flow_rate * hourly_value`
    - reduce volume_this hour by the recovery efficiency: `volume_this_hour = volume_this_hour * (1-drain_heat_recovery_efficiency)`
    - calculate the dT for the hour: `dT = supply_temperature - inlet_T_sched[index]`
    - now calculate the energy use to heat volume (gallons) of water - 1 Btu/lb/°F and 8.34 lb/gal of water: `energy_to_heat_water = volume_this_hour * 8.3452 * dT`
    - add the energy_to_heat_water to energy_required: `energy_required += energy_to_heat_water`
  - set the add this energy_required to energy_required_by_space: `energy_required_by_space[space.id] = energy_required`


- we still have a case where swh_use with VOLUME or POWER and not assigned to any spaces needs to be calculated.  Check if there are no spaces: `if len(spaces) == 0:`
  - check if swh_use.use_units is OTHER, if so, set value to UNDETERMINED: `if swh_use.use_units == "OTHER": energy_required_by_space["NO_SPACES_ASSIGNED"] = "UNDETERMINED"`
  - else, check if swh_use.use_units is POWER, if so, set value to POWER: `if swh_use.use_units == "POWER": energy_required_by_space["NO_SPACES_ASSIGNED"] = swh_use_value * sum(hourly_schedule) * (1-drain_heat_recovery_efficiency)`
  - else, check if swh_use.use_units is VOLUME, if so, we need to do the volume calculation: `if swh_use.use_units == "VOLUME":`
    - set energy_required to 0: `energy_required = 0`
    - iterate through each hourly value of the hourly_schedule: `for index, hourly_value in enumerate(hourly_schedule):`
      - set volume_this_hour equal to volume_flow_rate * hourly_value: `volume_this_hour = volume_flow_rate * hourly_value`
      - reduce volume_this hour by the recovery efficiency: `volume_this_hour = volume_this_hour * (1-drain_heat_recovery_efficiency)`
      - calculate the dT for the hour: `dT = supply_temperature - inlet_T_sched[index]`
      - now calculate the energy use to heat volume (gallons) of water - 1 Btu/lb/°F and 8.34 lb/gal of water: `energy_to_heat_water = volume_this_hour * 8.3452 * dT`
      - add the energy_to_heat_water to energy_required: `energy_required += energy_to_heat_water`
    - set the add this energy_required to energy_required_by_space: `energy_required_by_space["NO_SPACES_ASSIGNED"] = energy_required`

**Returns** energy_required_by_space

**[Back](../_toc.md)**

**Notes:**

1.  if use_units is OTHER - we need to be able to raise an error.
2.  relies on re-structuring of SWH as in: https://github.com/open229/ruleset-model-description-schema/issues/264

