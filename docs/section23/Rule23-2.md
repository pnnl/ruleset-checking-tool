
# CHW&CW - Rule 23-2  

**Schema Version:** 0.0.23  
**Mandatory Rule:** True  
**Rule ID:** 23-2  
**Rule Description:** For baseline systems 5-8 and 11, the SAT is reset higher by 5F under minimum cooling load conditions.  
**Rule Assertion:** B-RMR = expected value  
**Appendix G Section:** Section 23 Air-side  
**90.1 Section Reference:** Section G3.1.3.12 Supply Air Temperature Reset (Systems 5 through 8 and 11)  
**Data Lookup:** None  
**Evaluation Context:** Building  
**Applicability Checks:**  

1. B-RMR is modeled with at least one air-side system that is Type-5, 6, 7, 8, 11.1, 11.2, 7a, 8a, 11.1a, 11.2a, 5b, 6b, 7b, 8b, 11b, 7c, 11c.

**Function Calls:**  

1. get_baseline_system_types()
2. is_baseline_system_type()

**Applicability Checks:**  

- Get B-RMR system types: `baseline_hvac_system_dict = get_baseline_system_types(B-RMR)`

  - Check if B-RMR is modeled with at least one air-side system that is Type-5, 6, 7, 8, 11.1, 11.2, 7a, 8a, 11.1a, 11.2a, 5b, 6b, 7b, 8b, 11b, 7c, 11c, continue to rule logic: `if any(sys_type in baseline_hvac_system_dict.keys() for sys_type in ["SYS-5", "SYS-6", "SYS-7", "SYS-8", "SYS-11.1", "SYS-11.2", "SYS-7A", "SYS-8A", "SYS-11.1A", "SYS-11.2A", "SYS-5B", "SYS-6B", "SYS-7B", "SYS-8B", "SYS-11B", "SYS-7C", "SYS-11C"]): CHECK_RULE_LOGIC`

  - Else, rule is not applicable to B-RMR: `else: RULE_NOT_APPLICABLE`

## Rule Logic:  

- For each building segment in B_RMR: `for building_segment_b in B_RMR...building_segments:`

  - For each HVAC system in building segment: `for hvac_b in building_segment_b.heating_ventilating_air_conditioning_systems:`

    - Get HVAC system serving terminal: `hvac_b = terminal_b.served_by_heating_ventilating_air_conditioning_system`
  
      - Check if HVAC system is type 5, 7, 7a, 5b, 7b, 7c, 6, 8, 8a, 6b, 8b: `if any(is_baseline_system_type(hvac_b, sys_type) == TRUE for sys_type in ["SYS-5", "SYS-7", "SYS-7A", "SYS-5B", "SYS-7B", "SYS-7C", "SYS-6", "SYS-8", "SYS-8A", "SYS-6B", "SYS-8B"]):`

        **Rule Assertion:**

        - Case 1: For each HVAC system that is Type-5, 6, 7, 8, 11.1, 11.2, 7a, 8a, 11.1a, 11.2a, 5b, 6b, 7b, 8b, 11b, 7c, 11c, if supply air temperature is reset higher by 5F under minimum cooling load condition: `if ( fan_system_b.temperature_control == "ZONE_RESET" ) AND ( fan_system_b.reset_differential_temperature == 5 ): PASS`

        - Case 2: Else: `else: FAIL`

**Notes:**
1. Updated the Rule ID from 23-1 to 23-2 on 11/28/2022

**[Back](../_toc.md)**
