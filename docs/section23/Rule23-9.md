
# Airside System - Rule 23-9 

**Schema Version:** 0.0.34  
**Mandatory Rule:** True  
**Rule ID:** 23-9  
**Rule Description:** System 11 Minimum volume setpoint shall be the largest of 50% of the maximum design airflow rate, the minimum ventilation airflow rate or the airflow required to comply with codes or accredidation standards.    
**Rule Assertion:** B-RMR = expected value  
**Appendix G Section:** Section 23 Air-side  
**90.1 Section Reference:** System 11 Minimum volume setpoint shall be the largest of 50% of the maximum design airflow rate, the minimum ventilation airflow rate or the airflow required to comply with codes or accredidation standards.  
**Data Lookup:** None  
**Evaluation Context:** Building  

**Applicability Checks:**  

1. B-RMR is modeled with at least one air-side system that is Type-11.  

**Function Calls:**  

1. get_baseline_system_types()
2. baseline_system_type_compare()

**Applicability Checks:**  
- create a list of the target system types: `APPLICABLE_SYS_TYPES = [HVAC_SYS.SYS_11]`
- Get B-RMR system types: `baseline_hvac_system_dict = get_baseline_system_types(B-RMR)`

  - Check if B-RMR is modeled with at least one air-side system that is Type-11, continue to rule logic: `if any(baseline_system_type_compare(system_type, target_sys_type, false) for system_type in baseline_system_types_dict.keys() for applicable_sys_type in APPLICABLE_SYS_TYPES): UNDETERMINED`

  - Else, rule is not applicable to B-RMR: `else: RULE_NOT_APPLICABLE`

**Notes:**

**[Back](../_toc.md)**
