
# CHW&CW - Rule 22-9  

**Schema Version:** 0.0.10  
**Mandatory Rule:** True  
**Rule ID:** 22-9  
**Rule Description:** For Baseline chilled water system with cooling capacity of 300 tons or more, the secondary loop shall be modeled with a minimum flow of 25% of the design flow rate.  
**Rule Assertion:** B-RMR = expected value  
**Appendix G Section:** Section 22 CHW&CW Loop  
**90.1 Section Reference:** Section G3.1.3.10 Chilled-water pumps (System 7, 8, 11, 12 and 13)  
**Data Lookup:** None  
**Evaluation Context:** Building  
**Applicability Checks:**  

1. B-RMR is modeled with at least one air-side system that is Type-7, 8, 11, 12, 13, 7b, 8b, 11.1b, 12b.
2. B-RMR is modeled with primary-secondary configuration.
3. B-RMR chilled water system cooling capacity is 300 tons or more.

**Function Calls:**  

1. get_baseline_system_types()
2. get_primary_secondary_loops_dict()
3. get_component_by_id()

**Applicability Checks:**  

- **Check 1:** Get B-RMR system types: `baseline_hvac_system_dict = get_baseline_system_types(B-RMR)`

  - Check if B-RMR is modeled with at least one air-side system that is Type-7, 8, 11.1, 11.2, 12, 13, 7b, 8b, 11.1b, 12b, i.e. with air-side system served by chiller(s), continue to the next applicability check: `if any(sys_type in baseline_hvac_system_dict.keys() for sys_type in ["SYS-7", "SYS-8", "SYS-11.1", "SYS-11.2", "SYS-12", "SYS-13", "SYS-7B", "SYS-8B", "SYS-11.1B", "SYS-12B"]): NEXT_APPLICABILITY_CHECK`

  - Else, rule is not applicable to B-RMR: `else: RULE_NOT_APPLICABLE`

- **Check 2:** Get primary and secondary loops for B-RMR: `primary_secondary_loop_dictionary = get_primary_secondary_loops_dict(B_RMR)`

  - Check if B-RMR is modeled with primary-secondary configuration, continue to rule logic: `if LEN(primary_secondary_loop_dictionary) != 0: CHECK_RULE_LOGIC`

  - Else, rule is not applicable to B-RMR: `else: RULE_NOT_APPLICABLE`

## Rule Logic:  

- For each chiller in B_RMR: `for chiller_b in B_RMR.RulesetModelInstance.chillers:`

  - Get cooling loop that chiller serves: `chw_loop_b_id = chiller_b.cooling_loop`

    - Add chiller rated capacity to primary CHW loop total capacity: `chw_loop_capacity_dict[chw_loop_b_id] += chiller_b.rated_capacity`

- For each primary CHW loop: `for loop_b_id in primary_secondary_loop_dictionary["PRIMARY"]:`

  - Check if CHW primary loop total cooling capacity is 300 tons or more: `if chw_loop_capacity_dict[loop_b_id] >= 300 * CONVERSION(TON_TO_BTUH):`

    - Get primary loop: `primary_loop_b = get_component_by_id(loop_b_id)`

      - For each secondary loop served by primary CHW loop: `for secondary_loop_id_b in primary_loop_b.child_loops:`

        **Rule Assertion - Component:**

        - Case 1: If secondary loop is modeled with a minimum flow of 25% of the design flow rate: `if secondary_loop_id_b.cooling_or_condensing_design_and_control.minimum_flow_fraction == 0.25: PASS`

        - Case 2: Else: `else: FAIL`

**[Back](../_toc.md)**
