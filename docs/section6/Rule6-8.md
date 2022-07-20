
# Lighting - Rule 6-8

**Rule ID:** 6-8  
**Rule Description:** Additional occupancy sensor controls in the proposed building are modeled through schedule adjustments based on factors defined in Table G3.7.  
**Rule Assertion:** Proposed RMR = expected value  
**Appendix G Section:** Section G3.1-6(i) Modeling Requirements for the Proposed design  
**Appendix G Section Reference:**  

- Table G3.7, Performance Rating Method Lighting Power Density Allowances and Occupancy Sensor Reductions Using the Space-by-Space Method  

**Applicability:** All required data elements exist for P_RMR  
**Applicability Checks:** None

**Manual Check:** Yes  
**Evaluation Context:** Each Data Element  
**Data Lookup:** Table G3.7  
**Function Call:**  

  - compare_schedules()
  - normalize_space_schedules()

## Rule Logic:  

- Get building open schedule in the proposed model: `building_open_schedule_p = P_RMR.building.building_open_schedule`  

- For each building segment in building: `for building_segment_p in P_RMR.building.building_segments:`  

    - For each zone in thermal block: `zone_p in building_segment_p.zones:` 

      - For each space in zone: `space_p in zone_p.spaces:`  

        - Get matching space from B_RMR: `space_b = match_data_element(B_RMR, Spaces, space_p.id)`  

          - Get normalized space lighting schedule for B_RMR: `normalized_schedule_b = normalize_space_schedules(space_b.interior_lighting)`  

        - Get normalized space lighting schedule: `normalized_schedule_p = normalize_space_schedules(space_p.interior_lighting)`

        - Compare lighting schedules in P_RMR and B_RMR: `schedule_comparison_result = compare_schedules(normalized_schedule_p, normalized_schedule_b, building_open_schedule_p)`  

          **Rule Assertion:**

          - Case 1: For all hours, for each lighting, if lighting schedule in P_RMR is equal to lighting schedule in B_RMR times adjusted lighting occupancy sensor reduction factor: `if schedule_comparison_result == "MATCH": PASS`  

          - Case 2: Else if lighting schedule in P_RMR is lower than or equal to lighting schedule in B_RMR times adjusted lighting occupancy sensor reduction factor: `if schedule_comparison_result == "EQUAL AND LESS": FAIL and raise_warning "SCHEDULE ADJUSTMENT MAY BE CORRECT IF SPACE INCLUDES DAYLIGHT CONTROL MODELED BY SCHEDULE ADJUSTMENT OR INDIVIDUAL WORKSTATIONS WITH LIGHTING CONTROLLED BY OCCUPANCY SENSORS (TABLE G3.7 FOOTNOTE C)."`  

          - Case 3: Else, lighting schedule in P_RMR is higher than lighting schedule in B_RMR times adjusted lighting occupancy sensor reduction factor: `if schedule_comparison_result == "EQUAL AND MORE": UNDETERMINED and raise_message "LIGHTING SCHEDULE IN P-RMR INCLUDING ADJUSTED LIGHTING OCCUPANCY SENSOR REDUCTION FACTOR IS HIGHER THAN THAT IN B-RMR. VERIFY ADDITIONAL OCCUPANCY SENSOR CONTROL IS MODELED CORRECTLY IN P-RMR."`  

**Notes:**
  1. Updated the Rule ID from 6-13 to 6-9 on 6/3/2022
  2. Updated the Rule ID from 6-9 to 6-8 on 6/8/2022

**Temporary Function note:**

`compare_schedule_result = compare_schedules(Schedule 1, Schedule 2, Mask Schedule, comparison factor)`

(4 inputs, Schedule 1, Schedule 2, Mask Schedule, comparison factor)

- Schedule 2 as the comparison basis, i.e. Schedule 1 = Schedule 2 * comparison factor
- When Mask Schedule hourly value is 0, schedules need to be the same at that hour. If Mask Schedule hourly value is 1, Schedule 1 needs to be comparison factor times Schedule 2 at that hour. If Mask Schedule hourly value is 2, skip comparison.
- can return "match", "equal and less", "equal and more", "equal, less and more", with bin data, TBD

**[Back](../_toc.md)**
