
# CHW&CW - Rule 22-1  

**Rule ID:** 22-1  
**Rule Description:** Baseline chilled water design supply temperature shall be modeled at 44F.  
**Rule Assertion:** B-RMR = expected value  
**Appendix G Section:** Section 22 CHW&CW Loop  
**Appendix G Section Reference:** Section G3.1.3.8 Chilled-water design supply temperature (System 7, 8, 11, 12 and 13)  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  

1. B-RMR is modeled with at least one air-side system that is Type-7, 8, 11.1, 11,2, 12, 13, 1a, 3a, 7a, 8a, 11.1a, 11.2a, 12a, 13a, 7b, 8b, 11b, 12b, 1c, 3c, 7c, 11c.

**Manual Check:** None  
**Evaluation Context:** Building  
**Data Lookup:** None  
**Function Call:**  

1. get_baseline_system_types()
2. find_all()

**Applicability Checks:**  

- Get B-RMR system types: `baseline_hvac_system_dict = get_baseline_system_types(B-RMR)`

  - Check if B-RMR is modeled with at least one air-side system that is Type-7, 8, 11.1a. 11.2a, 12, 13, 1a, 3a, 7a, 8a, 11.1a, 11.2a, 12a, 13a, 7b, 8b, 11b, 12b, 13b, 1c, 3c, 7c, 11c, 13c, i.e. with air-side system served by chilled water, continue to rule logic: `if any(sys_type in baseline_hvac_system_dict.keys() for sys_type in ["SYS-7", "SYS-8", "SYS-11.1", "SYS-11.2", "SYS-12", "SYS-13", "SYS-1A", "SYS-3A", "SYS-7A", "SYS-8A", "SYS-11.1A", "SYS-11.2A", "SYS-12A", "SYS-13A", "SYS-7B", "SYS-8B", "SYS-11B", "SYS-12B", "SYS-1C", "SYS-3C", "SYS-7C", "SYS-11C"]): CHECK_RULE_LOGIC`

  - Else, rule is not applicable to B-RMR: `else: RULE_NOT_APPLICABLE`

## Rule Logic:  

- For each boiler in B_RMI, save boiler to loop boiler dictionary: `loop_boiler_dict = find_all(B-RMI)`

- For each fluid loop in B_RMR: `for fluid_loop_b in B_RMR.ASHRAE229.fluid_loops:`

  - Check if fluid loop is connected to chiller(s): `if fluid_loop_b.id in loop_chiller_dict.keys()`

    **Rule Assertion - Component:**

    - Case 1: For baseline primary chilled water loop, if design supply temperature is 44F: `if fluid_loop_b.cooling_or_condensing_design_and_control.design_supply_temperature == 44: PASS`

    - Case 2: Else: `else: FAIL`

**[Back](../_toc.md)**
