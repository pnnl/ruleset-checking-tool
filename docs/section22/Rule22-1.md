
# CHW&CW - Rule 22-1  

**Rule ID:** 22-1  
**Rule Description:** When baseline building requires CHW loop, design CHW Loop supply temperature is 44F.  
**Rule Assertion:** B-RMR = expected value  
**Appendix G Section:** Section 22 CHW&CW Loop  
**Appendix G Section Reference:** Section G3.1.3.8 Chilled-water design supply temperature (System 7, 8, 11, 12 and 13)  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  

1. B-RMR is modeled with at least one air-side system that is Type-7, 8, 11, 12, or 13
2. Pass Rule 22-42, Baseline must only have no more than one CHW plant.

**Manual Check:** None  
**Evaluation Context:** Building  
**Data Lookup:** None  
**Function Call:** None  

**Applicability Checks:**  

1. B-RMR is modeled with at least one air-side system that is Type-7, 8, 11, 12, or 13: `PLACEHOLDER`
2. Pass Rule 22-42, Baseline must only have no more than one CHW plant: `if Rule-22-42 == "PASS":`

## Rule Logic:  

- For each fluid loop in B_RMR: `for fluid_loop_b in B_RMR.ASHRAE229.fluid_loops:`

  - Check if loop is cooling type: `if fluid_loop_b.type == "COOLING":`

    **Rule Assertion:**

    - Case 1: For baseline chilled water loop, if design supply temperature is 44F: `if fluid_loop_b.cooling_or_condensing_design_and_control.design_supply_temperature == 44: PASS`

    - Case 2: Else: `else: FAIL`

**[Back](../_toc.md)**
