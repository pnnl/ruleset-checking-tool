
# Boiler - Rule 21-6  

**Rule ID:** 21-6  
**Rule Description:** When baseline building includes two boilers each shall stage as required by load.  
**Rule Assertion:** B-RMR  
**Appendix G Section:** Section 21 Boiler  
**Appendix G Section Reference:** Section G3.1.3.2 Building System-Specific Modeling Requirements for the Baseline model  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  

1. P-RMR is not modeled with purchased heating.
2. B-RMR is modeled with at least one air-side system that is Type-1a, 7, 11, 12 or that is Type-1, 5, 7, 11, 12.
3. B-RMR HHW loop is modeled with two boilers.

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

  - Check if fluid loop type is heating: `if fluid_loop_b.type == "HEATING":`

    - Get all boilers on loop: `boilers_array = loop_boiler_dict[hhw_loop]`

      - Check if loop has two boilers, loop is applicable: `if boilers_array.length == 2: component_applicability_flag = TRUE`

        - Get both boilers on loop: `boiler_1 = B_RMR.ASHRAE229.boilers[0], boiler_2 = B_RMR.ASHRAE229.boilers[1]`

          **Rule Assertion - Component:**

            - Case 1: If boiler_1's operation lower limit is 0 and operation upper limit is equal to its rated capacity, and boiler_2's operation lower limit is equal to its rated capacity and operation upper limit is equal to twice its rated capacity: `if ( boiler_1.operation_lower_limit == 0 ) AND ( boiler_1.operation_upper_limit == boiler_1.rated_capacity ) AND ( boiler_2.operation_lower_limit == boiler_2.rated_capacity ) AND ( boiler_2.operation_upper_limit == boiler_2.rated_capacity * 2 ): PASS`

            - Case 2: Else if boiler_2's operation lower limit is 0 and operation upper limit is equal to its rated capacity, and boiler_1's operation lower limit is equal to its rated capacity and operation upper limit is equal to twice its rated capacity: `if ( boiler_2.operation_lower_limit == 0 ) AND ( boiler_2.operation_upper_limit == boiler_2.rated_capacity ) AND ( boiler_1.operation_lower_limit == boiler_1.rated_capacity ) AND ( boiler_1.operation_upper_limit == boiler_1.rated_capacity * 2 ): PASS`

            - Case 3: Else, save component ID to output array for failed components: `else: FAIL and failed_components_array.append(fluid_loop_b.id).`

**Rule Assertion - RMR:**

- Case 1: If all components pass: `if ALL_COMPONENTS == PASS: PASS`

- Case 2: Else, list all failed components' ID: `else: FAIL and raise_message ${failed_components_array}`

**[Back](../_toc.md)**
