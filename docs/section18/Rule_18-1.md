# HVAC_SystemZoneAssignment - Rule 18-1
**Schema Version:** 0.0.28  
**Mandatory Rule:** True  
**Rule ID:** 18-1  
**Rule Description:** HVAC system type selection is based on ASHRAE 90.1 G3.1.1 (a-h)  
**Rule Assertion:** Options are PASS/FAIL/NOT_APPLICABLE
**Appendix G Section Reference:** Table G3.1.1

**Evaluation Context:** Each Zone Data Group
**Data Lookup:**   
**Function Call:** 

1. get_zone_target_baseline_system()
2. baseline_system_type_compare()
3. get_list_hvac_systems_associated_with_zone()
4. get_baseline_system_types()


**Applicability Checks:**
- call the function get_zone_target_baseline_system(): `target_baseline_system_dict = get_zone_target_baseline_system(P_RMI, B_RMI)`
- if the zone is conditioned and not dedicated to parking, the rule is applicable - the zone will only be in the dictionary provided by get_zone_target_baseline_system() if it is a zone which requires an HVAC system: `if zone in target_baseline_system_dict: continue to rule logic`
- otherwise: `else: result = NOT_APPLICABLE`

## Rule Logic:  
- set the result to fail: `result = FAIL`
- set expected_system_type to the expected system type given by the target_baseline_system_dict: `expected_system_type = target_baseline_system_dict[zone]["EXPECTED_SYSTEM_TYPE"]`
- set the system_type_origin to the SYSTEM_ORIGIN given by the target_baseline_system_dict: `system_type_origin = target_baseline_system_type_dict[zone]["SYSTEM_ORIGIN"]
- get the baseline system types in the building: `baseline_hvac_system_dict = get_baseline_system_types(B-RMI)`
- now check whether the system(s) serving this zone match the expected system.  Start by getting the list of HVAC systems that serve the zone: `hvac_systems_serving_zone = get_list_hvac_systems_associated_with_zone(B-RMI)`
- get a list of all of the HVAC systems that are of the same type as the expected system type for the zone: `systems_of_expected_type_list = baseline_hvac_system_dict[expected_system_type]`
- loop through the systems that serve the zone: `for system_b in hvac_systems_serving_zone:`
	- check to see if system_b is in the systems_of_expected_type_list, set result to PASS: `if system_b in systems_of_expected_type_list: result = PASS`


 - for most zones, we can simply return the result at this point, but there are some special cases that require a check for whether an UNDETERMINED needs to be returned.  We need to do further work in the case of laboratories (G3_1_1d) and vestibules (G3_1_1e)
 - check if the system_type_origin is "G3_1_1d" we need to determine whether the laboratory exhaust meets the threshold based solely on zone exhaust or not: `if system_type_origin == "G3_1_1d:"
	- complete logic to determine whether we can give a hard PASS / FAIL or simply UNDETERMINED
 - otherwise, if the system_type_origin is "G3_1_1e" we need to determine whether the zone in question is one that is potentially a vestibule.  We can't determine with 100% certainty if a zone is a vestibule, and if the HVAC system type is selected based on the fact that it might be a vestibule, then we can't determine with 100% accuracy a pass or fail: `elsif system_type_origin == "G3_1_1e":`
	 - complete logic to determine whether we can give a hard PASS / FAIL or simply undetermined


**Notes:**
1. this rule is written such that if at least one system serving the zone is the expected type, it passes.  In Appendix G, only one system per zone is allowed in the baseline model, however, this is covered by another rule.
2. I strongly feel that if the system types don't match, we need to provide logic to tell the user why they don't match.  The details of how to set up the various baseline system types can be seen as "rules" that are not reflected elsewhere in the schema.

## Rule Logic:  
- This function uses get_zone_target_baseline_system and looks through the list to find any zones that match the target string for this system.
- The target string is: `target_string = "PUBLIC_ASSEMBLY CZ_0_to_3a < 120,000 ft2"`
- the expected system type is "SYS-4": `expected_system_type = "SYS-4"`

- loop through building segments: `for segment in RMR.building_segments:`
	- loop through zones in the segments: `for zone in segment.zones:`
		- use the section_18_rule_test function to determine whether the zone meets the requirements: `zone_result = section_18_rule_test(P-RMD,B-RMD,zone.id,target_string,expected_system_type)`


  **Rule Assertion - Zone:**

  - Case 1: the target strings don't match, so it is not applicable to this zone: `if zone_result == NOT_APPLICABLE: NOT_APPLICABLE`
  - Case 2: All terminals in the zone are System-4 (there should only be one terminal in the zone, but this rule doesn't check number of terminals):`if zone_result == PASS: PASS`

  - Case 3: Else: `else: FAIL`

**Notes:**


# section_18_rule_test

**Description:** uses the function get_zone_target_baseline_system to get the targets for the entire building.  Accepts two enum values as inputs, one is the system type expected by the rule (ex: SYS_3,SYS_7), and the other is the target enum, which is used to determine if the rule calling the function was the one used to set the system designation

**Inputs:**  
- **P-RMI**: The proposed RMI
- **B-RMI**: The baseline RMI
- **zone_id**: the id of the zone to be tested
- **expected_system_type** - an enum describing the system type expected by the rule calling this function (ex: SYS_2)
- **target_string** - the target string, which will match if this rule was the one used to designate the system (ex: "PUBLIC_ASSEMBLY CZ_3b_3c_or_4_to_8 < 120,000 ft2")


**Returns:**  
- **result**: enum indicating PASS, FAIL, NOT_APPLICABLE
 
**Function Call:** 

1. get_zone_target_baseline_system()
2. baseline_system_type_compare()
3. get_list_hvac_systems_associated_with_zone()
4. get_baseline_system_types()

## Logic:  
- get the zone: `zone = get_component_by_id(B-RMI,zone_id)`
- check if the zone conditioning category is UNCONDITIONED: `if zone.conditioning_type == UNCONDITIONED:
	- if so the rule is NOT_APPLICABLE: `result = NOT_APPLICABLE`
- otherwise, continue with logic: `else:`
	- get the baseline system types in the building: `baseline_hvac_system_dict = get_baseline_system_types(B-RMI)`

	- get the expected system type using `get_zone_target_baseline_system()`: `zones_expected_system_types = get_zone_target_baseline_system(P-RMI,B-RMI)`
	- check whether the description string in zones_expected_system_types matches the target_string: `if zones_expected_system_types[zone]["SYSTEM_ORIGIN"] == target_string:`
		- now check whether the system(s) serving this zone match the expected system.  Start by getting the list of HVAC systems that serve the zone: `hvac_systems_serving_zone = get_list_hvac_systems_associated_with_zone(B-RMI)`
			- set result to PASS: `result = NO_MATCH`
			- loop through these systems: `for system_b in hvac_systems_serving_zone:`
				- loop through the baseline_hvac_system_dict looking for the expected system type - if any of the baseline HVAC systems do not match the expected system type result will be set to FAIL: `for hvac_system_type in baseline_hvac_system_dict:`
					- check if the system_b is one of the systems: `if system_b in baseline_hvac_system_dict[hvac_system_type]:`
						- check if hvac_system type is the same type (or one of the sub-types of expected_system_type: `if baseline_system_type_compare(hvac_system_type, expected_system_type, false):`
							- this system passes, set result to pass only if result is currently NO_MATCH: `if result == NO_MATCH: result = PASS`
						- otherwise, the system does not match, set result to FAIL: `else: result = FAIL`
	- if the strings don't match, this is not applicable: `else: result = NOT_APPLICABLE`
	- if none of the systems serving the zone were assigned a system type, then at this point result will still be NO_MATCH.  If result is still NO_MATCH, re-assign it to FAIL (no matching system types were found: `if result == NO_MATCH: result = FAIL`

 **Returns** `return result`  

**[Back](../_toc.md)**



**[Back](../_toc.md)**
