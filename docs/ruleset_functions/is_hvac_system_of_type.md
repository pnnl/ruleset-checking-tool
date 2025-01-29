# is_hvac_system_of_type

**Description:** takes an HVAC system type "SYS-1" through "SYS-13" WITHOUT the sub-system types (a,b,c,etc) and compares the first 5 letters in the `get_baseline_system_types` keys

**Inputs:**  
- **B-RMI**: The B-RMI to evaluate to get the list of the heating ventilaiton and cooling system ids associated with a zone in either the U_RMR, P_RMR, or B_RMR. 
- **hvac_system_id**: the id of the hvac system to be tested
- **target_system_type**: a string "SYS-1", "SYS-2", etc

**Returns:**  
- **result**: boolean true / false
 
**Function Call:** 
1.  get_baseline_system_types()

## Logic:
- get the list of all the baseline system types that exist in the baseline model: `baseline_system_types = get_baseline_system_types(B-RMI)`
- set result equal to false: `result = false`
- loop through the baseline_system_types: `for system_type in baseline_system_types:`
	- `system_type` is a string.  Compare the first 5 characters of this string to the target_system_type: `if system_type[0:5] == target_system_type:`
		- look for the hvac_system_id in this list: `if hvac_system_id.in baseline_system_types[system_type]`
			- the hvac system is of the target type, set result equal to true: `result = true`
			- we can return now, without continuing the loop: `return result`
- return result (which if we get here, will be false: `return result`

 **Returns** `return result`  

**[Back](../_toc.md)**
