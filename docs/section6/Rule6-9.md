
# Lighting - Rule 6-9

**Rule ID:** 6-9  
**Rule Description:** Baseline building is modeled with automatic shutoff controls in buildings >5000 sq.ft.  
**Appendix G Section:** Section G3.1-6 Modeling Requirements for the Baseline building  
**Appendix G Section Reference:**  None  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  

  1. Building total area is more than 5,000sq.ft.  

**Manual Check:** Yes  

**Function Call:**  

  - compare_schedules()
  - normalize_space_lighting_schedule()

**Evaluation Context:** Each Data Element  
**Data Lookup:** None  

## Rule Logic: 

- For each building_segment in the Baseline model: `for building_segment_b in B_RMR.building.building_segments:`  

  - For each thermal_block in building segment: `for thermal_block_b in building_segment.thermal_blocks:`  

    - For each zone in thermal block: `for zone_b in thermal_block_b.zones:`  

      - For each space in zone: `for space_b in zone.spaces:`  

        - Add space floor area to building total floor area: `building_total_area_b += space_b.floor_area`  

- **Applicability Check 1:**`if building_total_area_b > 5000:`  

- Get building open schedule in the baseline model: `building_open_schedule_b = B_RMR.building.building_open_schedule`  

- For each building segment in building: `building_segment_b in B_RMR.building.building_segments:`  

  - For each thermal block in building segment: `thermal_block_b in building_segment_b.thermal_blocks:`  

    - For each zone in thermal block: `zone_b in thermal_block_b.zones:`  

      - For each space in zone: `space_b in zone_b.spaces:`  

        - Get normalized space lighting schedule: `normalized_schedule_b = normalize_space_lighting_schedule(space_b)`  

        - Get matching space in P_RMR: `space_p = match_data_element(P_RMR, Spaces, space_b.id)`  

          - Get normalized space lighting schedule in P_RMR: `normalized_schedule_p = normalize_space_lighting_schedule(space_p)`

        - Check if automatic shutoff control is modeled in space during unoccupied hours (i.e. if lighting schedule hourly value in B_RMR is equal to P_RMR during unoccupied hours): `schedule_comparison_result = compare_schedules(normalized_schedule_b, normalized_schedule_p, building_open_schedule_b, none)`  

          **Rule Assertion:**

          - Case 1: For unoccupied hours, if lighting schedule hourly value in B_RMR is equal to P_RMR: `if schedule_comparison_result == "MATCH": PASS`  

          - Case 2: Else: `else: CAUTION and return schedule_comparison_result`  


**Temporary Function note:**

`compare_schedule_result = compare_schedules(Schedule 1, Schedule 2, Mask Schedule, reduction_factor)`

(4 inputs, Schedule 1, Schedule 2, Mask Schedule, comparison factor)

- Schedule 2 as the comparison basis, i.e. Schedule 1 = Schedule 2 * comparison factor
- When Mask Schedule hourly value is 0, schedules need to be the same at that hour. If Mask Schedule hourly value is 1, Schedule 1 needs to be comparison factor times Schedule 2 at that hour. If Mask Schedule hourly value is 2, skip comparison.
- can return "match", "equal and less", "equal and more", "equal, less and more", with bin data, TBD

