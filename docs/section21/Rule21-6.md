
# Boiler - Rule 21-6  

**Rule ID:** 21-6  
**Rule Description:** When baseline building includes two boilers each shall stage as required by load.  
**Rule Assertion:** B-RMR  
**Appendix G Section:** Section 21 Boiler  
**Appendix G Section Reference:** Section G3.1.3.2 Building System-Specific Modeling Requirements for the Baseline model  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  

1. B-RMR pass Rule 21-5.
2. B-RMR is modeled with two boilers on each heating fluid loop.

**Manual Check:** None  
**Evaluation Context:** Building  
**Data Lookup:** None  
**Function Call:** None  

**Applicability Checks 1:**  

1. B-RMR pass Rule 21-5: `if Rule-21-5 == PASS:`

## Rule Logic:  

- For each boiler in B_RMR, save boiler to loop boiler dictionary: `for boiler_b in B_RMR.ASHRAE229.boilers: loop_boiler_dict[boiler_b.loop].append(boiler_b)`

- For each fluid loop in B_RMR: `for fluid_loop_b in B_RMR.ASHRAE229.fluid_loops:`

  - Check if fluid loop type is heating: `if fluid_loop_b.type == "HEATING":`

    - Get all boilers on loop: `boilers_array = loop_boiler_dict[hhw_loop]`

      - Check if loop has two boilers, set applicability flag: `if boilers_array.length == 2: rule_applicability_check = TRUE`

        - Get both boilers on loop: `boiler_1 = B_RMR.ASHRAE229.boilers[0], boiler_2 = B_RMR.ASHRAE229.boilers[1]`

            **Rule Assertion - Component:**

              - Case 1: If boiler_1's operation lower limit is 0 and operation upper limit is equal to its rated capacity, and boiler_2's operation lower limit is equal to its rated capacity and operation upper limit is equal to twice its rated capacity: `if ( boiler_1.operation_lower_limit == 0 ) AND ( boiler_1.operation_upper_limit == boiler_1.rated_capacity ) AND ( boiler_2.operation_lower_limit == boiler_2.rated_capacity ) AND ( boiler_2.operation_upper_limit == boiler_2.rated_capacity * 2 ): PASS`

              - Case 2: If boiler_2's operation lower limit is 0 and operation upper limit is equal to its rated capacity, and boiler_1's operation lower limit is equal to its rated capacity and operation upper limit is equal to twice its rated capacity: `if ( boiler_2.operation_lower_limit == 0 ) AND ( boiler_2.operation_upper_limit == boiler_2.rated_capacity ) AND ( boiler_1.operation_lower_limit == boiler_1.rated_capacity ) AND ( boiler_1.operation_upper_limit == boiler_1.rated_capacity * 2 ): PASS`

              - Case 3: Else, save component ID to output array for failed components: `else: FAIL and failed_components_array.append(boiler_1.id, boiler_2.id).`

**Applicability Check 2:**

1. Rule is applicable if P-RMR is modeled with purchased hot water or steam: `if rule_applicability_check: is_applicable = TRUE`

**Rule Assertion - RMR:**

- Case 1: If all components pass: `if ALL_COMPONENTS == PASS: PASS`

- Case 2: Else, list all failed components' ID: `else: FAIL and raise_message ${failed_components_array}`

**[Back](../_toc.md)**
