
# Airside System - Rule 23-3  

**Schema Version:** 0.0.23  
**Mandatory Rule:** True  
**Rule ID:** 23-3  
**Rule Description:** System 5, 6, 7 and 8 minimum volume setpoint shall be 30% of zone peak airflow, minimum outdoor airflow, or rate required to comply with minium accreditation standards whichever is larger.  
**Rule Assertion:** B-RMI = expected value  
**Appendix G Section:** Section 23 Air-side  
**90.1 Section Reference:** Section G3.1.3.13 VAV Minimum Flow Set Points (Systems 5 and 7) and Section G3.1.3.14 Fan Power and Control (Systems 6 and 8)  
**Data Lookup:** None  
**Evaluation Context:**  
**Applicability Checks:**  

1. B-RMI is modeled with at least one air-side system that is Type-5, 6, 7, 8.

**Function Calls:**  

1. get_baseline_system_types()
2. is_baseline_system_type()
3. baseline_system_type_compare()

**Applicability Checks:**  
- create a list of the target system types: `APPLICABLE_SYS_TYPES = [HVAC_SYS.SYS_5,HVAC_SYS.SYS_6,HVAC_SYS.SYS_7,HVAC_SYS.SYS_8]`
- Get B-RMI system types: `baseline_hvac_system_dict = get_baseline_system_types(B-RMI)`

  - Check if B-RMI is modeled with at least one air-side system that is Type-5, 6, 7, 8, continue to rule logic: `if any(baseline_system_type_compare(system_type, applicable_sys_type, false) for system_type in baseline_system_types_dict.keys() for applicable_sys_type in APPLICABLE_SYS_TYPES): CHECK RULE LOGIC`

  - Else, rule is not applicable to B-RMI: `else: RULE_NOT_APPLICABLE`

## Rule Logic:  

- For each zone in B_RMI: `for terminal_b in B_RMI...terminals:`

    **Rule Assertion:**

    - Case 1: For each terminal that is served by HVAC system that is Type-5, 6, 7, 8, if minimum volume setpoint is equal to 30% of peak primary design airflow or the rate required for minimum outside air, whichever is larger: `if terminal_b.minimum_airflow == MAX(terminal_b.primary_airflow * 0.3, terminal_b.minimum_outdoor_airflow): PASS`

    - Case 2: Else, minimum volume setpoint is not equal to 30% of peak primary design airflow or the rate required for minimum outside air, whichever is larger: `else: FAIL`

**Notes:**
1. Updated the Rule ID from 23-2 to 23-3 on 11/28/2022


**[Back](../_toc.md)**
