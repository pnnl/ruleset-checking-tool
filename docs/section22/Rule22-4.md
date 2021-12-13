
# CHW&CW - Rule 22-4  

**Rule ID:** 22-4  
**Rule Description:** For Baseline chilled water loop that is not purchased chilled water and does not serve any computer room HVAC systems, chilled-water supply temperature shall be reset using the following schedule: 44F at outdoor dry-bulb temperature of 80F and above, 54F at 60F and below, and ramped linearly between 44F and 54F at temperature between 80F and 60F.  
**Rule Assertion:** B-RMR = expected value  
**Appendix G Section:** Section 22 CHW&CW Loop  
**Appendix G Section Reference:** Section G3.1.3.9 Chilled-water supply temperature reset (System 7, 8, 11, 12 and 13)  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  

1. B-RMR is modeled with at least one air-side system that is Type-7, 8, 12, or 13
2. B-RMR is not modeled with any air-side system that is type-11.
3. B-RMR is not modeled with purchased chilled water.
4. Pass Rule 22-34, Baseline must only have no more than one CHW plant.
5. Pass Rule 22-7, Baseline chilled water system that does not use purchased chilled water shall be modeled as primary/secondary systems.

**Manual Check:** None  
**Evaluation Context:** Building  
**Data Lookup:** None  
**Function Call:** None  

**Applicability Checks:**  

1. B-RMR is modeled with at least one air-side system that is Type-7, 8, 12, or 13: `PLACEHOLDER:`
2. B-RMR is not modeled with any air-side system that is Type-11: `PLACEHOLDER`
3. B-RMR is not modeled with purchased chilled water: `if Rule-18-8 == "NOT APPLICABLE":`
4. Pass Rule 22-34, Baseline must only have no more than one CHW plant: `if Rule-22-34 == "PASS":`
5. Pass Rule 22-7, Baseline chilled water system that does not use purchased chilled water shall be modeled as primary/secondary systems: `if Rule-22-7 == "PASS":`

## Rule Logic:  

- Get primary CHW loop in B_RMR `primary_chw_loop_b = B_RMR.ASHRAE229.chillers[0].cooling_loop`

  **Rule Assertion:**

  - Case 1: For Baseline chilled water loop that is not purchased cooling and does not serve any Baseline System Type-11, if chilled-water supply temperature is reset to 44F at outdoor dry-bulb temperature of 80F and above, 54F at 60F and below, and ramped linearly between 44F and 54F at temperature between 80F and 60F: `if ( primary_chw_loop_b.cooling_or_condensing_design_and_control.outdoor_high_for_loop_supply_temperature_reset == 80 ) AND ( primary_chw_loop_b.cooling_or_condensing_design_and_control.outdoor_low_for_loop_supply_temperature_reset == 60 ) AND ( primary_chw_loop_b.cooling_or_condensing_design_and_control.loop_supply_temperature_at_outdoor_high == 44 ) AND ( primary_chw_loop_b.cooling_or_condensing_design_and_control.loop_supply_temperature_at_outdoor_low == 54 ): PASS`

  - Case 2: Else: `else: FAIL`

**[Back](../_toc.md)**
