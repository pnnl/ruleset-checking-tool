
# CHW&CW - Rule 22-7  

**Rule ID:** 22-7  
**Rule Description:** Baseline chilled water system that does not use purchased chilled water shall be modeled as primary/secondary systems.  
**Rule Assertion:** B-RMR = expected value  
**Appendix G Section:** Section 22 CHW&CW Loop  
**Appendix G Section Reference:** Section G3.1.3.10 Chilled-water supply temperature reset (System 7, 8, 11, 12 and 13)  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  

1. B-RMR is not modeled with purchased chilled water.

**Manual Check:** None  
**Evaluation Context:** Building  
**Data Lookup:** None  
**Function Call:** None  

**Applicability Checks:**  

1. B-RMR is not modeled with purchased chilled water: `if Rule-18-8 == "NOT APPLICABLE":`

## Rule Logic:  

- For each building segment in B_RMR: `for building_segment_b in B_RMR...building_segments:`

  - For each HVAC system in building segment: `for hvac_b in building_segment_b.heating_ventilation_air_conditioning_systems`

    - Check if HVAC system has chilled water coil: `if hvac_b.cooling_system.chilled_water_loop:`

      - Save chilled water loop that serves cooling systems to secondary CHW loop array: `secondary_chw_loop_array.append(hvac_b.cooling_system.chilled_water_loop)`

- For each chiller in B_RMR, save chiller to loop-chiller dictionary: `for chiller_b in B_RMR.ASHRAE229.chillers: loop_chiller_dict[chiller_b.cooling_loop].append(chiller_b)`

- For each fluid loop in B_RMR: `for fluid_loop_b in B_RMR.ASHRAE229.fluid_loops:`

  - Check if fluid loop is connected to chiller(s): `if fluid_loop_b in loop_chiller_dict.keys()`

    - Check if fluid loop serves any cooling coils, set check coil flag to True: `if fluid_loop_b in secondary_chw_loop_array: check_coil_flag = TRUE`

    - Check if fluid loop is not modeled with one secondary loop, set check number flag to True: `if LEN(fluid_loop_b.child_loops) != 1: check_number_flag = TRUE`

    - Check if secondary CHW loop array are not the same as child loops of primary CHW loop, set check secondary loop flag to True: `if secondary_chw_loop_array == fluid_loop_b.child_loops: check_secondary_loop_flag = TRUE`

**Rule Assertion - RMR:**

- Case 1: If the CHW loop served by chiller(s) is connected to any HVAC system cooling coils: `if check_coil_flag: FAIL`

- Case 2: Else if the CHW loop served by chiller has more than one child loop: `else if check_number_flag: FAIL`

- Case 3: Else if HVAC system cooling coils are connected to CHW loops other than the child loop of the CHW loop served by chiller(s): `else if check_secondary_loop_flag: FAIL`

- Case 4: Else: `else: PASS`

**[Back](../_toc.md)**
