
# Boiler - Rule 21-11A  

**Rule ID:** 21-11A  
**Rule Description:** When the system uses boilers the hot water system shall be modeled as primary only.  
**Rule Assertion:** B-RMR  
**Appendix G Section:** Section 21 Boiler  
**Appendix G Section Reference:** Section G3.1.3.5 Building System-Specific Modeling Requirements for the Baseline model  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  

1. B-RMR is modeled with at least one air-side system that is Type-1, 5, 7, 11, or 12
2. B-RMR is not modeled with purchased heating.
3. Pass Rule 21-18.
4. Pass Rule 21-4.

**Manual Check:** None  
**Evaluation Context:** Building  
**Data Lookup:** None  
**Function Call:** None  

**Applicability Checks:**  

1. B-RMR is modeled with at least one air-side system that is Type-1, 5, 7, 11, or 12: `PLACEHOLDER:`
2. B-RMR is not modeled with purchased heating: `if Rule-21-1 == "NOT APPLICABLE":`
3. Pass Rule 21-18: `if Rule-21-18 == "PASS":`
4. Pass Rule 21-4: `if Rule-21-4 == "PASS":`

## Rule Logic:  

- For each fluid loop in B_RMR: `for fluid_loop_b in B_RMR.ASHRAE229.fluid_loops:`

  - Check if fluid loop is heating type: `if fluid_loop_b.type == "HEATING":`

    **Rule Assertion:**

    - Case 1: For heating hot water loop that is served by boiler(s), if loop is modeled as primary only: `if fluid_loop_b.child_loop == NULL: PASS`

    - Case 2: Else: `else: FAIL`

**[Back](../_toc.md)**

**Notes:**

1. Do we want to set Rule 21-4 "When baseline building does not use purchased heat, baseline systems 1,5,7,11, 12 shall be modeled with natural draft boilers" as mandatory so that if proposed does not have purchased heating, baseline needs to have boiler(s) on the HHW loop? And this rule can use Rule 21-4 as applicability check and just check if HHW loop does not have any child loop then it is correctly modeled as a primary loop.
