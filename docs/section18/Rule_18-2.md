# HVAC_SystemZoneAssignment - Rule 18-2 
**Schema Version:** 0.0.28  
**Mandatory Rule:** True  
**Rule ID:** 18-2  
**Rule Description:** Does the modeled system serve the appropriate zones (one system per zone for system types 1, 2, 3, 4, 9, 10, 11, 12, and 13 and one system per floor for system types 5, 6, 7, and 8, with the exception of system types 5 or 7 serving laboratory spaces - these systems should serve ALL laboratory zones in the buidling).  
**Rule Assertion:** Options are PASS/FAIL/NOT_APPLICABLE/UNDETERMINED  
**Appendix G Section:** Section 18 HVAC_SystemZoneAssignment  
**Appendix G Section Reference:** Table G3.1.1.3  

**Evaluation Context:** Each HVAC System  


**Manual Check:** Yes  
**Evaluation Context:** Evaluate whether each system serves the correct zones  
**Data Lookup:**   
**Function Call:** 

1. get_baseline_system_types()
2. get_zones_on_same_floor()
3. get_dict_of_zones_and_terminal_units_served_by_hvac_sys()
4. baseline_system_type_compare()
5. get_zone_target_baseline_system()
6. get_building_total_lab_exhaust_from_zone_exhaust_fan()


**Applicability Checks:**

## Rule Logic:  
- use the function get_baseline_system_types to get a dictionary of baseline system types and systems: `baseline_system_types_dict = get_baseline_system_types(B-RMI)`
- use the function get_dict_of_zones_and_terminal_units_served_by_hvac_sys to determine which zones are served by each system system: `zones_and_terminal_unit_list_dict = get_dict_of_zones_and_terminal_units_served_by_hvac_sys(B_RMI)`
- use the function get_zone_target_baseline_system to get the target baseline system types for each zone.  This will be used when checking for laboratory systems: `target_baseline_systems = get_zone_target_baseline_system(P_RMI, B_RMI)`
- use the function get_building_total_lab_exhaust_from_zone_exhaust_fan to get the totat lab exhaust air flow from zone exhaust fans.  This will be used when checking for laboratory systems: `lab_zone_exhaust = get_building_total_lab_exhaust_from_zone_exhaust_fan(P_RMI)`
- create a list of laboratory zones meeting G3_1_1d: `laboratory_zones_meeting_G3_1_1d = [x for x in target_baseline_systems if target_baseline_systems[x]["SYSTEM_ORIGIN"] == G3_1_1d]`
- evaluate the rule for each HVAC system in the B_RMI: `for hvac_system in B_RMI...heating_ventilating_air_conditioning_systems:`
	- set the result to FAIL: `result = FAIL`
	- find the hvac_system type by looking through the baseline_system_types_dict for the hvac_system.id: `for hvac_system_type in baseline_system_types_dict:`
		- find the actual system type of the system (for example, SYS_5 instead of SYS_5B).  Start by looping through the possible system types: `for possible_type in [SYS_1,SYS_2,SYS_3,SYS_4,SYS_5,SYS_6,SYS_7,SYS_8,SYS_9,SYS_10,SYS_11,SYS_12,SYS_13):`
			- set system_type to possible_type if the result of using the baseline_system_type_compare function is TRUE: `if baseline_system_type_compare(hvac_system_type,possible_type,FALSE): system_type = possible_type`
		- see if the hvac_system.id is in the list: `if hvac_system.id in? baseline_system_types_dict[hvac_system_type]:`
  			- Get the list of zones served by the system from zones_and_terminal_unit_list_dict: `zones_served_by_system = zones_and_terminal_unit_list_dict[hvac_system.id]["ZONE_LIST"]`
     			- check if the system is a single-zone system type: `if any(system_type == sys_type for sys_type in [SYS_1,SYS_2,SYS_3,SYS_4,SYS_9,SYS_10,SYS_11,SYS_12,SYS_13]):`
     				- only systems that serve single zones can be categorized as single zone systems, so set result to pass: `result = PASS`
     			- otherwise it is a multi-zone system:`else:`
					- for a multi-zone system, in a building without lab zones, the system can pass if:
						1. all zones are on the same floor
						2. there are no other systems of the same type that serve zones on the same floor
					- get the list of zones on the same floor by using the function get_zones_on_same_floor: `zones_on_floor = get_zones_on_same_floor(B_RMI,zones_served_by_system[0])`
					- check if all the zones served by the system are on the same floor: `if all(zone in zones_on_floor for zone in zones_served_by_system):`
						- now check if there are any other systems of the same system type that serve zones on this floor.  First loop through baseline_system_types_dict again: `for hvac_system_type2 in baseline_system_types_dict:`
							- check if the hvac_system_type2 is the same type: `if baseline_system_type_compare(hvac_system_type2,system_type,FALSE):`
								- look through all of the hvacs of this system type: `for hvac_system2_id in baseline_system_types_dict[hvac_system_type2]:`
									- make sure that hvac_system2_id is not the same as hvac_system_id: `if hvac_system2_id != hvac_system_id:`
										- now check if hvac_system2 serves any of the zones on the same floor as hvac_system.  Get the zones served by hvac_system2: `zones_served_by_system2 = zones_and_terminal_unit_list_dict[hvac_system2_id]["ZONE_LIST"]`
										- use set.intersection to see if any of these zones are on the same floor: `if(len(set(zones_served_by_system2).intersection(zones_on_floor))) > 0:`
											- the system fails, UNLESS system_type is SYS_5 or SYS_7 AND all of the zones in hvac_system2 are lab zones.  Set the result to fail, we'll check these special cases lower down and change the result back to pass if it passes: `result = FAIL`
											- check if the system type is 5 or 7: `if any(system_type == sys_type for sys_type in [SYS_5,SYS_7]):`
												- check if all of the zones served by hvac_system are lab zones: `if set(laboratory_zones_meeting_G3_1_1d) == set(zones_served_by_system):`
													- check if the building has greater than 15,000 cfm lab exhaust.  If so, set result to PASS.  If not, set result to UNDETERMINED: `if lab_zone_exhaust > 15000: result = TRUE`
													- else set result to UNDETERMINED: `result = UNDETERMINED`
												- else check if all of the zones served by hvac_system2 are lab zones: `if set(laboratory_zones_meeting_G3_1_1d) == set(zones_served_by_system2):`
													- check if the building has greater than 15,000 cfm lab exhaust.  If so, set result to PASS.  If not, set result to UNDETERMINED: `if lab_zone_exhaust > 15000: result = TRUE`
													- else set result to UNDETERMINED: `result = UNDETERMINED`
						- at this point, there is still one case we haven't handled - a system that is not type 5 or 7 and incorrectly serves a lab type zone.  This could be the case if the result is currently PASS: `if result == PASS:`
							- create the intersection between the zones_served_by_system and laboratory_zones_meeting_G3_1_1d: `lab_zones_served_by_system = set(zones_served_by_system).intersection laboratory_zones_meeting_G3_1_1d`
							- if the number of lab_zones_served_by_system is a number between 0 and the number of zones_served_by_system, then this system may be erroneously serving a lab zone: `if 0 < len(lab_zones_served_by_system) < len(zones_served_by_system:`
								- if the lab zone exhaust is greater than 15,000 cfm, then this is a hard fail: `if lab_zone_exhaust > 15000: result = FAIL`
								- otherwise set the result to UNDETERMINED: `result = UNDETERMINED`
					- otherwise, if not all zones are on the same floor, this could be OK if the system is type 5 or 7, the building has > 15000 cfm lab exhaust and the system serves all lab zones: `if any(system_type == sys_type for sys_type in [SYS_5,SYS_7]):`
						- check if the system serves all the laboratory zones: `if set(laboratory_zones_meeting_G3_1_1d) == set(zones_served_by_system):`
							- set result to UNDETERMINED.  The result will be set to PASS in the next step if we can 100% determine that the building has greater than 15000 cfm lab exhaust: `result = UNDETERMINED`
							- check if the building has greater than 15,000 cfm lab exhaust.  If so, set result to PASS.  If not, set result to UNDETERMINED: `if lab_zone_exhaust > 15000: result = PASS`
					
  **Rule Assertion - Zone:**

  - Case 1: result is PASS: `if result == PASS: PASS`
  - Case 2: result is FAIL:`if result == FAIL: FAIL`
  - Case 3: result is UNDETERMIEND: `if result == UNDETERMIEND: UNDETERMIEND; note = "the building includes laboratory zones and may have a total building laboratory exhaust air flow rate greater than 15,000cfm.  We are not able to determine with 100% accuracy if the building has greater than 15000cfm of laboratory exhaust.  An undetermined result was given because this system serves laboratory zones.  If the building has greater than 15,000cfm laboratory exhaust, all laboratory zones should be served by one system type 5 or 7.`
**Notes:**

**[Back](../_toc.md)**
