
# CHW&CW - Rule 22-3  

**Rule ID:** 22-3  
**Rule Description:** For Baseline chilled water loop that is not purchased cooling, chilled-water supply temperature shall be reset based on outdoor dry-bulb temperature.  
**Rule Assertion:** B-RMR = expected value  
**Appendix G Section:** Section 22 CHW&CW Loop  
**Appendix G Section Reference:** Section G3.1.3.9 Chilled-water supply temperature reset (System 7, 8, 11, 12 and 13)  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  

1. B-RMR is modeled with at least one air-side system that is Type-7, 8, 11, 12, or 13
2. B-RMR is not modeled with purchased chilled water.

**Manual Check:** None  
**Evaluation Context:** Building  
**Data Lookup:** None  
**Function Call:** None  

**Applicability Checks:**  

1. B-RMR is modeled with at least one air-side system that is Type-7, 8, 11, 12, or 13: `PLACEHOLDER:`
2. B-RMR is modeled with at least one chilled water system that does not use purchased chilled water: `if B_RMR.ASHRAE229.chillers:`

## Rule Logic:  

- For each chiller in B_RMR: `for chiller_b in B_RMR.ASHRAE229.chillers:`

  - Get cooling loop that chiller servers: `chw_loop_b = chiller_b.cooling_loop`

    - If cooling loop has not been saved in CHW loop array: `if chw_loop_b NOT in chw_loop_array:`

      - Save cooling loop to CHW loop array: `chw_loop_array.append(chw_loop_b)`

**Rule Assertion:**

- Case 1: For each fluid loop that chiller serves, if supply temperature is reset based on outdoor dry-bulb temperature: `if ( loop.cooling_or_condensing_design_and_control.temperature_reset_type == "OUTSIDE_AIR_RESET" for loop in chw_loop_array): PASS`

- Case 2: Else: `else: FAIL`

**[Back](../_toc.md)**

**Notes:**

1. Need to check secondary loop?
