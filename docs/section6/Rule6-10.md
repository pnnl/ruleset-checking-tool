
# Lighting - Rule 6-10  

**Rule ID:** 6-10  
**Rule Description:** Baseline building is modeled with occupancy sensor controls in applicable space types, i.e. employee lunch and break rooms, conference/meeting rooms, and classrooms (not including shop classrooms, laboratory classrooms, and preschool through 12th-grade classrooms).  
**Appendix G Section Reference:** Section G3.1-6 Modeling Requirements for the baseline building  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:** None  

**Manual Check:** Yes  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  
**Function Call:**  

  - compare_schedules()
  - normalize_space_lighting_schedule()

## Rule Logic: 

- Get building open schedule in the baseline model: `building_open_schedule_b = B_RMR.building.building_open_schedule`  

- For each building segment in building: `building_segment_b in B_RMR.building.building_segments:`  

  - For each thermal block in building segment: `thermal_block_b in building_segment_b.thermal_blocks:`  

    - For each zone in thermal block: `zone_b in thermal_block_b.zones:`  

      - For each space in zone: `space_b in zone_b.spaces:`  

        - Get interior lighting in space: `interior_lighting_b = space_b.interior_lighting`  

          - Get interior lighting occupancy control type: `control_type_b = interior_lighting_b.occupancy_control_type`  

        - Get normalized space lighting schedule: `normalized_schedule_b = normalize_space_lighting_schedule(space_b)`  

        - Get matching space in P_RMR: `space_p = match_data_element(P_RMR, Spaces, space_b.id)`  

          - Get normalized space lighting schedule: `normalized_schedule_p = normalize_space_lighting_schedule(space_p)`  

        - Compare lighting schedule in B_RMR and P_RMR: `schedule_comparison_result = compare_schedules(normalized_schedule_b, normalized_schedule_p, building_open_schedule_b, 1)`  

        - Get lighting space type: `lighting_space_type_b = space_b.lighting_space_type`  

          - If lighting space types is employee lunch and break rooms, conference/meeting rooms, or classrooms (not including shop classrooms, laboratory classrooms, and preschool through 12th-grade classrooms), set occupancy sensor flag: `if lighting_space_type_b in ["LOUNGE/BREAKROOM", "CONFERENCE/MEETING/MULTIPURPOSE ROOM", "CLASSROOM/LECTURE HALL/TRAINING ROOM - PENITENTIARY", "CLASSROOM/LECTURE HALL/TRAINING ROOM - ALL OTHER"]: occ_sensor_flag = TRUE`  

          **Rule Assertion:**  

          - Case 1: If space requires occupancy sensor and interior lighting is modeled with full-auto on occupancy sensor control: `if ( occ_sensor_flag ) and ( control_type_b == "FULL-AUTO ON" ): PASS and return schedule_comparison_result`  

          - Case 2: If space requires occupancy sensor and interior lighting is not modeled with full-auto on occupancy sensor control: `if ( occ_sensor_flag ) and ( control_type_b != "FULL-AUTO ON" ): FAIL`  

          - Case 3: If space does not require occupancy sensor and interior lighting is modeled with full-auto on occupancy sensor control: `if ( NOT occ_sensor_flag ) and ( control_type_b == "FULL-AUTO ON" ): FAIL`  

          - Case 4: If space does not require occupancy sensor and interior lighting is not modeled with full-auto on occupancy sensor control: `if ( NOT occ_sensor_flag ) and ( control_type_b != "FULL-AUTO ON" ): PASS and return schedule_comparison_result`  
 
**Temporary Function note:**

`compare_schedule_result = compare_schedules(lighting_schedule_p, normalized_schedule_b, building_open_schedule_p, reduction_factor_p)`

(4 inputs, Schedule 1, Schedule 2, Mask Schedule, comparison factor)

- Schedule 2 as the comparison basis, i.e. Schedule 1 = Schedule 2 * comparison factor
- When Mask Schedule hourly value is 0, schedules need to be the same at that hour. If Mask Schedule hourly value is 1, Schedule 1 needs to be comparison factor times Schedule 2 at that hour
- can return "match", "equal and less", "equal and more", "equal, less and more", with bin data, TBD
