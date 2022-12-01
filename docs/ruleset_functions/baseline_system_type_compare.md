# baseline_system_type_compare

**Schema Version:** 0.0.23

**Description:** compares two strings, the baseline system type (usually given by get_baseline_system_types), which could could include a number or letter modifier beyond the basic system type, and a target system type string, which will usually be simply "SYS-#".

**Inputs:**  
- **system_type**: the string indicating the hvac system type example: "SYS-5" or "SYS-8c".  This will usually be the value given by the function get_baseline_system_types
- **target_system_type**: the string indicating the target system type, will usually be "SYS-#" without a further number or letter modifier
- **exact_match**: a boolean, TRUE or FALSE.  if exact_match is TRUE, then the system type must match exactly the string given by hvac_system_type.  If false, an approximate match will return true.  This would be used in the case where the user wants any hvac system ot type 8, without having to type in 8a, 8b, 8c.  In this case, "SYS-8" would be passed to the function and the function would return TRUE for any system 8, regardless of it's 8a, 8b, or 8c

**Returns:**  
- **result**: TRUE or FALSE, indicating whether the hvac system type matches the hvac_system_type
 
**Function Call:**

- NONE

## Logic:
- set result to false: `result = FALSE`
- check if the user is requiring an exact match: `if exact_match:`
  - simply compare the uppercase version of the two strings (we want "SYS-5" and "Sys-5" to match): `if system_type.upper() == target_system_type.upper():`
    - set the result to true: `result = TRUE`
- if the match is not exact: `else:`
  - we need to manipulate the system_type string to get the format "SYS-#", first by splitting based on a ".": `short_system_type = system_type.split(".")[0]`
  - now, eliminate the last character, if it is a letter: `short_system_type = short_system_type[:-1] if short_system_type[-1].is_alpha()`
  - now compare the uppercase version of the two strings: `if short_system_type.upper() == target_system_type.upper():`
    - set the result to true: `result = TRUE`
**Returns**  `return result`

**[Back](../_toc.md)**














