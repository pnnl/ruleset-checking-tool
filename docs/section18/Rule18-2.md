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
7. get_lab_zone_hvac_systems()


**Applicability Checks:**

## Rule Logic:  
- use the function get_baseline_system_types to get a dictionary of baseline system types and systems: `baseline_system_types_dict = get_baseline_system_types(B-RMD)`
- use the function get_dict_of_zones_and_terminal_units_served_by_hvac_sys to determine which zones are served by each system system: `zones_and_terminal_unit_list_dict = get_dict_of_zones_and_terminal_units_served_by_hvac_sys(B_RMD)`
- use the function get_zone_target_baseline_system to get the target baseline system types for each zone.  This will be used when checking for laboratory systems: `target_baseline_systems = get_zone_target_baseline_system(P_RMI, B_RMI)`
- use the function get_lab_zone_hvac_systems to get the list of hvac_ids for the systems that serve only lab zones: `lab_zone_hvac_systems = get_lab_zone_hvac_systems(B_RMI,P_RMI)`
- create a list of laboratory zones meeting G3_1_1d: `laboratory_zones_meeting_G3_1_1d = [x for x in target_baseline_systems if target_baseline_systems[x]["SYSTEM_ORIGIN"] == G3_1_1d`
- evaluate the rule for each HVAC system in the B_RMI: `for hvac_system in B_RMI...heating_ventilating_air_conditioning_systems:`
	- set the result to FAIL: `result = FAIL`
 	- create variable do_multi_zone_evaluation and set to true: `do_multi_zone_evaluation = TRUE`
	- find the hvac_system type by looking through the baseline_system_types_dict for the hvac_system.id: `for hvac_system_type in baseline_system_types_dict:`
		- find the actual system type of the system (for example, SYS_5 instead of SYS_5B).  Start by looping through the possible system types: `for possible_type in [SYS_1,SYS_2,SYS_3,SYS_4,SYS_5,SYS_6,SYS_7,SYS_8,SYS_9,SYS_10,SYS_11,SYS_12,SYS_13):`
			- set system_type to possible_type if the result of using the baseline_system_type_compare function is TRUE: `if baseline_system_type_compare(hvac_system_type,possible_type,FALSE): system_type = possible_type`
		- see if the hvac_system.id is in the list: `if hvac_system.id in? baseline_system_types_dict[hvac_system_type]:`
  			- Get the list of zones served by the system from zones_and_terminal_unit_list_dict: `zones_served_by_system = zones_and_terminal_unit_list_dict[hvac_system.id]["ZONE_LIST"]`
     			- check if the system is a single-zone system type: `if any(system_type == sys_type for sys_type in [SYS_1,SYS_2,SYS_3,SYS_4,SYS_9,SYS_10,SYS_11,SYS_12,SYS_13]):`
     				- only systems that serve single zones can be categorized as single zone systems, so set result to pass and do_multi_zone_evalutation to FALSE: `result = PASS; do_multi_zone_evaluation = FALSE`
     			- otherwise it is a multi-zone system:`else:`
        			- we will deal first with the case of a system serving laboratory zones.  An hvac system serving laboratory zones needs to meet the following:
             				1.  can only serve lab zones
             				2.  serves ALL the lab zones
             				3.  is in a building with > 15,000cfm lab exhaust
             			- the function get_lab_zone_hvac_systems gets the hvac systems serving the lab zones.  If this system is in the list, AND it is the only one in the list, then this is a lab zone system: `if hvac_system.id in? lab_zone_hvac_systems["LAB_ZONES_ONLY"] && len(lab_zone_hvac_systems["LAB_ZONES_ONLY"]) == 1:`
                			- if we can tell with 100% certainty that the building has > 15,000 cfm lab exhaust this system can pass and do_multi_zone_evaluation to FALSE: `if building_total_lab_zone_exhaust > 15000: result = PASS; do_multi_zone_evaluation = FALSE`
                   			- otherwise, there *might* be > 15000 cfm exhaust, but we are not sure (the function get_lab_zone_hvac_systems relies on get_zone_target_baseline_system, which does the > 15000 cfm check, so we don't have to do it again): `else:`
                      				- set result to UNDETERMINED and do_multi_zone_evaluation to FALSE:  `result = UNDETERMINED; do_multi_zone_evaluation = FALSE`
       						- provide a note expaining the result: `note = "This system serves only lab zones, which is correct if the building has total lab exhaust greater than 15,000 cfm.  However, we could not determine with accuracy the total building exhuast."`
                		- otherwise if the hvac system is in the list (but there is more than one HVAC system): `elif hvac_system.id in? lab_zone_hvac_systems["LAB_ZONES_ONLY]:`
                			- if we can tell with 100% certainty that the building has > 15,000 cfm lab exhaust, set result to FAIL: `if building_total_lab_zone_exhaust > 15000:`
				                - set result to fail: `result = FAIL`
                     				- set do_multi_zone_evaluation to false FALSE: `do_multi_zone_evaluation = FALSE`
                      				- provide a note to explain the result: `note = "This HVAC system serves lab zones in a building with > 15,000 cfm of laboratory exhaust.  The baseline system should be type 5 or 7 and should serve ALL laboratory zones."`
                  		- otherwise, the hvac system might be a system that serves both lab zones and regular zones: `elif hvac_system.id in? lab_zone_havc_systems["LAB_AND_OTHER"]:`
                    			- if we can tell with 100% certainty that the building has > 15,000 cfm lab exhaust, set result to FAIL: `if building_total_lab_zone_exhaust > 15000:`
				                - set result to fail: `result = FAIL`
                      				- set do_multi_zone_evaluation to FALSE: `do_multi_zone_evaluation = FALSE`
                      				- provide a note to explain the result: `note = "This HVAC system serves lab zones in a building with > 15,000 cfm of laboratory exhaust.  The baseline system for laboratory zones should be type 5 or 7 and should serve only and all laboratory zones."`
                   			- otherwise, there *might* be > 15000 cfm exhaust, but we are not sure (the function get_lab_zone_hvac_systems relies on get_zone_target_baseline_system, which does the > 15000 cfm check, so we don't have to do it again): `else:`
                      				- set result to UNDETERMINED:  `result = UNDETERMINED`
                        			- set do_multi_zone_evaluation to FALSE: `do_multi_zone_evaluation = FALSE`
       						- provide a note expaining the result: `note = "This system serves some lab zones and some non-lab zones in a building which may have more than 15,000 cfm.  In buildings with > 15,000 cfm of lab exhaust, ALL and only lab zones should be served by system type 5 or 7."`
                      
                   		 - check do_multi_zone_evaluation to determine if this is a multi_zone system.  Continue checking whether all the zones it serves are on the same floor: `if do_multi_zone_evaluation:`
                      			- get the list of zones on the same floor by using the function get_zones_on_same_floor: `zones_on_floor = get_zones_on_same_floor(B_RMI,zones_served_by_system[0])`
					- check if all the zones served by the system are on the same floor: `if all(zone in zones_on_floor for zone in zones_served_by_system):`
						- set the result to PASS.  There are checks on the following lines that will set the result to fail a zone is also served by another system, or if the system serves lab zones: `result = PASS`
        					- now check if there are any other systems of the same system type that serve zones on this floor.  First loop through baseline_system_types_dict again: `for hvac_system_type2 in baseline_system_types_dict:`
							- check if the hvac_system_type2 is the same type: `if baseline_system_type_compare(hvac_system_type2,system_type,FALSE):`
								- look through all of the hvacs of this system type: `for hvac_system2_id in baseline_system_types_dict[hvac_system_type2]:`
									- make sure that hvac_system2_id is not the same as hvac_system_id: `if hvac_system2_id != hvac_system_id:`
										- now check if hvac_system2 serves any of the zones on the same floor as hvac_system.  Get the zones served by hvac_system2: `zones_served_by_system2 = zones_and_terminal_unit_list_dict[hvac_system2_id]["ZONE_LIST"]`
										- use set.intersection to see if any of these zones are on the same floor: `if(len(set(zones_served_by_system2).intersection(zones_on_floor))) > 0:`
											- the system fails: `result = FAIL`
	          									- UNLESS system_type is SYS_5 or SYS_7 AND all of the zones in hvac_system2 are lab zones: `if hvac_system2_id in? lab_zone_hvac_systems["LAB_ZONES_ONLY"] && len(lab_zone_hvac_systems["LAB_ZONES_ONLY"]) == 1 && lab_zone_exhaust > 15000: result = PASS`
	                   								- otherwise then if it's the only lab zone system, but we aren't sure about the exhaust air volume, result = UNDETERMINED: `if hvac_system2_id in? lab_zone_hvac_systems["LAB_ZONES_ONLY"] && len(lab_zone_hvac_systems["LAB_ZONES_ONLY"]) == 1: result = UNDETERMINED; note = "This HVAC system is on the same floor as " + hvac_system2_id + ", which serves lab zones in the building.  If the building has greater than 15,000 cfm of lab exhaust and " + hvac_system2_id + " is System type 5 or 7 serving only lab zones, this system passes, otherwise it fails"`
	                           							- otherwise the other system isn't a lab system, set result to fail: `result = FAIL`


					
  **Rule Assertion - Zone:**

  - Case 1: result is PASS: `if result == PASS: PASS`
  - Case 2: result is FAIL:`if result == FAIL: FAIL`
  - Case 3: result is UNDETERMIEND: `if result == UNDETERMIEND: UNDETERMIEND`
**Notes:**

**[Back](../_toc.md)**
