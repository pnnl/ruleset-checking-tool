# get_zone_peak_internal_load_floor_area
**Schema Version:** 0.0.21
**Description:** finds the peak coincident internal loads of a zone and returns the value in btu/h/ft2

**Inputs:** 
- **RMI**
- **zone**

**Returns:**  
- **result**: a dict giving 2 values: {"PEAK":total peak btu/h/ft2 in the zone, "AREA":total zone area} the total peak btu/sf is the internal non-coincident peak loads in all spaces in the zone
 
**Function Call:**
- **normalize_interior_lighting_schedules**


## Logic:

- create a variable that gives the sum total of the loads in the zone in btu/hr: `zone_loads_btu_per_hr = 0`
- create an area variable which will be the sum of all space areas: `zone_area_sf = 0`
 
- For each space in zone: `for space in zone.spaces:`
	- add the space.floor_area to the area variable: `zone_area_sf += space.floor_area`
	- For each lighting object in the space: `for lights in space.interior_lighting:`
		- find the maximum value for the lighting schedule: `lighting_max_schedule_value = max(lights.lighting_multiplier_schedule.hourly_cooling_design_day)`
		- calculate the maximum lighting load and convert from W to btu/hr: `lighting_load_btu_per_hr = lights.power_per_area * 3.412142 * space.area * lighting_max_schedule_value`
		- add the space lighting power to the running total of zone loads: `zone_loads_btu_per_hr += lighting_load_btu_per_hr`

	- get the people maximum multiplier schedule for cooling design day: `people_max_schedule_value = max(space.occupant_multiplier_schedule.hourly_cooling_design_day)`
	- get information for people & assume the units are already btu/hr: `people_load_btu_per_hr = (space.occupant_sensible_heat_gain + space.occupant_latent_heat_gain) * people_max_schedule_value`
	- add the people load to the running total of zone loads: `zone_loads_btu_per_hr += people_load_btu_per_hr`
	
	- For each internal load in space: `for internal_load in space.miscellaneous_equipment:`
		- find the maximum value for the misc equipment schedule: `misc_max_schedule_value = max(internal_load.multiplier_schedule.hourly_cooling_design_day)`
		- calculate the maximum misc load and convert from W to btu/hr: `misc_load_btu_per_hr = internal_load.power * 3.412142 * misc_max_schedule_value`
		- add the space misc power to the running total of zone loads: `zone_loads_btu_per_hr += misc_load_btu_per_hr`

- create variable that gives the loads in btu/sf/hr: `zone_loads_btu_per_sf_per_hr = zone_loads_btu_per_hr / zone_area_sf`
- create the result dictionary: `result = {"PEAK":zone_loads_btu_per_sf_per_hr, "AREA":zone_area_sf}`


**Returns** `result`



**[Back](../_toc.md)**
