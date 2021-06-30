
# Lighting - Rule 6-13

**Rule ID:** 6-13  
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

## Rule Logic:  

- For each building_segment in the Proposed model: ```for building_segment_p in P_RMR.building.building_segments:```  

  - For each thermal_block in building segment: ```thermal_block_p in building_segment_p.thermal_blocks:```  

    - For each zone in thermal block: ```zone_p in thermal_block_p.zones:```  

      - For each space in zone: ```space_p in zone_p.spaces:```  

        - Get lighting space type: ```lighting_space_type_p = space_p.lighting_space_type```  

        - Get lighting in space: ```lighting_p = space_p.interior_lighting```  

        - Get lighting schedule: ```schedule_p = match_data_element(P_RMR, schedules, lighting_p.lighting_multiplier_schedule_name)```  (Note XC, this would require match_data_element to use name instead of id)

        - Get lighting schedule equivalent full load hours: ```schedule_EFLH_p = EFLH(schedule_p.hourly_values)```  

        - Get matching space from B_RMR: ```space_b = match_data_element(B_RMR, spaces, space_p.id)```  

          - Get lighting in space: ```lighting_b = space_b.interior_lighting```  

          - Get lighting schedule: ```schedule_b = match_data_element(B_RMR, schedules, lighting_b.lighting_multiplier_schedule_name)```  

          - Get lighting schedule equivalent full load hours: ```schedule_EFLH_b = EFLH(schedule_b.hourly_values)```  

**Rule Assertion:**  

- Case 1, Proposed model interior lighting schedule EFLH is equal to Baseline model: ```schedule_EFLH_p == schedule_EFLH_b: PASS```  

- Case 2, Proposed model interior lighting schedule EFLH is not equal to Baseline model, raise warning and return lighting space type, lighting schedule EFLHs for manual check: ```schedule_EFLH_p != schedule_EFLH_b: CAUTION, return lighting_space_type_p, schedule_EFLH_p, schedule_EFLH_b```  
