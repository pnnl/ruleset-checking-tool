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
