# baseline_system_type_compare

**Schema Version:** 0.0.23

**Description:** compares two enums, the baseline system type (usually given by get_baseline_system_types), which could could include a number or letter modifier beyond the basic system type, and a target system type enum, which will usually be simply "SYS-#".

**Inputs:**  
- **system_type**: the enum indicating the hvac system type example: SYS_5 or SYS_8c.  This will usually be the value given by the function get_baseline_system_types
- **target_system_type**: the enum indicating the target system type, will usually be SYS_# without a further number or letter modifier
- **exact_match**: a boolean, TRUE or FALSE.  if exact_match is TRUE, then the system type must match exactly the enum given by hvac_system_type.  If false, an approximate match will return true.  This would be used in the case where the user wants any hvac system ot type 8, without having to type in 8a, 8b, 8c.  In this case, SYS_8 would be passed to the function and the function would return TRUE for any system 8, regardless of it's 8a, 8b, or 8c

**Returns:**  
- **result**: TRUE or FALSE, indicating whether the hvac system type matches the hvac_system_type
 
**Function Call:**

- NONE

**CONSTANT or Lookup Table**

HVAC_SYSTEM_TYPE_DICTIONARY = {
	HVAC_SYS.SYS_1: [HVAC_SYS.SYS_1, HVAC_SYS.SYS_1A, HVAC_SYS.SYS_1B, HVAC_SYS.SYS_1C]
	HVAC_SYS.SYS_2: [HVAC_SYS.SYS_2]
	HVAC_SYS.SYS_3: [HVAC_SYS.SYS_3, HVAC_SYS.SYS_3A, HVAC_SYS.SYS_3B, HVAC_SYS.SYS_3C]
	HVAC_SYS.SYS_4: [HVAC_SYS.SYS_4]
	HVAC_SYS.SYS_5: [HVAC_SYS.SYS_5, HVAC_SYS.SYS_5B]
	HVAC_SYS.SYS_6: [HVAC_SYS.SYS_6, HVAC_SYS.SYS_6B]
	HVAC_SYS.SYS_7: [HVAC_SYS.SYS_7, HVAC_SYS.SYS_7A, HVAC_SYS.SYS_7B, HVAC_SYS.SYS_7C]
	HVAC_SYS.SYS_8: [HVAC_SYS.SYS_8, HVAC_SYS.SYS_8A, HVAC_SYS.SYS_8B, HVAC_SYS.SYS_8C]
	HVAC_SYS.SYS_9: [HVAC_SYS.SYS_9, HVAC_SYS.SYS_9B]
	HVAC_SYS.SYS_10: [HVAC_SYS.SYS_10]
	HVAC_SYS.SYS_11: [HVAC_SYS.SYS_11, HVAC_SYS.SYS_11_1, HVAC_SYS. SYS_11_1A , HVAC_SYS. SYS_11B , HVAC_SYS. SYS_11C, HVAC_SYS. SYS_11_2, HVAC_SYS. SYS_11_2A]
	HVAC_SYS.SYS_12: [HVAC_SYS.SYS_12, HVAC_SYS.SYS_12A, HVAC_SYS.SYS_12B, HVAC_SYS.SYS_12C]
	HVAC_SYS.SYS_13: [HVAC_SYS.SYS_13, HVAC_SYS.SYS_13A, HVAC_SYS.SYS_13B, HVAC_SYS.SYS_13C]
	}

## Logic:
- set result to false: `result = FALSE`
- check if the user is requiring an exact match: `if exact_match:`
  - simply compare the two variables: `if system_type == target_system_type:`
    - set the result to true: `result = TRUE`
- if the match is not exact: `else:`
  - we need to use the lookup dict to determine whether the system types match: `if system_type in HVAC_SYSTEM_TYPE_DICTIONARY[target_system_type]:`
    - set the result to true: `result = TRUE`
**Returns**  `return result`

**[Back](../_toc.md)**
