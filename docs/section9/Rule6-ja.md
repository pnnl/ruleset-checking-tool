
# Lighting - Rule 6-ja

**Rule ID:** 6-ja  
**Rule Description:** The total building interior lighting power shall not exceed the interior lighting power allowance determined using either Table G3.7 or G3.8.  
**Appendix G Section:** Section G1.2.1(b) Mandatory Provisions related to interior lighting power
  
**Appendix G Section Reference:**  

- Table G3.7, Performance Rating Method Lighting Power Density Allowances and Occupancy Sensor Reductions Using the Space-by-Space Method
- Table G3.8, Performance Rating Method Lighting Power Densities Using the Building Area Method  

**Applicability:** All required data elements exist for P_RMR  
**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** Table G3.7 and Table G3.8  
## Rule Logic: 

- For each building_segment in the Proposed Model: ```building_segment_proposed in P_RMR.building.building_segments```  

- Get the lighting_building_area_type for the building_segment: ```lighting_building_area_type_proposed = building_segment_proposed.lighting_building_area_type```  

  - Determine if the building segment uses Building Area Method: ```if lighting_building_area_type_proposed is "None": bam_flag = FALSE else bam_flag = TRUE```  

- For each thermal_block in building_segment: ```thermal_block_proposed in lighting_building_area_type_proposed.thermal_blocks:```  

- For each thermal_zone in thermal_block: ```thermal_zone_proposed in thermal_block_proposed.zones:```  

- For each space in thermal zone: ```space_proposed in thermal_zone_proposed.spaces:```  

  - Get floor_area from space: ```floor_area_proposed = space_proposed.floor_area```  

  - If bam_flag is TRUE then add floor_area to the total building segment floor area: ```total_building_segment_area_proposed += floor_area_proposed```  

    - Get the allowable lighting power density for this building area type: ```if lighting_building_area_type_proposed in table_G3_8: allowable_LPD_proposed = data_lookup(table_G3_8, lighting_building_area_type_proposed) else raise_warning```  

    - Calculate the total allowable lighting wattage for the building segment: ```building_segment_allowable_lighting_wattage = allowable_LPD_proposed * total_building_segment_area_proposed```  

  - If bam_flag is FALSE, get lighting_space_type: ```lighting_space_type_proposed = space_proposed.lighting_space_type```  

    - If lighting_space_type_proposed exists in Table G3.7 then get the allowable lighting power density for this space type: ```if lighting_space_type_proposed in table_G3_7: allowable_LPD_proposed = data_lookup(table_G3_7, lighting_space_type_proposed) else raise_warning```  

    - Calculate the total allowable lighting wattage for the building segment: ```building_segment_allowable_lighting_wattage_proposed += allowable_LPD_proposed * floor_area_proposed```  

  - Get interior_lighting in space: ```interior_lighting_proposed = space_proposed.interior_lightings```  
  
    - Get the total design power_per_area for the space: ```space_lighting_power_per_area_proposed = sum( lighting.power_per_area for lighting in interior_lighting_proposed )```  

    - Calculate the total design lighting wattage for the space: ```space_lighting_wattage_proposed = space_lighting_power_per_area_proposed * floor_area_proposed```  

    - Calculate the total design lighting wattage for the building segment: ```building_segment_design_lighting_wattage_proposed += space_lighting_wattage_proposed```  

- Calculate the total allowable lighting wattage for the whole building: ```for building_segment_proposed in P_RMR.building.building_segments: building_allowable_lighting_wattage_proposed += building_segment_allowable_lighting_wattage_proposed```  

- Calculate the total design lighting power for for the whole buidling: ```for building_segment_proposed in P_RMR.building.building_segments: building_design_lighting_wattage_proposed += building_segment_design_lighting_wattage_proposed```  

**Rule Assertion:** For the Proposed model: ```building_design_lighting_wattage_proposed <= building_allowable_lighting_wattage_proposed```  
