
# Boiler - Rule 21-11C  

**Rule ID:** 21-11C  
**Rule Description:** When the system uses boilers the hot water system shall be modeled with a minimum turndown ratio of 0.25.  
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

    - Case 1: For heating hot water loop that is served by boiler(s), if loop is modeled with a minimum turndown ratio of 25%: `if fluid_loop_b.heating_design_and_control.minimum_flow_fraction == 0.25: PASS`

    - Case 2: Else: `else: FAIL`

**[Back](../_toc.md)**
