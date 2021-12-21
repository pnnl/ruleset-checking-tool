
# CHW&CW - Rule 22-4  

**Rule ID:** 22-4  
**Rule Description:** For Baseline chilled water loop that is not purchased chilled water and does not serve any computer room HVAC systems, chilled-water supply temperature shall be reset using the following schedule: 44F at outdoor dry-bulb temperature of 80F and above, 54F at 60F and below, and ramped linearly between 44F and 54F at temperature between 80F and 60F.  
**Rule Assertion:** B-RMR = expected value  
**Appendix G Section:** Section 22 CHW&CW Loop  
**Appendix G Section Reference:** Section G3.1.3.9 Chilled-water supply temperature reset (System 7, 8, 11, 12 and 13)  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  

1. Pass Rule 22-4, Baseline chilled-water supply temperature shall be reset based on outdoor dry-bulb temperature if Baseline chilled water loop is not purchased cooling and loop does not serve any Baseline System Type-11.

**Manual Check:** None  
**Evaluation Context:** Building  
**Data Lookup:** None  
**Function Call:** None  

**Applicability Checks:**  

1. Pass Rule 22-4: `if Rule-22-4 == "PASS":`

## Rule Logic:  

- For each chiller in B_RMR, save chiller to loop-chiller dictionary: `for chiller_b in B_RMR.ASHRAE229.chillers: loop_chiller_dict[chiller_b.cooling_loop].append(chiller_b)`

- For each fluid loop in B_RMR: `for fluid_loop_b in B_RMR.ASHRAE229.fluid_loops:`

  - Check if fluid loop is connected to chiller(s): `if fluid_loop_b in loop_chiller_dict.keys()`

    **Rule Assertion - Component:**

    - Case 1: For Baseline chilled water loop that is not purchased cooling and does not serve any Baseline System Type-11, if chilled-water supply temperature is reset to 44F at outdoor dry-bulb temperature of 80F and above, 54F at 60F and below, and ramped linearly between 44F and 54F at temperature between 80F and 60F: `if ( fluid_loop_b.cooling_or_condensing_design_and_control.outdoor_high_for_loop_supply_temperature_reset == 80 ) AND ( fluid_loop_b.cooling_or_condensing_design_and_control.outdoor_low_for_loop_supply_temperature_reset == 60 ) AND ( fluid_loop_b.cooling_or_condensing_design_and_control.loop_supply_temperature_at_outdoor_high == 44 ) AND ( fluid_loop_b.cooling_or_condensing_design_and_control.loop_supply_temperature_at_outdoor_low == 54 ): PASS`

    - Case 2: Else, save component ID to output array for failed components:: `else: FAIL and failed_components_array.append(fluid_loop_b)`

**Rule Assertion - RMR:**

- Case 1: If all components pass: `if ALL_COMPONENTS == PASS: PASS`

- Case 2: Else, list all failed components' ID: `else: FAIL and raise_message ${failed_components_array}`

**[Back](../_toc.md)**
