
# Receptacle - Rule 12-2

**Rule ID:** 12-2  
**Rule Description:** Number of spaces modeled in User RMR and Proposed RMR are the same  
**Rule Assertion:** Proposed RMR = User RMR  
**Appendix G Section:** Section Table G3.1-12 Modeling Requirements for the Proposed design  
**Appendix G Section Reference:** None  

**Applicability:** All required data elements exist for P_RMR and U_RMR  
**Applicability Checks:** None  
**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  

## Rule Logic:  

- Get the total number of spaces in the building segment in the User model: ```for building_segment_user in U_RMR.building.building_segments:```  

  - For each thermal_block in building segment: ```thermal_block in building_segment.thermal_blocks:```

  - For each zone in thermal block: ```zone_user in thermal_block_user.zones:```

  - For each space in zone, add to the total number of spaces in the User model: ```for space_user in thermal_zone_user.spaces: num_of_spaces_user += 1```  

- Get the total number of spaces in the building segment in the Proposed model: ```for building_segment_proposed in P_RMR.building.building_segments:```  

  - For each thermal_block in building segment: ```thermal_block_proposed in building_segment_proposed.thermal_blocks:```

  - For each zone in thermal block: ```zone_proposed in thermal_block_proposed.zones:```

  - For each space in zone, add to the total number of spaces in the Proposed model: ```for space_proposed in zone_proposed.spaces: num_of_spaces_proposed += 1```  

**Rule Assertion:** ```num_of_spaces_user == num_of_spaces_proposed```  

**[Back](../_toc.md)**
