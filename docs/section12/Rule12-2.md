
# Lighting - Rule 12-2

**Rule ID:** 12-2  
**Rule Description:** Number of spaces modeled in User RMR and Proposed RMR are the same  
**Rule Assertion:** Proposed RMR = User RMR  
**Appendix G Section:** Receptacle  
**Appendix G Section Reference:** None  

**Applicability:** All required data elements exist for P_RMR and U_RMR  
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

- Get the total number of spaces in the building segment in the Proposed model: ```For building_segment in P_RMR.building.building_segments:```  

  - Get thermal_block from building segment: ```thermal_block in building_segment.thermal_blocks:```

  - Get thermal_zone from thermal block: ```thermal_zone in thermal_block.zones:```

  - Get space from thermal zone: ```space in thermal_zone.spaces:```  

    - Add to the total number of spaces in the Proposed model: ```num_of_spaces_proposed += 1```

**Rule Assertion:** ```num_of_spaces_user == num_of_spaces_proposed```  
