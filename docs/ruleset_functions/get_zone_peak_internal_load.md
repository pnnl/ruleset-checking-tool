# get_zone_peak_internal_load

**Description:** finds the peak coincident internal loads of a zone and returns the value in W/sf

**Inputs:** 
- **RMR**
- **zone**

**Returns:**  
- **result**: an array giving 2 values: [total peak watts in the zone, total zone area] the total peak watts is the  of the internal coincident peak loads in all spaces in the zone
 
**Function Call:**
- **get_baseline_system_types**

## Logic:

- create list of all loads in the zone.  Each load is an array of: [the peak in W, schedule hourly values], the peak in W takes into account the sensible and latent fraction: `loads = []`
- create an area variable which will be the sum of all space areas: `zone_area = 0`
- For each space in zone: `for space in zone.spaces:`
	- add the space.floor_area to the area variable: `zone_area += space.floor_area`
	- get information for interior lighting: `lights = space.interior_lighting`
	- create the array for the lights: `lights_info = [space.area * lights.power_per_area, lights.lighting_multiplier_schedule.hourly_values]`
	- append the lights_info to the loads list: `loads.append(lights_info)`
	- get information for people: `people_info = [space.number_of_occupants * space.occupant_sensible_heat_gain, space.occupant_multiplier_schedule.hourly_values]`
	- append people_info to the list: `loads.append(people_info)`
	
	- For each internal load in space: `for internal_load in space.miscellaneous_equipment:`
		- get information for the miscellaneous_equipment: `equipment_info = [internal_load.power * load.sensible_fraction + internal_load.power * load.latent_fraction, internal_load.multiplier_schedule.hourly_values]`
		- append equipment_info to the list: `loads.append(equipment_info)`

- create a variable "max_internal_load" and set it to a starting value of 0: `max_internal_load = 0`
- loop through all the hours of the year: `for hour in range(8760):`
	- create variable for the value of internal loads for the hour: `internal_loads_this_hour = 0`
	- loop through each load: `for load in loads:`
		- calculate the total internal load for this hour for this object and add it to internal_loads_this_hour: `internal_loads_this_hour += load[0] * load[1][hour]
	- check if internal_loads_this_hour is greater than max_internal_load: `if internal_loads_this_hour > max_internal_load:`
		- reset max_internal_load to internal_loads_this_hour: `max_internal_load = internal_loads_this_hour`

- create the result array: `result = [max_internal_load, area]`


**Returns** `result`



**[Back](../_toc.md)**
