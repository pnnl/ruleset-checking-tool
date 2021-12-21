
# CHW&CW - Rule 22-8  

**Rule ID:** 22-8  
**Rule Description:** For Baseline chilled water system with cooling capacity of 300 tons or more, the secondary pump shall be modeled with variable-speed drives.  
**Rule Assertion:** B-RMR = expected value  
**Appendix G Section:** Section 22 CHW&CW Loop  
**Appendix G Section Reference:** Section G3.1.3.10 Chilled-water supply temperature reset (System 7, 8, 11, 12 and 13)  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  

1. B-RMR passes Rule 22-7, Baseline chilled water system that does not use purchased chilled water shall be modeled as primary/secondary systems.

**Manual Check:** None  
**Evaluation Context:** Building  
**Data Lookup:** None  
**Function Call:** None  

**Applicability Checks:**  

1. B-RMR passes Rule 22-7: `if Rule-22-7 == "PASS":`

## Rule Logic:  

- For each pump in B_RMR: `for pump_b in B_RMR.ASHRAE229.pumps:`

  - Save loop served by pump and pump to a dictionary: `loop_pump_dictionary[pump_b.loop_or_piping].append(pump)`

- For each chiller in B_RMR: `for chiller_b in B_RMR.ASHRAE229.chillers:`

  - Get cooling loop that chiller servers: `chw_loop_b = chiller_b.cooling_loop`

    - Add chiller rated capacity to CHW loop total capacity: `chw_loop_capacity_dict[chw_loop_b] += chiller_b.rated_capacity`

- For each CHW loop that chiller serves: `for primary_loop_b in chw_loop_capacity_dict.keys():`

  - Check if CHW loop total cooling capacity is 300 tons or more: `if chw_loop_capacity_dict[primary_loop_b] >= 300 * CONVERSION(TON_TO_BTUH):`

    - For each secondary loop served by primary CHW loop: `for secondary_loop_b in primary_loop_b.child_loops:`

      - For each secondary pump associated with secondary loop: `for secondary_pump in loop_pump_dictionary[secondary_loop_b]:`

        **Rule Assertion - Component:**

        - Case 1: If secondary pump is modeled with variable-speed drives: `if secondary_pump.speed_control == "VARIABLE_SPEED": PASS`

        - Case 2: Else, save component ID to output array for failed components:: `else: FAIL and failed_components_array.append(secondary_pump)`

**Rule Assertion - RMR:**

- Case 1: If all components pass: `if ALL_COMPONENTS == PASS: PASS`

- Case 2: Else, list all failed components' ID: `else: FAIL and raise_message ${failed_components_array}`

**[Back](../_toc.md)**
