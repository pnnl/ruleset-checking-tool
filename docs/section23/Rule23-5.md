
# Airside System - Rule 23-5 

**Schema Version:** 0.0.34  
**Mandatory Rule:** True  
**Rule ID:** 23-5  
**Rule Description:** For baseline systems 6 and 8, Fans in parallel VAV fan-powered boxes shall run as the first stage of heating before the reheat coil is energized.  
**Rule Assertion:** B-RMR = expected value  
**Appendix G Section:** Section 23 Air-side  
**90.1 Section Reference:** G3.1.3.14 Fan Power and Control (Systems 6 and 8)  
**Data Lookup:** None  
**Evaluation Context:** Building  

**Applicability Checks:**  

1. B-RMR is modeled with at least one air-side system that is Type-6 or 8.  

**Function Calls:**  

1. get_baseline_system_types()
2. baseline_system_type_compare()

**Applicability Checks:**  
- create a list of the target system types: `APPLICABLE_SYS_TYPES = [HVAC_SYS.SYS_6, HVAC_SYS.SYS_8]`
- Get B-RMR system types: `baseline_hvac_system_dict = get_baseline_system_types(B-RMR)`

  - Check if B-RMR is modeled with at least one air-side system that is Type-6, or 8, continue to rule logic: `if any(baseline_system_type_compare(system_type, target_sys_type, false) for system_type in baseline_system_types_dict.keys() for applicable_sys_type in APPLICABLE_SYS_TYPES): APPLICABLE`

  - Else, rule is not applicable to B-RMR: `else: RULE_NOT_APPLICABLE`

**Notes:**

**[Back](../_toc.md)**
