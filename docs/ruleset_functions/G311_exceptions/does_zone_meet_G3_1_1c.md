# does_zone_meet_G3_1_1c

**Schema Version:** 0.0.21

**Description:** determines whether a given zone meets the G3_1_1c exception "If the baseline HVAC system type is 5, 6, 7, 8, 9, 10, 11, 12, or 13 use separate single-zone systems conforming with the requirements of system 3 or system 4 (depending on building heating source) for any spaces that have occupancy or process loads or schedules that differ significantly from the rest of the building. Peak thermal loads that differ by 10 Btu/h·ft2 (2.930710 W/sf) or more from the average of other spaces served by the system, or schedules that differ by more than 40 equivalent full-load hours per week from other spaces served by the system, are considered to differ significantly. Examples where this exception may be applicable include but are not limited to natatoriums and continually occupied security areas. This exception does not apply to computer rooms."
"average" is not particularly well defined in this exception. 
for the peak W/sf calculation I've assumed:
	1. the zone being tested is not included
 	2. the average: (each space coincident peak W) / total_area

**Inputs:** 
- **B_RMD**
- **zone**

**Returns:**  
- **result**: a string - either "C" or "No"
 
**Function Call:**
- **get_baseline_system_types**
- **get_zone_peak_internal_load**
- **get_list_hvac_systems_associated_with_zone**
- **get_hvac_zone_list_w_area**
- **find_zone**

## Logic:
- set the result variable to "No" - only a positive test can give it a different value: `result = "No"`
- use the function get_list_hvac_systems_associated_with_zone to get a list of all HVAC systems associated with the zone and make a list of hvac system ids:
`relevant_systems = [a.id for a in get_list_hvac_systems_associated_with_zone(B_RMD,zone.id)]`



- first check if the system type is one of the following:
`eligible_primary_system_types = ["SYS-5","SYS-5b","Sys-6","Sys-6b","Sys-7","Sys-7a","Sys-7b","Sys-7c","Sys-8","Sys-8a","Sys-8b","Sys-8c","Sys-8d","Sys-9","Sys-9b","Sys-10","Sys-11.1","Sys-11.1a","Sys-11b","Sys-11c","Sys-12","Sys-12a","Sys-12b","Sys-12c","Sys-13","Sys-13a"]`
- get the dict of get_baseline_system_types:
`system_types_b = get_baseline_system_types(B_RMD)`
- create a sub-list of system_types_b that includes only the system types and id references in the serving the zone:
`segment_system_types_b = {key: system_types_b[0] for key in system_types_b if(len(set(system_types_b[key])&set(relevant_systems)) > 0)`

- create set of system types that are eligible for this rule AND serve the zone:
`eligible_systems_in_zone = (set(segment_system_types_b) & set(eligible_primary_system_types))`
- check if any of the eligible_primary_system_types is in the system_types_b:
`if((len(eligible_systems_in_zone)) > 0):`
	- get the list of all systems and the zones they serve in the RMD by calling get_hvac_zone_list_w_area: `hvac_zone_list_w_area = get_hvac_zone_list_w_area(B_RMD)`
	- loop through each system in eligible_systems_in_zone: `for eligible_system in eligible_systems_in_zone:`
		- create a variable to hold the sum total of all peak loads in the system:
		`system_total_peak_load = 0`
		- create a variable to hold the sum total of the system area:
		`system_total_area = hvac_zone_list_w_area[eligible_system.id]["TOTAL_AREA"]`
		- create a list of the EFLH's for each zone `eflh = []`
		- get the list of zones associated with this system: `zones_associated_with_system = hvac_zone_list_w_area[eligible_system.id]["ZONE_LIST"]`
		- loop through the zones in the list: `for zone_id in zones_associated_with_system:`
			- find the zone using the find_zone function: `zone = find_zone(zone_id)`
				- check that zone_b is not the zone being investigated:
				`if zone_b != zone:`
					- add the zone internal loads to the system_total_peaks:
					`a = get_zone_peak_internal_load(zone_b)`
					`system_total_peak += a[0]`
					- add the eflh to the eflh list.  We are multiplying the schedule by the zone area so that later we can divide the total by the total area.  Otherwise small zones with very different schedules have too great an impact
					`eflh.append(a[2] * a[1])`
		- now calculate the average internal load: `avg_internal_load = system_total_peak / system_total_area`
		- and calculate the averge eflh: `avg_eflh = sum(eflh)/len(eflh)`
		- get the internal load of the reference zone: `internal_loads = get_zone_peak_internal_load(zone)`
		- now do the rule checks:
		- if the zone peak differs by more than 10 btu/hr/sf from the average, then it meets the exception:
		`if(abs(internal_loads[0]/internal_loads[1] - avg_internal_load) > 10):
			- it meets the exception: `result = "C"`
		- OR if the eflh differs by more than 40, then the zone meets this exception:
		`if(abs(internal_loads[2] - eflh) > 40):
			- it meets the exception: `result = "C"`
		- at this point, if the result is not equal to "C", the zone doesn't meet the requirements and we should return the negative result without checking other systems: `return result`


**Returns** `result`

**[Back](../_toc.md)**
