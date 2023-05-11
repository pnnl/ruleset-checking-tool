# get_zone_peak_internal_load_floor_area
**Schema Version:** 0.0.21
**Description:** finds the peak coincident internal loads of a zone and returns the value in btu/h/ft2

**Inputs:** 
- **RMI**
- **zone**

**Returns:**  
- **result**: a dict giving 2 values: {"PEAK":total peak btu/h/ft2 in the zone, "AREA":total zone area} the total peak btu/sf is the internal coincident peak loads in all spaces in the zone
 
**Function Call:**
- **normalize_interior_lighting_schedules**


## Logic:

- create list of all loads in the zone.  Each load is an dict of: {"POWER": number, "SCHEDULE": schedule_values}, the peak in btu/h/ft2 takes into account the sensible and latent fraction, for where there are multiple internal_loads in a space, the schedule multiplier indicates the % of total of the internal load: `loads = []`
- create an area variable which will be the sum of all space areas: `zone_area = 0`
- For each space in zone: `for space in zone.spaces:`
	- add the space.floor_area to the area variable: `zone_area += space.floor_area`
	- create lights power variable for storing the total space lighting power: `lights_power = 0`
	- For each lighting object in the space: `for lights in space.interior_lighting:`
		- add the space lighting power to the lights_power & convert from W/ft2 to btu/hr: `lights_power += lights.power_per_area * 3.412142 * space.area`
	- create the dict for the lights: `lights_info = {"POWER":lights_power, "SCHEDULE": lights.lighting_multiplier_schedule.cooling_design_day_sequence}`
	- append the lights_info to the loads list: `loads.append(lights_info)`
	- get information for people & assume the units are already btu/hr: `people_info = {"POWER":space.number_of_occupants * (space.occupant_sensible_heat_gain + space.occupant_latent_heat_gain), "SCHEDULE": space.occupant_multiplier_schedule.cooling_design_day_sequence}`
	- append people_info to the list: `loads.append(people_info)`
	
	- For each internal load in space: `for internal_load in space.miscellaneous_equipment:`
		- get information for the miscellaneous_equipment (assume the units are W/sf and convert to btu/hr): `equipment_info = {"POWER":internal_load.power*3.412142 * load.sensible_fraction + internal_load.power*3.412142 * load.latent_fraction, "SCHEDULE":internal_load.multiplier_schedule.cooling_design_day_sequence}`
		- append equipment_info to the list: `loads.append(equipment_info)`

- create a variable "max_internal_load" and set it to a starting value of 0: `max_internal_load = 0`
- loop through all the hours of the year: `for hour in range(24):`
	- create variable for the value of internal loads for the hour: `internal_loads_this_hour = 0`
	- loop through each load: `for load in loads:`
		- calculate the total internal load for this hour for this object and add it to internal_loads_this_hour: `internal_loads_this_hour += load["POWER"] * load["SCHEDULE"][hour]`
	- check if internal_loads_this_hour is greater than max_internal_load: `if internal_loads_this_hour > max_internal_load:`
		- reset max_internal_load to internal_loads_this_hour: `max_internal_load = internal_loads_this_hour`

- create the result dictionary: `result = {"PEAK":max_internal_load, "AREA":zone_area}`


**Returns** `result`



**[Back](../_toc.md)**
