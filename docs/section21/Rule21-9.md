
# Boiler - Rule 21-9  

**Rule ID:** 21-9  
**Rule Description:** When baseline building includes boilers, Hot Water Pump Power = 19W/gpm.  
**Rule Assertion:** B-RMR = expected value  
**Appendix G Section:** Section 21 Boiler  
**Appendix G Section Reference:** Section G3.1.3.5 Building System-Specific Modeling Requirements for the Baseline model  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  

1. B-RMR is not modeled with purchased heating.
2. Pass Rule 21-11
3. Pass Rule 21-18

**Manual Check:** None  
**Evaluation Context:** Building  
**Data Lookup:** None  
**Function Call:** None  

**Applicability Checks:**  

1. B-RMR is not modeled with purchased heating: `if Rule-21-1 == "NOT APPLICABLE":`  
2. Pass Rule 21-11: `if Rule-21-11 == "PASS"`  
3. Pass Rule 21-18: `if Rule-21-18 == "PASS"`  

## Rule Logic:  

- For each fluid loop in B_RMR: `for fluid_loop_b in B_RMR.ASHRAE229.fluid_loops:`

  - Check if fluid loop is heating type: `if fluid_loop_b.type == "HEATING":`

    **Rule Assertion - Component:**

    - Case 1: For heating hot water loop that is served by boiler, if total pump power per flow rate is equal to 19W/gpm: `if fluid_loop_b.pump_power_per_flow_rate == 19: PASS`

    - Case 2: Else, save component ID to output array for failed components:: `else: FAIL and failed_components_array.append(fluid_loop_b)`

**Rule Assertion - RMR:**

- Case 1: If all components pass: `if ALL_COMPONENTS == PASS: PASS`

- Case 2: Else, list all failed components' ID: `else: FAIL and raise_message ${failed_components_array}`

**[Back](../_toc.md)**
