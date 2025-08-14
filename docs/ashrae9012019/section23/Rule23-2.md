
# CHW&CW - Rule 23-2  

**Schema Version:** 0.0.23  
**Mandatory Rule:** True  
**Rule ID:** 23-2  
**Rule Description:** For baseline systems 5-8, the SAT is reset higher by 5F under minimum cooling load conditions.
**Rule Assertion:** B-RMD = expected value  
**Appendix G Section:** Section 23 Air-side  
**90.1 Section Reference:** Section G3.1.3.12 Supply Air Temperature Reset (Systems 5 through 8)  
**Data Lookup:** None  
**Evaluation Context:** Building  
**Applicability Checks:**  

1. B-RMD is modeled with at least one air-side system that is Type-5, 6, 7, 8, 7a, 8a, 5b, 6b, 7b, 8b, 7c.

**Function Calls:**  

1. get_baseline_system_types()
2. baseline_system_type_compare()

**Applicability Checks:**  
- create a list of the target system types: `target_system_types = [HVAC_SYS.SYS_5,HVAC_SYS.SYS_6,HVAC_SYS.SYS_7,HVAC_SYS.SYS_8]`
- Get B-RMD system types: `baseline_hvac_system_dict = get_baseline_system_types(B-RMD)`

  - Check if B-RMD is modeled with at least one air-side system that is Type-5, 6, 7, 8, 7a, 8a, 5b, 6b, 7b, 8b, 7c, continue to rule logic: `if any(baseline_system_type_compare(system_type, target_sys_type, false) for system_type in baseline_hvac_system_dict.keys() for target_system_type in target_system_types): CHECK RULE LOGIC`

  - Else, rule is not applicable to B-RMD: `else: RULE_NOT_APPLICABLE`

## Rule Logic:  
- For each hvac system type in the building: `for baseline_system_type in baseline_hvac_system_dict:`

  - for each hvac system in the building: `for hvac_b_id in baseline_hvac_system_dict[baseline_system_type]:`

    - check if it is one of the eligible system types: `if any(baseline_system_type_compare(baseline_system_type, target_system_type, false) for target_system_type in target_system_types):`

    - get the hvac system: `hvac_b = get_component_by_id(B_RMI, hvac_id)`
    
      - For each fan system in HVAC system: `for fan_system_b in hvac_b.fan_systems:`
        **Rule Assertion:**

        - Case 1: For each HVAC system that is Type-5, 6, 7, 8, 7a, 8a, 5b, 6b, 7b, 8b, 7c, if supply air temperature is reset higher by 5F under minimum cooling load condition: `if ( fan_system_b.temperature_control == "ZONE_RESET" ) AND ( fan_system_b.reset_differential_temperature == 5 ): PASS`
        - Case 2: Else: `else: FAIL`

**Notes:**
1. Updated the Rule ID from 23-1 to 23-2 on 11/28/2022
2. moved the logic for System Type 11 to 23-11 based on conflict between G3.1.3.12 and G3.1.3.17

**[Back](../_toc.md)**
