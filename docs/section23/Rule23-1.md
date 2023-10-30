
# Airside System - Rule 23-1 

**Schema Version:** 0.0.34  
**Mandatory Rule:** True  
**Rule ID:** 23-1  
**Rule Description:** System 2 and 4 - Electric air-source heat pumps shall be modeled with electric auxiliary heat and an outdoor air thermostat. The systems shall be controlled to energize auxiliary heat only when the outdoor air temperature is less than 40°F. The air-source heat pump shall be modeled to continue to operate while auxiliary heat is energized.  
**Rule Assertion:** B-RMR = expected value  
**Appendix G Section:** Section 23 Air-side  
**90.1 Section Reference:** G3.1.3.1 Heat Pumps (Systems 2 and 4)  
**Data Lookup:** None  
**Evaluation Context:** Building  

**Applicability Checks:**  

1. B-RMR is modeled with at least one air-side system that is Type-2, or 4  

**Function Calls:**  

1. get_baseline_system_types()
2. baseline_system_type_compare()
3. get_component_by_id()

**Applicability Checks:**  
- create a list of the target system types: `APPLICABLE_SYS_TYPES = [HVAC_SYS.SYS_2,HVAC_SYS.SYS_4]`
- Get B-RMR system types: `baseline_hvac_system_dict = get_baseline_system_types(B-RMR)`

  - Check if B-RMR is modeled with at least one air-side system that is Type-2, or 4, continue to rule logic: `if any(baseline_system_type_compare(system_type, target_sys_type, false) for system_type in baseline_system_types_dict.keys() for applicable_sys_type in APPLICABLE_SYS_TYPES): APPLICABLE`

  - Else, rule is not applicable to B-RMR: `else: RULE_NOT_APPLICABLE`

**Notes:**

**[Back](../_toc.md)**
