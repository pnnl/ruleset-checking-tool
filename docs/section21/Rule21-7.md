
# Boiler - Rule 21-7  

**Rule ID:** 21-7  
**Rule Description:** When baseline building requires boilers, systems 1,5,7,11 and 12 - Model HWST = 180F and return design temp = 130F.  
**Rule Assertion:** B-RMR = expected value  
**Appendix G Section:** Section 21 Boiler  
**Appendix G Section Reference:** Section G3.1.3.3 Building System-Specific Modeling Requirements for the Baseline model  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  

1. B-RMR is modeled with at least one air-side system that is Type-1, 5, 7, 11, or 12
2. B-RMR is not modeled with purchased heating.
3. Pass Rule 21-11
4. Pass Rule 21-18

**Manual Check:** None  
**Evaluation Context:** Building  
**Data Lookup:** None  
**Function Call:** None  

**Applicability Checks:**  

1. B-RMR is modeled with at least one air-side system that is Type-1, 5, 7, 11, or 12: `PLACEHOLDER`  
2. B-RMR is not modeled with purchased heating: `if Rule-21-1 == "NOT APPLICABLE":`  
3. Pass Rule 21-11: `if Rule-21-11 == "PASS"`  
4. Pass Rule 21-18: `if Rule-21-18 == "PASS"`  

## Rule Logic:  

- For each fluid loop in B_RMR: `for fluid_loop_b in B_RMR.ASHRAE229.fluid_loops:`

  - Check if fluid loop is heating type: `if fluid_loop_b.type == "HEATING":`

    **Rule Assertion:**

    - Case 1: For each fluid loop that boiler serves, if design supply temperature is 180F and design return temperature is 130F: `if ( fluid_loop_b.heating_design_and_control.design_supply_temperature == 180 ) AND ( fluid_loop_b.heating_design_and_control.design_return_temperature == 130 ): PASS`

    - Case 2: Else: `else: FAIL`

**[Back](../_toc.md)**
