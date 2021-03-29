
# Lighting - Rule 6-aa

**Rule ID:** 6-aa  
**Rule Description:** Proposed building is modeled with other programmable lighting controls through a 10% schedule reduction.  
**Rule Assertion:** Proposed RMR = expected value
**Appendix G Section:** Lighting  
**Appendix G Section Reference:**  

- Table G3.7, Performance Rating Method Lighting Power Density Allowances and Occupancy Sensor Reductions Using the Space-by-Space Method  

**Applicability:** All required data elements exist for P_RMR and B_RMR  
**Applicability Checks:**  

  1. Building total area is less than 5,000sq.ft.  

**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  

## Rule Logic:  

- For each building_segment in the Proposed model: ```For building_segment in P_RMR.building.building_segments:```  
  - Get thermal_block from building segment: ```thermal_block in building_segment.thermal_blocks:```
  - Get thermal_zone from thermal block: ```thermal_zone in thermal_block.thermal_zones:```
  - Get space from thermal zone: ```space in thermal_zone.spaces:```
  - Get floor_area from space: ```space_floor_area = space.floor_area```
    - Get building total floor area: ```building_total_area_proposed = sum(space_floor_area)```

- **Applicability Check 1:**```if building_total_area_proposed < 5000```

  - Get purpose_type from interior lighting: ```purpose_type =  interior_lighting.purpose_type:```  

  - Determine the allowable occupancy sensor reduction as per Table G3.7: ```occ_sensor_reduction = data_lookup(table_G3_7, purpose_type)```

  - Get occupancy sensor type from interior lighting: ```occ_sensor_type =  interior_lighting.occupancy_sensor_type:```(Note XC, assuming occupancy sensor type is None, Manual-on, Partial-auto-on, Individual Workstation and Other)  

    - Determine the allowable occupancy sensor reduction as per sensor type:  

      - Case 1: occupancy sensor type is None, occupancy sensor reduction credit is 0: ```if occ_sensor_type == "None", occ_sensor_reduction = 0```
      - Case 2: occupancy sensor type is not None, occupancy sensor reduction credit is 10% as per Appendix G Table G3.1 6-i: ```else occ_sensor_type == 10%```

  - Get the lighting schedule for the interior lighting object: ```lighting_schedule = interior_lighting.lighting_schedule_name```  

    - Get the EFLH value for the lighting schedule: ```schedule_EFLH_proposed = EFLH(lighting_schedule)```

- For each interior lighting in the Baseline model: ```For interior_lighting in B_RMR.building.interior_lightings:```

  - Get the lighting schedule for the interior lighting object: ```lighting_schedule = interior_lighting.lighting_schedule_name```  

    - Get the EFLH value for the lighting schedule: ```schedule_EFLH_baseline = EFLH(lighting_schedule)```

**Rule Assertion:** For each interior_lighting in P_RMR: ```schedule_EFLH_proposed == schedule_EFLH_baseline * (1 - occ_sensor_reduction)```  

- Case 1, Proposed model interior lighting schedule EFLH is equal to Baseline model: ```schedule_EFLH_proposed == schedule_EFLH_baseline: PASS```  

- Case 2, Proposed model interior lighting schedule EFLH is not equal to Baseline model: ```schedule_EFLH_proposed == schedule_EFLH_baseline: CAUTION```
