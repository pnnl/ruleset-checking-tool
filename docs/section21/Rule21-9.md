
# Boiler - Rule 21-9  

**Rule ID:** 21-9  
**Rule Description:** When baseline building includes boilers, Hot Water Pump Power = 19W/gpm.  
**Rule Assertion:** B-RMR = expected value  
**Appendix G Section:** Section 21 Boiler  
**Appendix G Section Reference:** Section G3.1.3.5 Building System-Specific Modeling Requirements for the Baseline model  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  

1. P-RMR is not modeled with purchased heating.
2. B-RMR is modeled with at least one air-side system that is Type-1a, 7, 11, 12 or that is Type-1, 5, 7, 11, 12.

**Manual Check:** None  
**Evaluation Context:** Building  
**Data Lookup:** None  
**Function Call:**  

1. check_purchased_chw_hhw()

**Applicability Checks:**  

1. Check if P-RMR is modeled with purchased cooling or purchased hot water/steam: `purchased_chw_hhw_status_dict = check_purchased_chw_hhw(P_RMR)`

  - If P-RMR is modeled with purchased hot water/steam, rule is not applicable: `if purchased_chw_hhw_status_dict["PURCHASED_HEATING"]: rule_applicability_flag = FALSE`

  - Else, P-RMR is not modeled with purchased hot water/steam, continue to next applicability check: `if NOT purchased_chw_hhw_status_dict["PURCHASED_HEATING"]:`

2. B-RMR is modeled with at least one air-side system that is Type-1a, 7, 11, 12 or that is Type-1, 5, 7, 11, 12:

  - If P-RMR is not modeled with purchased cooling: `if NOT purchased_chw_hhw_status_dict["PURCHASED_COOLING"]:`

    - Check if B-RMR is modeled with at least one air-side system that is Type-1, 5, 7, 11 or 12, continue to rule logic: `PLACEHOLDER`

    - Else, rule is not applicable: `else: rule_applicability_flag = FALSE`

  - Else, P-RMR is modeled with purchased cooling: `else:`

    - Check if B-RMR is modeled with at least one air-side system that is Type-1a, 7, 11 or 12, continue to rule logic: `PLACEHOLDER`

    - Else, rule is not applicable: `else: rule_applicability_flag = FALSE`

## Rule Logic:  

- For each boiler in B_RMR, save boiler to loop boiler dictionary: `for boiler_b in B_RMR.ASHRAE229.boilers: loop_boiler_dict[boiler_b.loop].append(boiler_b)`

- For each fluid loop in B_RMR: `for fluid_loop_b in B_RMR.ASHRAE229.fluid_loops:`

  - Check if fluid loop is connected to boiler(s): `if fluid_loop_b in loop_boiler_dict.keys()`

    **Rule Assertion - Component:**

    - Case 1: For heating hot water loop that boiler serves, if total pump power per flow rate is equal to 19W/gpm: `if fluid_loop_b.pump_power_per_flow_rate == 19: PASS`

    - Case 2: Else, save component ID to output array for failed components:: `else: FAIL and failed_components_array.append(fluid_loop_b)`

**Rule Assertion - RMR:**

- Case 1: If all components pass: `if ALL_COMPONENTS == PASS: PASS`

- Case 2: Else, list all failed components' ID: `else: FAIL and raise_message ${failed_components_array}`

**[Back](../_toc.md)**

**Notes:**

1. This rule does not check any pump power on heating loop that is not connected to boiler(s). If RMR has heating loop not connected to boiler(s), it will fail the one HHW loop rule. 
