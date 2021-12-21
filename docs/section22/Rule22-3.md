
# CHW&CW - Rule 22-3  

**Rule ID:** 22-3  
**Rule Description:** For Baseline chilled water loop that is not purchased cooling, chilled-water supply temperature shall be reset based on outdoor dry-bulb temperature if loop does not serve any Baseline System Type-11.  
**Rule Assertion:** B-RMR = expected value  
**Appendix G Section:** Section 22 CHW&CW Loop  
**Appendix G Section Reference:** Section G3.1.3.9 Chilled-water supply temperature reset (System 7, 8, 11, 12 and 13)  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  

1. B-RMR is not modeled with any air-side system that is type-11.
2. B-RMR is not modeled with purchased chilled water.

**Manual Check:** None  
**Evaluation Context:** Building  
**Data Lookup:** None  
**Function Call:** None  

**Applicability Checks:**  

1. B-RMR is not modeled with any air-side system that is Type-11: `PLACEHOLDER`
2. B-RMR is not modeled with purchased chilled water: `if Rule-18-8 == "NOT APPLICABLE":`

## Rule Logic:  

- For each chiller in B_RMR, save chiller to loop-chiller dictionary: `for chiller_b in B_RMR.ASHRAE229.chillers: loop_chiller_dict[chiller_b.cooling_loop].append(chiller_b)`

- For each fluid loop in B_RMR: `for fluid_loop_b in B_RMR.ASHRAE229.fluid_loops:`

  - Check if fluid loop is connected to chiller(s): `if fluid_loop_b in loop_chiller_dict.keys()`

    **Rule Assertion - Component:**

    - Case 1: For Baseline chilled water loop that is not purchased cooling and does not serve any Baseline System Type-11, if supply temperature is reset based on outdoor dry-bulb temperature: `if fluid_loop_b.cooling_or_condensing_design_and_control.temperature_reset_type == "OUTSIDE_AIR_RESET": PASS`

    - Case 2: Else, save component ID to output array for failed components:: `else: FAIL and failed_components_array.append(fluid_loop_b)`

**Rule Assertion - RMR:**

- Case 1: If all components pass: `if ALL_COMPONENTS == PASS: PASS`

- Case 2: Else, list all failed components' ID: `else: FAIL and raise_message ${failed_components_array}`

**[Back](../_toc.md)**
