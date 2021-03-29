
# Lighting - Rule 6-mno

**Rule ID:** 6-mno  
**Rule Description:** ILP for the proposed building is determined as designed/as exisiting or determined using BAM for lighting system not designed and not exisiting. And the ILP for the baseline building is determined using values in Table G3.7 (Note XC, is this only applied if the building goes for space-by-space method?)  
**Appendix G Section:** Lighting  
**Appendix G Section Reference:**  

- Table G3.7, Performance Rating Method Lighting Power Density Allowances and Occupancy Sensor Reductions Using the Space-by-Space Method  

**Applicability:** All required data elements exist for P_RMR and B_RMR  
**Applicability Checks:** None  
**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** Table G3.7  
## Rule Logic: 

- Get the lighting status in each space in the building segment in the Proposed model: ```For building_segment in P_RMR.building.building_segments:```  

  - Get thermal_block from building segment: ```thermal_block in building_segment.thermal_blocks:```

  - Get thermal_zone from thermal block: ```thermal_zone in thermal_block.thermal_zones:```

  - Get space from thermal zone: ```space in thermal_zone.spaces:```  

    - Get the lighting status for the space: ```lighting_status = space.lighting_status_type``` (Note XC, assuming there is a lighting status type in the space, indicating, existing, designed or not designed)  

    - Determine the ILP for the space:  

      - Case 1: lighting_status is "Existing", ILP cannot be verified, raise caution: ```if lighting_status == "Existing", CAUTION```
      - Case 2: lighting_status is "Designed", ILP cannot be verified, raise caution: ```if lighting_status == "Designed", CAUTION```
      - Case 3: lighting_status is "Not Designed", ILP should be based on Table 9.5.1, get space type: ```if lighting_status == "Not Designed", lighting_space_type = space.lighting_space_type``` (Note XC, no lighitng_space_type in the schema right now.)

        - Determine the allowable lighting power density for the space type as per Table 3.7: ```allowable_baseline_LPD = data_lookup(table_G3_7, lighting_space_type)```

- For each interior lighting in the Proposed model: ```For interior_lighting in P_RMR.building.interior_lightings:```
  - Get purpose_type from interior lighting: ```purpose_type =  interior_lighting.purpose_type:```  

- Get the building segment in the Baseline model: ```For building_segment in B_RMR.building.building_segments:```  

  - Get thermal_block from building segment: ```thermal_block in building_segment.thermal_blocks:```  

  - Get thermal_zone from thermal block: ```thermal_zone in thermal_block.thermal_zones:```  

  - Get space from thermal zone: ```space in thermal_zone.spaces:```  

    - Get the area of the space: ```floor_area_baseline = space.floor_area```  

    - Get the space type of the space: ```lighting_space_type = space.lighting_space_type``` (Note XC, no lighitng_space_type in the schema right now.)  

    - Determine the allowable lighting power density for the space type as per Table 3.7: ```allowable_baseline_LPD = data_lookup(table_G3_7, lighting_space_type)```  

    - Get the total lighting power modeled in the space: ```space_lighting_power_baseline = space.lighting_power``` (Note XC, does the RMR report total wattage or LPD, or fixtures in the space?)  

**Rule Assertion:** For each space in B_RMR: ```space_lighting_power_baseline == floor_area_baseline * allowable_baseline_LPD```  
