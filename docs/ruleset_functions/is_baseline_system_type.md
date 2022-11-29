# is_baseline_system_type

**Schema Version:** 0.0.23

**Description:** Returns a boolean TRUE or FALSE indicating whether the given hvac_id is of the given hvac_system_type

**Inputs:**  
- **RMI**: The RMR to evalute (B-RMR or P-RMR or U-RMR). 
- **hvac_id**: The id of the hvac system to be tested
- **hvac_system_type**: the string indicating the hvac system type for example: "SYS-5" or "SYS-8c"
- **exact_match**: a boolean, TRUE or FALSE.  if exact_match is TRUE, then the system type must match exactly the string given by hvac_system_type.  If false, an approximate match will return true.  This would be used in the case where the user wants any hvac system ot type 8, without having to type in 8a, 8b, 8c.  In this case, "SYS-8" would be passed to the function and the function would return TRUE for any system 8, regardless of it's 8a, 8b, or 8c

**Returns:**  
- **result**: TRUE or FALSE, indicating whether the hvac system type matches the hvac_system_type
 
**Function Call:**

- get_baseline_system_types

## Logic:
- set result to false: `result = FALSE`
- get the baseline hvac system types: `hvac_system_types = get_baseline_system_types(RMI)
- create a list of the acceptable matching strings: `detailed_hvac_system_types = []`
- check if the user is requiring an exact match: `if exact_match:`
  - append the user's hvac_system_type string to the list: `detailed_hvac_system_types.append(hvac_system_type)`
- otherwise, we need to match the given string to the possible strings: `else:`
  - if the hvac_system_type is "SYS-1": `if hvac_system_type == "SYS-1":`
    - the sub-types are 1a, 1b, 1c: `detailed_hvac_system_types = ["SYS-1", "SYS-1a", "SYS-1b", "SYS-1c"]
  - elsif the hvac_system type is "SYS-2": `elsif hvac_system_type == "SYS-2:"`
    - the sub-types are 2: `detailed_hvac_system_types = ["SYS-2"]
  - elsif the hvac_system type is "SYS-3": `elsif hvac_system_type == "SYS-3:"`
    - the sub-types are 3a, 3b, 3c: `detailed_hvac_system_types = ["SYS-3", "SYS-3a", "SYS-3b", "SYS-3c"]
  - elsif the hvac_system type is "SYS-4": `elsif hvac_system_type == "SYS-4:"`
    - the sub-types are 4: `detailed_hvac_system_types = ["SYS-4"]
  - elsif the hvac_system type is "SYS-5": `elsif hvac_system_type == "SYS-5:"`
    - the sub-types are 5, 5b: `detailed_hvac_system_types = ["SYS-5", "SYS-5b"]
  - elsif the hvac_system type is "SYS-6": `elsif hvac_system_type == "SYS-6:"`
    - the sub-types are 6, 6b: `detailed_hvac_system_types = ["SYS-6", "SYS-6b"]
  - elsif the hvac_system type is "SYS-7": `elsif hvac_system_type == "SYS-7:"`
    - the sub-types are 7a, 7b, 7c: `detailed_hvac_system_types = ["SYS-7", "SYS-7a", "SYS-7b", "SYS-7c"]
  - elsif the hvac_system type is "SYS-8": `elsif hvac_system_type == "SYS-8:"`
    - the sub-types are 8a, 8b, 8c: `detailed_hvac_system_types = ["SYS-8", "SYS-8a", "SYS-8b", "SYS-8c"]
  - elsif the hvac_system type is "SYS-9": `elsif hvac_system_type == "SYS-9:"`
    - the sub-types are 9, 9b: `detailed_hvac_system_types = ["SYS-9", "SYS-9b"]
  - elsif the hvac_system type is "SYS-10": `elsif hvac_system_type == "SYS-10:"`
    - there are no sub-types: `detailed_hvac_system_types = ["SYS-10"]
  - elsif the hvac_system type is "SYS-11": `elsif hvac_system_type == "SYS-11:"`
    - the sub-types are 11.1, 11.1a, 11b, 11c, 11.2, 11.2a: `detailed_hvac_system_types = ["SYS-11.1", "SYS-11.1a", "SYS-11b", "SYS-11c", "SYS-11.2", "SYS-11.2a"]
  - elsif the hvac_system type is "SYS-12": `elsif hvac_system_type == "SYS-12:"`
    - the sub-types are 12, 12a, 12b, 12c: `detailed_hvac_system_types = ["SYS-12", "SYS-12a", "SYS-12b", "SYS-12c"]
  - elsif the hvac_system type is "SYS-13": `elsif hvac_system_type == "SYS-13:"`
    - the sub-types are 13, 13a, 13b, 13c: `detailed_hvac_system_types = ["SYS-13", "SYS-13a", "SYS-13b", "SYS-13c"]

- for each system type in the detailed_hvac_system_types list: `for target_system_type in detailed_hvac_system_types:`
  - check if the hvac_id is in the list of hvac_ids served by this sytem type: `if hvac_id in hvac_system_types[target_system_type]:`
    - set the result to true: `result = TRUE`
    - break out of the loop: `break`

**Returns**  `return result`

**[Back](../_toc.md)**














