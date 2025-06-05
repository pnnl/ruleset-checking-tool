# does_zone_meet_G3_1_1c

**Schema Version:** 0.0.22

**Description:** determines whether a given zone meets the G3_1_1c exception "If the baseline HVAC system type is 5, 6, 7, 8 use separate single-zone systems conforming with the requirements of system 3 or system 4 (depending on building heating source) for any spaces that have occupancy or process loads or schedules that differ significantly from the rest of the building. Peak thermal loads that differ by 10 Btu/h·ft2 (2.930710 W/sf) or more from the average of other spaces served by the system, or schedules that differ by more than 40 equivalent full-load hours per week from other spaces served by the system, are considered to differ significantly. Examples where this exception may be applicable include but are not limited to natatoriums and continually occupied security areas. This exception does not apply to computer rooms."
"average" is not particularly well defined in this exception. 
for the peak W/sf calculation I've assumed:
	1. the zone being tested is not included
 	2. the average: (each space non-coincident peak W) / total_area

**Inputs:** 
- **B_RMD**
- **zone**
- **zones_and_systems** - this is a dict of the existing expected system types from the function `get_zone_target_baseline_system`

**Returns:**  
- **result**: boolean, True or False
 
**Function Call:**
- **get_zone_peak_internal_load**
- **get_zone_eflh**
- **zones_with_computer_room_dict_x**
- **get_zones_on_same_floor**

## Logic:
- set the result variable to "No" - only a positive test can give it a different value: `result = NO`

- first check if the system type is one of the following: `eligible_primary_system_types = ["SYS-5","SYS-6","SYS-7","SYS-8"]`
- check if the starting_system_type is in the list of eligible system types: `if zones_and_systems[zone]["EXPECTED_SYSTEM_TYPE"] in eligible_primary_system_types:`
	- get a list of zones that are on the same floor: `zones_on_same_floor = get_zones_on_same_floor(B_RMI,zone)`
	- create a list of zones that are on the same floor that have the same system type: `zones_on_same_system = []`
	- create a variable to hold the sum total of the system area:	`system_total_area = 0`
	- create a list of the EFLH's for each zone `eflh = []`
	- create a variable to hold the sum total of all peak loads in the system: `system_total_peak_load = 0`
	- loop through the zones in the zones_and_systems list: `for z in zones_and_systems:`
		- make sure that we don't include the original zone: `if z != zone:`
			- determine whether it is on the same floor: `if z in zones_on_same_floor:`
				- determine whether it has the same system type: `if zones_and_systems[z]["EXPECTED_SYSTEM_TYPE"] == zones_and_systems[zone]["EXPECTED_SYSTEM_TYPE"]:`
					- add the zone internal loads to the system_total_peaks: `a = get_zone_peak_internal_load(z)`
					`system_total_peak += a["PEAK"]`
					- get the zone eflh by using the get_zone_eflh function.  This returns eflh for the year, so we need to convert to weeks by dividing by 52.1428: `zone_eflh = get_zone_eflh(z)/52.1428`
					- add the eflh to the eflh list.  We are multiplying by the zone area so that later we can divide the total by the total area.  Otherwise small zones have too great an impact
					`eflh.append(zone_eflh * a["AREA"])`
		- now calculate the average internal load: `avg_internal_load = system_total_peak / system_total_area`
		- and calculate the averge eflh: `avg_eflh = sum(eflh)/system_total_area`
		- get the internal load of the reference zone: `internal_loads = get_zone_peak_internal_load(zone)`
		- now do the rule checks:
		- if the zone peak differs by more than 10 btu/hr/sf from the average, then it meets the exception:
		`if(abs(internal_loads["PEAK"]/internal_loads["AREA"] - avg_internal_load) > 10):
			- it meets the exception: `result = YES`
		- OR if the eflh differs by more than 40, then the zone meets this exception:
		`if(abs(get_zone_eflh(zone) - avg_eflh) > 40):
			- it meets the exception: `result = YES`
		- if the zone is still eligible, check if it is a computer room zone (computer room zones are not eligible for this exception): `if result == YES:`
			- use the function zones_with_computer_room_dict_x to get a list of zones including computer rooms: `computer_room_zones_dict = zones_with_computer_room_dict_x(B_RMD)`
			- if the zone.id is in the computer_room_zones_dict, then this is a computer room zone and it is not eligible: `if zone.id in computer_room_zones_dict:`
				- set the result to NO: `result = NO`
		- at this point, if the result is not equal to YES, the zone doesn't meet the requirements and we should return the negative result without checking other systems: `return result`


**Returns** `result`

**[Back](../_toc.md)**
