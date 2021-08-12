
# Lighting - Rule 6-13

**Rule ID:** 6-13  
**Rule Description:** Additional occupancy sensor controls in the proposed building are modeled through schedule adjustments based on factors defined in Table G3.7.  
**Rule Assertion:** Proposed RMR = expected value  
**Appendix G Section:** Section G3.1-6(i) Modeling Requirements for the Proposed design  
**Appendix G Section Reference:**  

- Table G3.7, Performance Rating Method Lighting Power Density Allowances and Occupancy Sensor Reductions Using the Space-by-Space Method  

**Applicability:** All required data elements exist for P_RMR  
**Applicability Checks:**  

  1. Pass Rule 6-10.

**Manual Check:** Yes  
**Evaluation Context:** Each Data Element  
**Data Lookup:** Table G3.7  
**Function Call:**  

  - compare_schedules()
  - normalize_space_lighting_schedule()

## Rule Logic:  

- **Applicability Check 1:** If pass Rule 6-10: `if rule_6_10 == TRUE:`  

- Get building open schedule in the proposed model: `building_open_schedule_p = P_RMR.building.building_open_schedule`  

- For each building segment in building: `for building_segment_p in P_RMR.building.building_segments:`  

  - For each thermal block in building segment: `thermal_block_p in building_segment_p.thermal_blocks:`  

    - For each zone in thermal block: `zone_p in thermal_block_p.zones:`  

      - For each space in zone: `space_p in zone_p.spaces:`  

        - Get matching space from B_RMR: `space_b = match_data_element(B_RMR, Spaces, space_p.id)`  

          - Get normalized space lighting schedule for B_RMR: `normalized_schedule_b = normalize_space_lighting_schedule(space_b)`  

        - Get lighting space type: `lighting_space_type_p = space_p.lighting_space_type`  

          - If lighting space type is employee lunch and break rooms, conference/meeting rooms, or classrooms (not including shop classrooms, laboratory classrooms, and preschool through 12th-grade classrooms), get baseline lighting occupancy sensor reduction factor from Table G3.7: `if lighting_space_type_p in ["LOUNGE/BREAKROOM", "CONFERENCE/MEETING/MULTIPURPOSE ROOM", "CLASSROOM/LECTURE HALL/TRAINING ROOM - PENITENTIARY", "CLASSROOM/LECTURE HALL/TRAINING ROOM - ALL OTHER"]: reduction_factor_b = data_lookup(table_G3_7, lighting_space_type_p, "FULL-AUTO ON")`  

          - Else, set baseline reduction factor to 0: `else: reduction_factor_b = 0`  

        - For each lighting in space: `lighting_p in space_p.interior_lighting:`  

          - Get lighting control type: `lighting_control_type_p = lighting_p.occupancy_control_type`  

          - Get lighting occupancy sensor reduction factor from Table G3.7: `reduction_factor_p = data_lookup(table_G3_7, lighting_space_type_p, lighting_control_type_p)`  

          - Calculate adjusted lighting occupancy sensor reduction factor based on B_RMR: `adjusted_reduction_factor_p = ( 1 - reduction_factor_p ) / ( 1 - reduction_factor_b )`  

          - Get lighting schedule: `lighting_schedule_p = lighting_p.lighting_multiplier_schedule`  

          - Compare lighting schedules in P_RMR and B_RMR: `schedule_comparison_result = compare_schedules(lighting_schedule_p, normalized_schedule_b, building_open_schedule_p, adjusted_reduction_factor_p)`  

            **Rule Assertion:**

            - Case 1: For all hours, for each lighting, if lighting schedule in P_RMR is equal to lighting schedule in B_RMR times adjusted lighting occupancy sensor reduction factor: `if schedule_comparison_result == "MATCH": PASS`  

            - Case 2: Else if lighting schedule in P_RMR is lower than or equal to lighting schedule in B_RMR times adjusted lighting occupancy sensor reduction factor: `if schedule_comparison_result == "EQUAL AND LESS": CAUTION`  

            - Case 3: Else, lighting schedule in P_RMR is higher than lighting schedule in B_RMR times adjusted lighting occupancy sensor reduction factor: `if schedule_comparison_result == "EQUAL AND MORE": FAIL`  

**Temporary Function note:**

`compare_schedule_result = compare_schedules(lighting_schedule_p, normalized_schedule_b, building_open_schedule_p, reduction_factor_p)`

(4 inputs, Schedule 1, Schedule 2, Mask Schedule, comparison factor)

- Schedule 2 as the comparison basis, i.e. Schedule 1 = Schedule 2 * comparison factor
- When Mask Schedule hourly value is 0, schedules need to be the same at that hour. If Mask Schedule hourly value is 1, Schedule 1 needs to be comparison factor times Schedule 2 at that hour
- can return "match", "equal and less", "equal and more", "equal, less and more", with bin data, TBD

