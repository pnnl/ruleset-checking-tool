
# Receptacle - Rule 12-1

**Rule ID:** 12-1  
**Rule Description:** Number of spaces modeled in User RMR and Baseline RMR are the same  
**Rule Assertion:** Baseline RMR = User RMR  
**Appendix G Section:** Receptacle  
**Appendix G Section Reference:** None  

**Applicability:** All required data elements exist for B_RMR and U_RMR  
**Applicability Checks:** None  
**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  

## Rule Logic:  

- Get the total number of spaces in the building segment in the User model: ```For building_segment in U_RMR.building.building_segments:```  

  - Get thermal_block from building segment: ```thermal_block in building_segment.thermal_blocks:```

  - Get thermal_zone from thermal block: ```thermal_zone in thermal_block.zones:```

  - Get space from thermal zone: ```space in thermal_zone.spaces:```  

    - Add to the total number of spaces in the User model: ```num_of_spaces_user += 1```

- Get the total number of spaces in the building segment in the Baseline model: ```For building_segment in B_RMR.building.building_segments:```  

  - Get thermal_block from building segment: ```thermal_block in building_segment.thermal_blocks:```

  - Get thermal_zone from thermal block: ```thermal_zone in thermal_block.zones:```

  - Get space from thermal zone: ```space in thermal_zone.spaces:```  

    - Add to the total number of spaces in the Baseline model: ```num_of_spaces_baseline += 1```

**Rule Assertion:** ```num_of_spaces_user == num_of_spaces_baseline```  
