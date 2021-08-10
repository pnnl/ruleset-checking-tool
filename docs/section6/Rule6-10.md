
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

## Rule Logic: 

- For each building_segment in the baseline model: `building_segment_b in B_RMR.building.building_segments:`  

  - For each thermal_block in building segment: `thermal_block_b in building_segment_b.thermal_blocks:`  

    - For each zone in thermal block: `zone_b in thermal_block_b.zones:`  

      - For each space in zone: `space_b in zone_b.spaces:`  

        - Get interior lighting in space: `interior_lighting_b = space_b.interior_lighting`  

          - Get interior lighting occupancy control type: `control_type_b = interior_lighting_b.occupancy_control_type`  

          - Get interior lighting schedule: `lighting_schedule_b = interior_lighting_b.lighting_multiplier_schedule`  

          - Get matching interior lighting schedule in P_RMR: `lighting_schedule_p = match_data_element(P_RMR, Schedules, lighting_schedule_b.id)`  

          - Determine if interior lighting schedule in B_RMR is the same as P_RMR: `schedule_match_flag = compare_schedules(lighting_schedule_b, lighting_schedule_p)`  

        - Get lighting space type: `lighting_space_type_b = space_b.lighting_space_type`  

          - If lighting space types is employee lunch and break rooms, conference/meeting rooms, or classrooms (not including shop classrooms, laboratory classrooms, and preschool through 12th-grade classrooms), set occupancy sensor flag: `if lighting_space_type_b in ["LOUNGE/BREAKROOM", "CONFERENCE/MEETING/MULTIPURPOSE ROOM", "CLASSROOM/LECTURE HALL/TRAINING ROOM - PENITENTIARY", "CLASSROOM/LECTURE HALL/TRAINING ROOM - ALL OTHER"]: occ_sensor_flag == TRUE`  

          **Rule Assertion:**  

          - Case 1: If space requires occupancy sensor and interior lighting is modeled with full-auto on occupancy sensor control, and interior lighting schedule matches P_RMR: `if ( occ_sensor_flag ) and ( control_type_b == "FULL-AUTO ON" ) and ( schedule_match_flag ): PASS`  

          - Case 2: If space requires occupancy sensor and interior lighting is modeled with full-auto on occupancy sensor control, and interior lighting schedule does not match P_RMR: `if ( occ_sensor_flag ) and ( control_type_b == "FULL-AUTO ON" ) and ( NOT schedule_match_flag ): CAUTION`  

          - Case 3: If space requires occupancy sensor and interior lighting is not modeled with full-auto on occupancy sensor control, and interior lighting schedule matches P_RMR: `if ( occ_sensor_flag ) and ( control_type_b != "FULL-AUTO ON" ) and ( schedule_match_flag ): CAUTION`  

          - Case 4: If space requires occupancy sensor and interior lighting is not modeled with full-auto on occupancy sensor control, and interior lighting schedule does not match P_RMR: `if ( occ_sensor_flag ) and ( control_type_b != "FULL-AUTO ON" ) and ( NOT schedule_match_flag ): FAIL`  

          - Case 5: If space does not require occupancy sensor and interior lighting is modeled with full-auto on occupancy sensor control, and interior lighting schedule matches P_RMR: `if ( NOT occ_sensor_flag ) and ( control_type_b == "FULL-AUTO ON" ) and ( schedule_match_flag ): FAIL`  

          - Case 6: If space does not require occupancy sensor and interior lighting is modeled with full-auto on occupancy sensor control, and interior lighting schedule does not match P_RMR: `if ( NOT occ_sensor_flag ) and ( control_type_b == "FULL-AUTO ON" ) and ( NOT schedule_match_flag ): CAUTION`  

          - Case 7: If space does not require occupancy sensor and interior lighting is not modeled with full-auto on occupancy sensor control, and interior lighting schedule matches P_RMR: `if ( NOT occ_sensor_flag ) and ( control_type_b != "FULL-AUTO ON" ) and ( schedule_match_flag ): CAUTION`  

          - Case 8: If space does not require occupancy sensor and interior lighting is not modeled with full-auto on occupancy sensor control, and interior lighting schedule does not match P_RMR: `if ( NOT occ_sensor_flag ) and ( control_type_b != "FULL-AUTO ON" ) and ( NOT schedule_match_flag ): CAUTION`  

**Rule Assertion Table:**  
| Input                     |Case 1 |Case 2   |Case 3   |Case 4   |Case 5   |Case 6   |Case 7   |Case 8   |
| :-                        |:-:    |:-:      |:-:      |:-:      |:-:      |:-:      |:-:      |:-:      |
| occ control required      |true   |true     |true     |true     |false    |false    |false    |false    |
| "FULL-AUTO ON" modeled    |true   |true     |false    |false    |true     |true     |false    |false    |
| schedule matches P_RMR    |true   |false    |true     |false    |true     |false    |true     |false    |
| ASSERTION                 |PASS   |CAUTION  |CAUTION  |FAIL     |FAIL     |CAUTION  |CAUTION  |CAUTION  |

