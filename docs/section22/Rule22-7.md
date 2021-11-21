
# CHW&CW - Rule 22-7  

**Rule ID:** 22-7  
**Rule Description:** Baseline chilled water system that does not use purchased chilled water shall be modeled as primary/secondary systems.  
**Rule Assertion:** B-RMR = expected value  
**Appendix G Section:** Section 22 CHW&CW Loop  
**Appendix G Section Reference:** Section G3.1.3.10 Chilled-water supply temperature reset (System 7, 8, 11, 12 and 13)  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  

1. B-RMR is modeled with at least one air-side system that is Type-7, 8, 11, 12, or 13.
2. B-RMR is modeled with at least one chilled water system that does not use purchased chilled water.

**Manual Check:** None  
**Evaluation Context:** Building  
**Data Lookup:** None  
**Function Call:** None  

**Applicability Checks:**  

1. B-RMR is modeled with at least one air-side system that is Type-7, 8, 11, 12, or 13: `PLACEHOLDER`
2. B-RMR is modeled with at least one chilled water system that does not use purchased chilled water: `if B_RMR.ASHRAE229.chillers:`

## Rule Logic:  

- For each pump in B_RMR: `for pump_b in B_RMR.ASHRAE229.pumps:`

  - For loop served by pump, save to an array: `loop_with_pump_array.append(pump_b.loop_or_piping)`

- For each chiller in B_RMR: `for chiller_b in B_RMR.ASHRAE229.chillers:`

  - Get cooling loop that chiller servers: `chw_loop_b = chiller_b.cooling_loop`

    - If cooling loop has not been saved in CHW loop array: `if chw_loop_b NOT in chw_loop_check_array:`

      - Save cooling loop to CHW loop array that needs to comply with the requirement: `chw_loop_check_array.append(chw_loop_b)`

- For each CHW loop that chiller serves: `for loop_b in chw_loop_check_array:`

  **Rule Assertion:**

  - Case 1: If CHW loop is modeled with secondary loop with pump: `if ( loop_b.child_loops ) AND ( loop in loop_with_pump_array for loop in loop_b.child_loops ): PASS`

  - Case 2: Else: `else: FAIL`

**[Back](../_toc.md)**
