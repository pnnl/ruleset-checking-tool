
# CHW&CW - Rule 22-3  

**Rule ID:** 22-3  
**Rule Description:** For Baseline chilled water loop that is not purchased cooling, chilled-water supply temperature shall be reset based on outdoor dry-bulb temperature if loop does not serve any Baseline System Type-11.  
**Rule Assertion:** B-RMR = expected value  
**Appendix G Section:** Section 22 CHW&CW Loop  
**Appendix G Section Reference:** Section G3.1.3.9 Chilled-water supply temperature reset (System 7, 8, 11, 12 and 13)  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  

1. B-RMR is modeled with at least one air-side system that is Type-7, 8, 12, or 13
2. B-RMR is not modeled with any air-side system that is type-11.
3. B-RMR is not modeled with purchased chilled water.
4. Pass Rule 22-34, Baseline must only have no more than one CHW plant.
5. Pass Rule 22-7, Baseline chilled water system that does not use purchased chilled water shall be modeled as primary/secondary systems.


**Manual Check:** None  
**Evaluation Context:** Building  
**Data Lookup:** None  
**Function Call:** None  

**Applicability Checks:**  

1. B-RMR is modeled with at least one air-side system that is Type-7, 8, 12, or 13: `PLACEHOLDER:`
2. B-RMR is not modeled with any air-side system that is Type-11: `PLACEHOLDER`
3. B-RMR is not modeled with purchased chilled water: `if Rule-18-8 == "NOT APPLICABLE":`
4. Pass Rule 22-34, Baseline must only have no more than one CHW plant: `if Rule-22-34 == "PASS":`
5. Pass Rule 22-7, Baseline chilled water system that does not use purchased chilled water shall be modeled as primary/secondary systems: `if Rule-22-7 == "PASS":`

## Rule Logic:  

- Get primary CHW loop in B_RMR `primary_chw_loop_b = B_RMR.ASHRAE229.chillers[0].cooling_loop`

  **Rule Assertion:**

  - Case 1: For Baseline chilled water loop that is not purchased cooling and does not serve any Baseline System Type-11, if supply temperature is reset based on outdoor dry-bulb temperature: `if fluid_loop_b.cooling_or_condensing_design_and_control.temperature_reset_type == "OUTSIDE_AIR_RESET": PASS`

  - Case 2: Else: `else: FAIL`

**[Back](../_toc.md)**
