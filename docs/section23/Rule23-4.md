
# Airside System - Rule 23-4 

**Schema Version:** 0.0.34  
**Mandatory Rule:** True  
**Rule ID:** 23-4  
**Rule Description:** Baseline systems 5 & 7 serving lab spaces per G3.1.1c shall reduce lab exhaust and makeup air during unoccupied periods to 50% of zone peak airflow, the minimum outdoor airflow, or rate required to comply with minimum accreditation standards whichever is larger.
**Rule Assertion:** B-RMR = expected value  
**Appendix G Section:** Section 23 Air-side  
**90.1 Section Reference:** G3.1.3.13 VAV Minimum Flow Set Points (Systems 5 and 7)  
**Data Lookup:** None  
**Evaluation Context:** Building  

**Applicability Checks:**  

1. B-RMR is modeled with at least one air-side system that is Type-5 or 7.  

**Function Calls:**  

1. get_baseline_system_types()
2. baseline_system_type_compare()

**Applicability Checks:**  
- create a list of the target system types: `APPLICABLE_SYS_TYPES = [HVAC_SYS.SYS_11]`
- Get B-RMR system types: `baseline_hvac_system_dict = get_baseline_system_types(B-RMR)`

  - Check if B-RMR is modeled with at least one air-side system that is Type-2, or 4, continue to rule logic: `if any(baseline_system_type_compare(system_type, target_sys_type, false) for system_type in baseline_system_types_dict.keys() for applicable_sys_type in APPLICABLE_SYS_TYPES): APPLICABLE`

  - Else, rule is not applicable to B-RMR: `else: RULE_NOT_APPLICABLE`

**Notes:**

**[Back](../_toc.md)**
