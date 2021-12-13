
# CHW&CW - Rule 22-7  

**Rule ID:** 22-7  
**Rule Description:** Baseline chilled water system that does not use purchased chilled water shall be modeled as primary/secondary systems.  
**Rule Assertion:** B-RMR = expected value  
**Appendix G Section:** Section 22 CHW&CW Loop  
**Appendix G Section Reference:** Section G3.1.3.10 Chilled-water supply temperature reset (System 7, 8, 11, 12 and 13)  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  

1. B-RMR is modeled with at least one air-side system that is Type-7, 8, 11, 12, or 13.
2. B-RMR is not modeled with purchased chilled water.
3. Pass Rule 22-34, Baseline must only have no more than one CHW plant.

**Manual Check:** None  
**Evaluation Context:** Building  
**Data Lookup:** None  
**Function Call:** None  

**Applicability Checks:**  

1. B-RMR is modeled with at least one air-side system that is Type-7, 8, 11, 12, or 13: `PLACEHOLDER`
2. B-RMR is not modeled with purchased chilled water: `if Rule-18-8 == "NOT APPLICABLE":`
3. Pass Rule 22-34, Baseline must only have no more than one CHW plant: `if Rule-22-34 == "PASS":`

## Rule Logic:  

- For each building segment in B_RMR: `for building_segment_b in B_RMR...building_segments:` (See Note#1)

  - For each HVAC system in building segment: `for hvac_b in building_segment_b.heating_ventilation_air_conditioning_systems`

    - Check if HVAC system has chilled water coil: `if hvac_b.cooling_system.chilled_water_loop:`

      - Save chilled water loop that serves cooling systems to secondary CHW loop array: `secondary_chw_loop_array.append(hvac_b.cooling_system.chilled_water_loop)`

- Get primary CHW loop in B_RMR `primary_chw_loop_b = B_RMR.ASHRAE229.chillers[0].cooling_loop`

  - Check if primary CHW loop serve any cooling coils, set check coil flag to True: `if primary_chw_loop_b in secondary_chw_loop_array: check_coil_flag = TRUE`

  - Check if primary CHW loop is not modeled with one secondary loop, set check number flag to True: `if LEN(primary_chw_loop_b.child_loops) != 1: check_number_flag = TRUE`

  - Check if all loops in secondary CHW loop array are not the same as child loops of primary CHW loop, set check secondary loop flag to True: `if secondary_chw_loop_array == primary_chw_loop_b.child_loops: check_secondary_loop_flag = TRUE`

**Rule Assertion:**

- Case 1: If the CHW loop served by chiller(s) is connected to any HVAC system cooling coils: `if check_coil_flag: FAIL`

- Case 2: Else if the CHW loop served by chiller has more than one child loop: `else if check_number_flag: FAIL`

- Case 3: Else if HVAC system cooling coils are connected to CHW loops other than the child loop of the CHW loop served by chiller(s): `else if check_secondary_loop_flag: FAIL`

- Case 4: Else: `else: PASS`

**[Back](../_toc.md)**

**Notes:**

1. Is there only one CHW plant per RMR or per building?
