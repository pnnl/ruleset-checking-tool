# does_zone_meet_G3_1_1c

**Schema Version:** 0.0.21

**Description:** determines whether a given zone meets the G3_1_1c exception "If the baseline HVAC system type is 5, 6, 7, 8, 9, 10, 11, 12, or 13 use separate single-zone systems conforming with the requirements of system 3 or system 4 (depending on building heating source) for any spaces that have occupancy or process loads or schedules that differ significantly from the rest of the building. Peak thermal loads that differ by 10 Btu/h·ft2 (2.930710 W/sf) or more from the average of other spaces served by the system, or schedules that differ by more than 40 equivalent full-load hours per week from other spaces served by the system, are considered to differ significantly. Examples where this exception may be applicable include but are not limited to natatoriums and continually occupied security areas. This exception does not apply to computer rooms."
"average" is not particularly well defined in this exception. 
for the peak W/sf calculation I've assumed:
	1. the zone being tested is not included
 	2. the average: (each space coincident peak W) / total_area

**Inputs:** 
- **B_RMI**
- **zone_id**
- **starting_system_type** - this is the expected system type that was selected prior to checking G3_1_1c exception

**Returns:**  
- **result**: an enum - either YES or NO

**Function Call:**
- **get_zone_peak_internal_load**
- **get_hvac_zone_list_w_area**
- **find_zone**
- **get_zone_eflh**
- **zones_with_computer_room_dict_x**
- **get_component_by_id(zone_id)**
- 

## Logic:
- set the result variable to "No" - only a positive test can give it a different value: `result = NO`
- check if it is a computer room zone (computer room zones are not eligible for this exception): `if result == YES:`
	- use the function zones_with_computer_room_dict_x to get a list of zones including computer rooms: `computer_room_zones_dict = zones_with_computer_room_dict_x(B_RMD)`
	- if the target_zone.id is in the computer_room_zones_dict, then this is a computer room zone and it is not eligible: `if target_zone.id in computer_room_zones_dict:`
	- set the result to NO: `result = NO`
	- return result
- get the target zone: `target_zone = get_component_by_id(zone_id)`
- first check if the system type is one of the following:
`eligible_primary_system_types = ["SYS-5","Sys-6","Sys-7","Sys-8","Sys-9","Sys-10","Sys-11","Sys-12","Sys-13"]`
- check if the starting_system_type is in the list of eligible system types: `if starting_system_type in eligible_primary_system_types:`
	- the eligible system types are all systems that serve an entire floor, so we are comparing the target zone with all the other zones on this floor.
	- create a variable to hold the sum total of all peak loads in the system:`system_total_peak_load = 0`
	- create a variable to hold the sum total of the system area:`system_total_area = hvac_zone_list_w_area[eligible_system.id]["TOTAL_AREA"]`
	- create a list of the EFLH's for each zone `eflh = []`
	- loop through all zones in the RMI: `for zone in B-RMI..zones:`
		- check if this zone is on the same floor as the target zone: `if zone.floor_name == target_zone.floor_name:`
			- check that zone_b is not the zone being investigated: `if zone != target_zone:`
				- add the zone internal loads to the system_total_peaks: `system_total_peak += get_zone_peak_internal_load(zone_b)`
				- get the zone eflh by using the get_zone_eflh function.  This returns eflh for the year, so we need to convert to weeks by dividing by 52.1428: `zone_eflh = get_zone_eflh(zone)/52.1428`
				- add the eflh to the eflh list.  We are multiplying the schedule by the zone area so that later we can divide the total by the total area.  Otherwise small zones with very different schedules have too great an impact
				`eflh.append(zone_eflh * a[1])`
	- now calculate the average internal load per floor area: `internal_load_per_floor_area  = system_total_peak / system_total_area`
	- and calculate the averge eflh: `avg_eflh = sum(eflh)/len(eflh)`
	- get the internal load of the reference zone: `internal_loads = get_zone_peak_internal_load(target_zone)`
	- now do the rule checks:
	- if the zone peak differs by more than 10 btu/hr/sf from the average, then it meets the exception:
	`if(abs(internal_loads[0]/internal_loads[1] - internal_load_per_floor_area ) > 10):
		- it meets the exception: `result = YES`
	- OR if the eflh differs by more than 40, then the target_zone meets this exception:
	`if(abs(internal_loads[2] - avg_eflh) > 40):
		- it meets the exception: `result = YES`
	- at this point, if the result is not equal to YES, the target_zone doesn't meet the requirements and we should return the negative result without checking other systems: `return result`


**Returns** `result`

**[Back](../_toc.md)**
