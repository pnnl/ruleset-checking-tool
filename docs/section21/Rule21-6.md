
# Boiler - Rule 21-6  

**Rule ID:** 21-6  
**Rule Description:** When baseline building includes two boilers each shall stage as required by load.  
**Rule Assertion:** B-RMR  
**Appendix G Section:** Section 21 Boiler  
**Appendix G Section Reference:** Section G3.1.3.2 Building System-Specific Modeling Requirements for the Baseline model  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  

1. B-RMR is modeled with at least one air-side system that is Type-1, 5, 7, 11.2, 12, 1a, 7a, 11.2a, 12a.

**Manual Check:** None  
**Evaluation Context:** Building  
**Data Lookup:** None  
**Function Call:**  

1. get_baseline_system_types()
2. baseline_system_type_compare()

**Applicability Checks:**  

- Get B-RMR system types: `baseline_hvac_system_dict = get_baseline_system_types(B-RMR)`

  - Check if B-RMR is modeled with at least one air-side system that is Type-1, 5, 7, 11.2, 12, 1a, 7a, 11.2a, 12a, continue to rule logic: if any(baseline_system_type_compare(sys_type, target_system_type, true) for sys_type in baseline_hvac_system_dict.keys() for target_system_type in [HVAC.SYS_1, HVAC.SYS_5, HVAC.SYS_7, HVAC.SYS_11_2, HVAC.SYS_12, HVAC.SYS_1A, HVAC.SYS_7A, HVAC.SYS_11_2A, HVAC.SYS_12A]): CHECK_RULE_LOGIC

  - Else, rule is not applicable to B-RMR: `else: RULE_NOT_APPLICABLE`

## Rule Logic:  

- For each boiler in B_RMR, save boiler to loop boiler dictionary: `for boiler_b in B_RMR.RulesetModelInstance.boilers: loop_boiler_dict[boiler_b.loop].append(boiler_b)`

- For each fluid loop in B_RMR: `for fluid_loop_b in B_RMR.RulesetModelInstance.fluid_loops:`

  - Check if fluid loop type is heating: `if fluid_loop_b.type == "HEATING":`

    - Get all boilers on loop: `boilers_array = loop_boiler_dict[hhw_loop]`

      - Check if loop has two boilers: `if boilers_array.length == 2:`

        - Get both boilers on loop: `boiler_1 = boilers_arrays[0], boiler_2 = boilers_array[1]`

          **Rule Assertion - Component:**

            - Case 1: If boiler_1's operation lower limit is 0 and operation upper limit is equal to its rated capacity, and boiler_2's operation lower limit is equal to boiler_1 rated capacity and operation upper limit is equal to the sum of boiler 1 and boiler 2 rated capacity: `if ( boiler_1.operation_lower_limit == 0 ) AND ( boiler_1.operation_upper_limit == boiler_1.rated_capacity ) AND ( boiler_2.operation_lower_limit == boiler_1.rated_capacity ) AND ( boiler_2.operation_upper_limit == boiler_21.rated_capacity + boiler_2.rated_capacity ): PASS`

            - Case 2: Else if boiler_2's operation lower limit is 0 and operation upper limit is equal to its rated capacity, and boiler_1's operation lower limit is equal to boiler_2 rated capacity and operation upper limit is equal to the sum of boiler 1 and boiler 2 rated capacity: `if ( boiler_2.operation_lower_limit == 0 ) AND ( boiler_2.operation_upper_limit == boiler_2.rated_capacity ) AND ( boiler_1.operation_lower_limit == boiler_2.rated_capacity ) AND ( boiler_1.operation_upper_limit == boiler_1.rated_capacity + boiler_2.rated_capacity ): PASS`

            - Case 3: Else: `else: FAIL`

**[Back](../_toc.md)**
