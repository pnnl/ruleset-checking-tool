
# Receptacle - Rule 12-1

**Rule ID:** 12-1  
**Rule Description:** Number of spaces modeled in User RMR and Baseline RMR are the same  
**Rule Assertion:** Baseline RMR = User RMR  
**Appendix G Section:** Section Table G3.1-12 Modeling Requirements for the Proposed design  
**Appendix G Section Reference:** None  

**Applicability:** All required data elements exist for B_RMR and U_RMR  
**Applicability Checks:** None  
**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  

## Rule Logic:  

- Get the total number of spaces in the building segment in the User model: ```for building_segment_user in U_RMR.building.building_segments:```  

  - For each thermal_block in building segment: ```thermal_block_user in building_segment_user.thermal_blocks:```

  - For each zone in thermal block: ```zone_user in thermal_block_user.zones:```

  - For each space in zone, add to the total number of spaces in the User model: ```for space_user in zone_user.spaces: num_of_spaces_user += 1```  

- Get the total number of spaces in the building segment in the Baseline model: ```for building_segment_baseline in B_RMR.building.building_segments:```  

  - For each thermal_block in building segment: ```thermal_block_baseline in building_segment.thermal_blocks:```

  - For each zone in thermal block: ```zone_baseline in thermal_block_baseline.zones:```

  - For each space in zone, add to the total number of spaces in the Baseline model: ```for space_baseline in zone_baseline.spaces: num_of_spaces_baseline += 1```  

**Rule Assertion:** ```num_of_spaces_user == num_of_spaces_baseline```  

**[Back](../_toc.md)**
