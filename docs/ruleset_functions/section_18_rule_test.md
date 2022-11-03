# section_18_rule_test

**Description:** uses the function get_zone_target_baseline_system to get the targets for the entire building.  Accepts two string values as inputs, one is the system type expected by the rule ("SYS-3","SYS-7"), and the other is the target string, which is used to determine if the rule calling the function was the one used to set the system designation

**Inputs:**  
- **P-RMD**: The proposed RMD
- **B-RMD**: The baseline RMD
- **zone_id**: the id of the zone to be tested
- **expected_system_type** - a string describing the system type expected by the rule calling this function (ex: "SYS-2")
- **target_string** - the target string, which will match if this rule was the one used to designate the system (ex: "PUBLIC_ASSEMBLY CZ_3b_3c_or_4_to_8 < 120,000 ft2")


**Returns:**  
- **result**: enum indicating PASS, FAIL, NOT_APPLICABLE
 
**Function Call:** 

1. get_zone_target_baseline_system()
2. is_hvac_system_of_type()
3. get_list_hvac_systems_associated_with_zone()
4. is_hvac_system_of_type()

## Logic:  
- get the zone: `zone = get_component_by_id(zone_id)`
- get the expected system type using `get_zone_target_baseline_system()`: `zones_expected_system_types = get_zone_target_baseline_system(P-RMD,B-RMD)`
- check whether the description string in zones_expected_system_types matches the target_string: `if zones_expected_system_types[zone]["SYSTEM_ORIGIN"] == target_string:`
- now check whether the system(s) serving this zone match the expected system.  Start by getting the list of HVAC systems that serve the zone: `hvac_systems_serving_zone = get_list_hvac_systems_associated_with_zone(B-RMD)`
	- loop through these systems: `for system in hvac_systems_serving_zone:`
		- set result to PASS: `result = PASS`
		- now check that system_b is the expected type by using the is_hvac_system_of_type() function: `if is_hvac_system_of_type(B-RMI,system.id,expected_system_type):`
			- this system passes, no need to do anything (in the python code, the check above can be `not in` instead of `in`)
		- otherwise, this system is not compliant: `else:`
			- set the result to FAIL: `result = FAIL`
- if the strings don't match, this is not applicable: `else:`
	- the strings don't match, set result to NOT_APPLICABLE: `result = NOT_APPLICABLE`

 **Returns** `return result`  

**[Back](../_toc.md)**
