
# CHW&CW - Rule 22-1  

**Rule ID:** 22-1  
**Rule Description:** When baseline building requires CHW loop, design CHW Loop supply temperature is 44F.  
**Rule Assertion:** B-RMR = expected value  
**Appendix G Section:** Section 22 CHW&CW Loop  
**Appendix G Section Reference:** Section G3.1.3.8 Chilled-water design supply temperature (System 7, 8, 11, 12 and 13)  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  

1. B-RMR is modeled with at least one air-side system that is Type-7, 8, 11, 12, or 13

**Manual Check:** None  
**Evaluation Context:** Building  
**Data Lookup:** None  
**Function Call:** None  

**Applicability Checks:**  

1. B-RMR is modeled with at least one air-side system that is Type-7, 8, 11, 12, or 13: `PLACEHOLDER`

## Rule Logic:  

- For each fluid loop in B_RMR: `for fluid_loop_b in B_RMR.ASHRAE229.fluid_loops:`

  - Check if loop is cooling type: `if fluid_loop_b.type == "COOLING":`

    - Get child loops under cooling loop: `child_loops_b = fluid_loop_b.child_loops`

      **Rule Assertion:**

      - Case 1: For each fluid loop that chiller serves and its child loops, if design supply temperature is 44F: `if ( fluid_loop_b.cooling_or_condensing_design_and_control.design_supply_temperature == 44 ) AND ( child_loop.cooling_or_condensing_design_and_control.design_supply_temperature == 44 for child_loop in child_loops_b ): PASS`

      - Case 2: Else: `else: FAIL`

**[Back](../_toc.md)**

**Notes:**

1. This is applicable to both CHW loop served by chiller and purchased chilled water. Using Section 22 for now. Purchased chilled water is Section 18. Or do we need to have a separate rule under Section 18 to check the temperature?
