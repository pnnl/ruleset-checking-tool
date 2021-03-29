
# Lighting - Rule 6-z

**Rule ID:** 6-z  
**Rule Description:** Other automatic lighting controls included in the proposed design shall be modeled directly in the building simulation by reducing the lighting schedule each hour by the occupancy sensor reduction factors in Table G3.7 for the applicable space type. This reduction shall be taken only for lighting controlled by the occupancy sensors.  In the baseline no additional automatic lighting controls for daylight utilization shall be modeled.  
**Rule Assertion:** Proposed RMR = expected value
**Appendix G Section:** Lighting  
**Appendix G Section Reference:**  

- Table G3.7, Performance Rating Method Lighting Power Density Allowances and Occupancy Sensor Reductions Using the Space-by-Space Method  

**Applicability:** All required data elements exist for P_RMR and B_RMR  
**Applicability Checks:** None  
**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** Table G3.7  

## Rule Logic:  

- For each interior lighting in the Proposed model: ```For interior_lighting in P_RMR.building.interior_lightings:```  

  - Get purpose_type from interior lighting: ```purpose_type =  interior_lighting.purpose_type:```  

  - Determine the allowable occupancy sensor reduction as per Table G3.7: ```occ_sensor_reduction = data_lookup(table_G3_7, purpose_type)```

  - Get occupancy sensor type from interior lighting: ```occ_sensor_type =  interior_lighting.occupancy_sensor_type:```(Note XC, assuming occupancy sensor type is None, Manual-on, Partial-auto-on, Individual Workstation and Other)  

    - Determine the allowable occupancy sensor reduction as per sensor type:  

      - Case 1: occupancy sensor type is None, occupancy sensor reduction credit is 0: ```if occ_sensor_type == "None", occ_sensor_reduction = 0```
      - Case 2: occupancy sensor type is "Manual-on" or "Partial-auto-on", occupancy sensor reduction credit is 1.25 times Table G3.7 value: ```elsif occ_sensor_type == "Manual-on" or occ_sensor_type == "Partial-auto-on", occ_sensor_reduciton = occ_sensor_reduction * 1.25```
      - Case 3: occupancy sensor type is "Other", occupancy sensor reduction credit is as per Table G3.7: ```elsif occ_sensor_type == "Other", occ_sensor_reduction = occ_sensor_reduction```
      - Case 4: occupancy sensor type is "Individual Workstation", occupancy sensor reduction credit for open plan offices is 30%: ```elsif occ_sensor_type == "Other" and purpose_type == "Office, Open Plan", occ_sensor_reduction = 30%```

  - Get the lighting schedule for the interior lighting object: ```lighting_schedule = interior_lighting.lighting_schedule_name```  

    - Get the EFLH value for the lighting schedule: ```schedule_EFLH_proposed = EFLH(lighting_schedule)```

- For each interior lighting in the Baseline model: ```For interior_lighting in B_RMR.building.interior_lightings:```

  - Get the lighting schedule for the interior lighting object: ```lighting_schedule = interior_lighting.lighting_schedule_name```  

    - Get the EFLH value for the lighting schedule: ```schedule_EFLH_baseline = EFLH(lighting_schedule)```

**Rule Assertion:** For each interior_lighting in P_RMR: ```schedule_EFLH_proposed == schedule_EFLH_baseline * (1 - occ_sensor_reduction)```  

- Case 1, Proposed model interior lighting schedule EFLH is equal to Baseline model: ```schedule_EFLH_proposed == schedule_EFLH_baseline: PASS```  

- Case 2, Proposed model interior lighting schedule EFLH is not equal to Baseline model: ```schedule_EFLH_proposed == schedule_EFLH_baseline: CAUTION```
