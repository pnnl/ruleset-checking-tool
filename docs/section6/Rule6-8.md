
# Lighting - Rule 6-8

**Rule ID:** 6-8  
**Rule Description:** Additional occupancy sensor controls in the proposed building are modeled through schedule adjustments based on factors defined in Table G3.7.  
**Rule Assertion:** Proposed RMD = expected value  
**Appendix G Section:** Section G3.1-6(i) Modeling Requirements for the Proposed design  
**Appendix G Section Reference:**  

- Table G3.7, Performance Rating Method Lighting Power Density Allowances and Occupancy Sensor Reductions Using the Space-by-Space Method  

**Applicability:** All required data elements exist for P_RMD  
**Applicability Checks:** None

**Manual Check:** Yes  
**Evaluation Context:** Each Data Element  
**Data Lookup:** Table G3.7  
**Function Call:**  

  - compare_schedules()
  - normalize_space_schedules()

## Rule Logic:  

- Get building open schedule in the proposed model: `building_open_schedule_p = P_RMD.building.building_open_schedule`
- For each building segment in building: `for building_segment_p in P_RMD.building.building_segments:`
    - For each zone in building_segments: `zone_p in building_segment_p.zones:`
      - For each space in zone: `space_p in zone_p.spaces:`
        - Get matching space from the baseline: `space_b = match_data_element(B_RMD, Spaces, space_p.id)`
        - Get normalized space lighting schedule for the baseline: `normalized_schedule_b = normalize_space_schedules(space_b.interior_lighting)`
        - Get normalized space lighting schedule: `normalized_schedule_p = normalize_space_schedules(space_p.interior_lighting)`
        - Compare lighting schedules in the proposed and baseline: `schedule_comparison_result = compare_schedules(normalized_schedule_p, normalized_schedule_b, building_open_schedule_p)`  

        **Rule Assertion:**
        - Case 1: If the lighting schedule in the proposed is equal to the lighting schedule in the baseline times the adjusted lighting occupancy sensor reduction factor for all hours, then pass: `if schedule_comparison_result == "MATCH": PASS`
        - Case 2: Else if, the lighting schedule in the proposed has fewer or equal equivalent full load hours than the lighting schedule in the baseline times the adjusted lighting occupancy sensor reduction factor, then undetermined: `if schedule_comparison_result == "EQUAL AND LESS": UNDETERMINED and raise_warning "Fail unless the model includes daylighting controls that are modeled using schedule adjustments or individual workstations with workstation lighting controlled by occupancy sensors (Table G3.7 footnote C)."`
        - Case 3: Else, the lighting schedule in the proposed has greater equivalent full load hours than the lighting schedule in the baseline times adjusted lighting occupancy sensor reduction factor, then fail: `if schedule_comparison_result == "MORE": FAIL and raise_message "The lighting schedule in the proposed model unexpectedly has greater equivalent full load hours than the baseline model, including the adjusted lighting occupancy sensor reduction factor."`  

**Notes:**
  1. Updated the Rule ID from 6-13 to 6-9 on 6/3/2022
  2. Updated the Rule ID from 6-9 to 6-8 on 6/8/2022

**[Back](../_toc.md)**
