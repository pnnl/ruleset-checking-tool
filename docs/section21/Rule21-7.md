
# Boiler - Rule 21-7  

**Rule ID:** 21-7  
**Rule Description:** When baseline building requires boilers, systems 1,5,7,11 and 12 - Model HWST = 180F and return design temp = 130F.  
**Rule Assertion:** B-RMR = expected value  
**Appendix G Section:** Section 21 Boiler  
**Appendix G Section Reference:** Section G3.1.3.3 Building System-Specific Modeling Requirements for the Baseline model  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  

1. B-RMR is not modeled with purchased heating.

**Manual Check:** None  
**Evaluation Context:** Building  
**Data Lookup:** None  
**Function Call:** None  

**Applicability Checks:**  

1. B-RMR is not modeled with purchased heating: `if Rule-21-1 == "NOT APPLICABLE":`  

## Rule Logic:  

- For each boiler in B_RMR, save boiler to loop boiler dictionary: `for boiler_b in B_RMR.ASHRAE229.boilers: loop_boiler_dict[boiler_b.loop].append(boiler_b)`

- For each fluid loop in B_RMR: `for fluid_loop_b in B_RMR.ASHRAE229.fluid_loops:`

  - Check if fluid loop is connected to boiler(s): `if fluid_loop_b in loop_boiler_dict.keys()`

    **Rule Assertion - Component:**

    - Case 1: For each fluid loop that boiler serves, if design supply temperature is 180F and design return temperature is 130F: `if ( fluid_loop_b.heating_design_and_control.design_supply_temperature == 180 ) AND ( fluid_loop_b.heating_design_and_control.design_return_temperature == 130 ): PASS`

    - Case 2: Else, save component ID to output array for failed components:: `else: FAIL and failed_components_array.append(fluid_loop_b)`

**Rule Assertion - RMR:**

- Case 1: If all components pass: `if ALL_COMPONENTS == PASS: PASS`

- Case 2: Else, list all failed components' ID: `else: FAIL and raise_message ${failed_components_array}`

**[Back](../_toc.md)**

**Notes:**

1. This logic only checks all fluid loops connected to boilers meet the requirement. Other heating loops that are not connected to boilers will not be checked. But these rules will fail the "one-loop" check.
