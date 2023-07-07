
# Airside System - Rule 23-3  

**Schema Version:** 0.0.23  
**Mandatory Rule:** True  
**Rule ID:** 23-3  
**Rule Description:** System 5, 6, 7 and 8 minimum volume setpoint shall be 30% of zone peak airflow, minimum outdoor airflow, or rate required to comply with minium accreditation standards whichever is larger.  
**Rule Assertion:** B-RMD = expected value  
**Appendix G Section:** Section 23 Air-side  
**90.1 Section Reference:** Section G3.1.3.13 VAV Minimum Flow Set Points (Systems 5 and 7) and Section G3.1.3.14 Fan Power and Control (Systems 6 and 8)  
**Data Lookup:** None  
**Evaluation Context:**  
**Applicability Checks:**  

1. B-RMD is modeled with at least one air-side system that is Type-5, 7, 7a, 5b, 7b, 7c, 6, 8, 8a, 6b, 8b.

**Function Calls:**  

1. get_baseline_system_types()
2. is_baseline_system_type()
3. baseline_system_type_compare()

**Applicability Checks:**  
- create a list of the target system types: `target_system_types = [HVAC_SYS.SYS_5,HVAC_SYS.SYS_6,HVAC_SYS.SYS_7,HVAC_SYS.SYS_8]`
- Get B-RMD system types: `baseline_hvac_system_dict = get_baseline_system_types(B-RMD)`

  - Check if B-RMD is modeled with at least one air-side system that is Type-5, 7, 7a, 5b, 7b, 7c, continue to rule logic: `if any(baseline_system_type_compare(system_type, target_sys_type, false) for system_type in baseline_hvac_system_dict.keys() for target_system_type in target_system_types): CHECK RULE LOGIC`

  - Else, rule is not applicable to B-RMD: `else: RULE_NOT_APPLICABLE`

## Rule Logic:  

- create a list of eligible hvac systems: `eligible_hvac_system_ids = []`

- For each hvac system type in the baseline_hvac_system_dict: `for baseline_system_type in baseline_hvac_system_dict:`
  - check if it is one of the applicable systems (5, 6, 7, 8): `if any(baseline_system_type_compare(baseline_system_type, target_system_type, false) for target_system_type in target_system_types):`
    - add the ids to the list of eligible systems: `eligible_hvac_system_ids = eligible_hvac_system_ids + baseline_hvac_system_dict[baseline_system_type]`

- For each zone in B_RMR: `for zone_b in B_RMR...zones:`

  - For each terminal in zone: `for terminal_b in zone_b.terminals:`

    - Get HVAC system serving terminal: `hvac_b = terminal_b.served_by_heating_ventilating_air_conditioning_systems`
  
      - Check if HVAC system is one of the eligible systems: `if hvac_b.id in eligible_hvac_system_ids:`

        **Rule Assertion:**    

        - Case 1: For each terminal that is served by HVAC system that is Type-5, 7, 7a, 5b, 7b, 7c, 6, 8, 8a, 6b, 8b, if minimum volume setpoint is equal to 30% of peak primary design airflow or the rate required for minimum outside air, whichever is larger: `if terminal_b.minimum_airflow == MAX(terminal_b.primary_airflow * 0.3, terminal_b.minimum_outdoor_airflow): PASS`

        - Case 2: Else, minimum volume setpoint is not equal to 30% of peak primary design airflow or the rate required for minimum outside air, whichever is larger: `else: FAIL`

**Notes:**
1. Updated the Rule ID from 23-2 to 23-3 on 11/28/2022


**[Back](../_toc.md)**
