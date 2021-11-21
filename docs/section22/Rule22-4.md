
# CHW&CW - Rule 22-4  

**Rule ID:** 22-4  
**Rule Description:** For Baseline chilled water loop that is not purchased chilled water and does not serve any computer room HVAC systems, chilled-water supply temperature shall be reset using the following schedule: 44F at outdoor dry-bulb temperature of 80F and above, 54F at 60F and below, and ramped linearly between 44F and 54F at temperature between 80F and 60F.  
**Rule Assertion:** B-RMR = expected value  
**Appendix G Section:** Section 22 CHW&CW Loop  
**Appendix G Section Reference:** Section G3.1.3.9 Chilled-water supply temperature reset (System 7, 8, 11, 12 and 13)  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  

1. B-RMR is modeled with at least one air-side system that is Type-7, 8, 12, or 13.
2. B-RMR is modeled with at least one chilled water system that does not use purchased chilled water.
3. Pass Rule 22-3.

**Manual Check:** None  
**Evaluation Context:** Building  
**Data Lookup:** None  
**Function Call:** None  

**Applicability Checks:**  

1. B-RMR is modeled with at least one air-side system that is Type-7, 8, 12, or 13: `PLACEHOLDER`

2. B-RMR is modeled with at least one chilled water system that does not use purchased chilled water: `if B_RMR.ASHRAE229.chillers:`

3. Pass Rule 22-3: `if Rule-22-3 == "PASS"`

## Rule Logic:  

- For each HVAC system in B-RMR: `for hvac_b in B-RMR...heating_ventilation_air_conditioning_systems:`

  - Check if HVAC system serves computer room: `if hvac_b.does_serve_computer_room:`

    - Save CHW loop that serves the cooling system of HVAC system serving computer room to an array: `chw_loop_for_computer_room_array.append(hvac_b.cooling_system.chilled_water_loop)`

- For each chiller in B_RMR: `for chiller_b in B_RMR.ASHRAE229.chillers:`

  - Get cooling loop that chiller servers: `chw_loop_b = chiller_b.cooling_loop`

    - If cooling loop has not been saved in CHW loop array and does not serve any computer room HVAC system: `if ( chw_loop_b NOT in chw_loop_array ) AND ( chw_loop_b NOT in chw_loop_for_computer_room_array ):`

      - Save cooling loop to CHW loop array that needs to comply with reset temperature schedule: `chw_loop_array.append(chw_loop_b)`

- For each CHW loop that chiller serves, and does not serve any computer room HVAC system: `for loop_b in chw_loop_array:`

  **Rule Assertion:**

  - Case 1: If chilled-water supply temperature is reset to 44F at outdoor dry-bulb temperature of 80F and above, 54F at 60F and below, and ramped linearly between 44F and 54F at temperature between 80F and 60F: `if ( loop_b.cooling_or_condensing_design_and_control.outdoor_high_for_loop_supply_temperature_reset == 80 ) AND ( loop_b.cooling_or_condensing_design_and_control.outdoor_low_for_loop_supply_temperature_reset == 60 ) AND ( loop_b.cooling_or_condensing_design_and_control.loop_supply_temperature_at_outdoor_high == 44 ) AND ( loop_b.cooling_or_condensing_design_and_control.loop_supply_temperature_at_outdoor_low == 54 ): PASS`

  - Case 2: Else: `else: FAIL`

**[Back](../_toc.md)**

**Notes:**

1. Need to check secondary loop for reset?
