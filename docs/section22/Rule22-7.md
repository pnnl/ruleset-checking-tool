
# CHW&CW - Rule 22-7  

**Schema Version:** 0.0.10   
**Mandatory Rule:** True   
**Rule ID:** 22-7  
**Rule Description:** Baseline chilled water system that does not use purchased chilled water shall be modeled as primary/secondary systems.  
**Rule Assertion:** B-RMR = expected value  
**Appendix G Section:** Section 22 CHW&CW Loop  
**90.1 Section Reference:** Section G3.1.3.10 Chilled-Water Pumps (Systems 7, 8, 11, 12, and 13)  
**Data Lookup:** None  
**Evaluation Context:** Building  
**Applicability Checks:**  

1. B-RMR is modeled with at least one air-side system that is Type-7, 8, 11.1, 11.2, 12, 13, 7b, 8b, 11b, 12b.

**Function Calls:**  

1. get_baseline_system_types()
2. get_primary_secondary_loops_dict()

**Applicability Checks:**  

- Get B-RMR system types: `baseline_hvac_system_dict = get_baseline_system_types(B-RMR)`

  - Check if B-RMR is modeled with at least one air-side system that is Type-7, 8, 11.1, 11.2, 12, 13, 7b, 8b, 11b, 12b, 13b, i.e. with air-side system served by chiller(s), continue to rule logic: `if any(sys_type in baseline_hvac_system_dict.keys() for sys_type in ["SYS-7", "SYS-8", "SYS-11.1", "SYS-11.2", "SYS-12", "SYS-13", "SYS-7B", "SYS-8B", "SYS-11B", "SYS-12B"]): CHECK_RULE_LOGIC`

  - Else, rule is not applicable to B-RMR: `else: RULE_NOT_APPLICABLE`

## Rule Logic:  

- Get primary and secondary loops for B-RMR: `primary_secondary_loop_dictionary = get_primary_secondary_loops_dict(B_RMR)`

**Rule Assertion - Component:**

- Case 1: If B-RMR is modeled with primary-secondary configuration: `if LEN(primary_secondary_loop_dictionary) != 0: PASS`

- Case 2: Else: `else: FAIL`

**[Back](../_toc.md)**
