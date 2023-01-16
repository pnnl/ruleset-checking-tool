
# CHW&CW - Rule 23-2  

**Schema Version:** 0.0.23  
**Mandatory Rule:** True  
**Rule ID:** 23-2  
**Rule Description:** For baseline systems 5-8 and 11, the SAT is reset higher by 5F under minimum cooling load conditions.  
**Rule Assertion:** B-RMI = expected value  
**Appendix G Section:** Section 23 Air-side  
**90.1 Section Reference:** Section G3.1.3.12 Supply Air Temperature Reset (Systems 5 through 8 and 11)  
**Data Lookup:** None  
**Evaluation Context:** Building  
**Applicability Checks:**  

1. B-RMI is modeled with at least one air-side system that is Type-5, 6, 7, 8, 11.1.

**Function Calls:**  

1. get_baseline_system_types()
2. baseline_system_type_compare()

**Applicability Checks:**  
- create a list of the target system types: `APPLICABLE_SYS_TYPES = [HVAC_SYS.SYS_5,HVAC_SYS.SYS_6,HVAC_SYS.SYS_7,HVAC_SYS.SYS_8,HVAC_SYS.SYS_11.1]`
- Get B-RMI system types: `baseline_hvac_system_dict = get_baseline_system_types(B-RMI)`

  - Check if B-RMI is modeled with at least one air-side system that is Type-5, 6, 7, 8, 11.1, continue to rule logic: `if any(baseline_system_type_compare(system_type, applicable_sys_type, false) for system_type in baseline_system_types_dict.keys() for applicable_sys_type in APPLICABLE_SYS_TYPES): CHECK RULE LOGIC`

  - Else, rule is not applicable to B-RMI: `else: RULE_NOT_APPLICABLE`

## Rule Logic:  

- For each fan system in HVAC system: `for fan_system_b in B_RMI.ASHRAE229.fan_systems:`       

  **Rule Assertion:**    

  - Case 1: For each HVAC system that is Type-5, 6, 7, 8, 11.1, if supply air temperature is reset higher by 5F under minimum cooling load condition: `if ( fan_system_b.temperature_control == "ZONE_RESET" ) AND ( fan_system_b.reset_differential_temperature == 5 ): PASS`

  - Case 2: Else: `else: FAIL`

**Notes:**
1. Updated the Rule ID from 23-1 to 23-2 on 11/28/2022

**[Back](../_toc.md)**
