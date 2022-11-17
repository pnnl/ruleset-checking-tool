
# CHW&CW - Rule 22-3  

**Rule ID:** 22-3  
**Rule Description:** For Baseline chilled water loop that is not purchased cooling, chilled-water supply temperature shall be reset based on outdoor dry-bulb temperature if loop does not serve any Baseline System Type-11.  
**Rule Assertion:** B-RMR = expected value  
**Appendix G Section:** Section 22 CHW&CW Loop  
**Appendix G Section Reference:** Section G3.1.3.9 Chilled-water supply temperature reset (System 7, 8, 11, 12 and 13)  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  

1. B-RMR is modeled with at least one air-side system that is Type-7, 8, 12, 13, 7b, 8b, 12b.
2. B-RMR is not modeled with any air-side system that is Type-11.1, 11.2, 11.1a, 11.2a, 11b or 11c.

**Manual Check:** None  
**Evaluation Context:** Building  
**Data Lookup:** None  
**Function Call:**  

1. get_baseline_system_types()

**Applicability Checks:**  

- Get B-RMR system types: `baseline_hvac_system_dict = get_baseline_system_types(B-RMR)`

  - Check if B-RMR is modeled with at least one air-side system that is Type-7, 8, 12, 13, 7b, 8b, 12b, 13b, i.e. with air-side system served by chiller(s): `if any(sys_type in baseline_hvac_system_dict.keys() for sys_type in ["SYS-7", "SYS-8", "SYS-12", "SYS-13", "SYS-7B", "SYS-8B", "SYS-12B"]):`

    - Check if B-RMR is modeled with any air-side system that is Type-11.1, 11.2, 11.1a, 11.2a, 11b or 11c, rule is not applicable to B-RMR: `if any(sys_type in baseline_hvac_system_dict.keys() for sys_type in ["SYS-11.1", "SYS-11.2", "SYS-11.1A", "SYS-11.2A", "SYS-11B", "SYS-11C"]): RULE_NOT_APPLICABLE`

    - Else, continue to rule logic: `else: CHECK_RULE_LOGIC`

  - Else, rule is not applicable to B-RMR: `else: RULE_NOT_APPLICABLE`

## Rule Logic:  

- For each chiller in B_RMR, save chiller to loop-chiller-ids-list: `for chiller_b in B_RMR.ASHRAE229.chillers: loop_chiller_ids_list.append(chiller_b)`

- For each fluid loop in B_RMR: `for fluid_loop_b in B_RMR.ASHRAE229.fluid_loops:`

  - Check if fluid loop is connected to chiller(s): `if fluid_loop_b.id in loop_chiller_dict.keys()`

    **Rule Assertion - Component:**

    - Case 1: For Baseline chilled water loop that is not purchased cooling and does not serve any Baseline System Type-11, if supply temperature is reset based on outdoor dry-bulb temperature: `if fluid_loop_b.cooling_or_condensing_design_and_control.temperature_reset_type == "OUTSIDE_AIR_RESET": PASS`

    - Case 2: Else: `else: FAIL`

**[Back](../_toc.md)**
