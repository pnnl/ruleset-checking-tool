
# Lighting - Rule 6-mno

**Rule ID:** 6-mno  
**Rule Description:** Interior lighting power in the baseline building design shall be determined using the values in Table G3.7. (Note XC, is this only applied if the building goes for space-by-space method?)  
**Appendix G Section:** Lighting  
**Appendix G Section Reference:**  

- Table G3.7, Performance Rating Method Lighting Power Density Allowances and Occupancy Sensor Reductions Using the Space-by-Space Method  

**Applicability:** All required data elements exist for B_RMR  
**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** Table G3.7  
**Determining Expected Value:**  

- Get the building segment in the Baseline model: ```For building_segment in B_RMR.building.building_segments:```  

  - Get thermal_block from building segment: ```thermal_block in building_segment.thermal_blocks:```  

  - Get thermal_zone from thermal block: ```thermal_zone in thermal_block.thermal_zones:```  

  - Get space from thermal zone: ```space in thermal_zone.spaces:```  

    - Get the area of the space: ```floor_area_baseline = space.floor_area```  

    - Get the space type of the space: ```lighting_space_type = space.lighting_space_type``` (Note XC, no lighitng_space_type in the schema right now.)  

    - Determine the allowable lighting power density for the space type as per Table 3.7: ```allowable_baseline_LPD = data_lookup(table_G3_7, lighting_space_type)```  

    - Get the total lighting power modeled in the space: ```space_lighting_power_baseline = space.lighting_power``` (Note XC, does the RMR report total wattage or LPD, or fixtures in the space?)  

**Rule Assertion:** For each space in B_RMR: ```space_lighting_power_baseline == floor_area_baseline * allowable_baseline_LPD```  
