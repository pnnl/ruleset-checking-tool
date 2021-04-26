
# Receptacle - Rule 12-3

**Rule ID:** 12-3  
**Rule Description:** User RMR Space Name in Proposed RMR?  
**Rule Assertion:** Proposed RMR = User RMR  
**Appendix G Section:** Section Table G3.1-12 Modeling Requirements for the Proposed design  
**Appendix G Section Reference:** None  

**Applicability:** All required data elements exist for P_RMR and U_RMR  
**Applicability Checks:**  

  1. User RMR Space Count > 0  

**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  

## Rule Logic:  

- **Applicability Check 1:** ```sum(length(zone.spaces in U_RMR)) > 0:```
- Get the name of each space in the building segment in the User model: ```for building_segment_user in U_RMR.building.building_segments:```  
  - For each thermal_block in building segment: ```thermal_block_user in building_segment_user.thermal_blocks:```
  - For each zone in thermal block: ```zone_user in thermal_block_user.zones:```
  - For each space in zone: ```space_user in zone_user.spaces:```  
    - Get the name of the space: ```space_name_user = space_user.name```
    - Add to the list of space names in the User model: ```space_names_user_list.append(space_name_user)```

- Get the name of each space in the building segment in the Proposed model: ```for building_segment_proposed in P_RMR.building.building_segments:```  
  - For each thermal_block in building segment: ```thermal_block_proposed in building_segment_proposed.thermal_blocks:```
  - For each zone in thermal block: ```zone_proposed in thermal_block_proposed.zones:```
  - For each space in thermal zone: ```space_proposed in zone_proposed.spaces:```  
    - Get the name of the space: ```space_name_proposed = space_proposed.name```
    - Add to the list of space names in the Proposed model: ```space_names_proposed_list.append(space_name_proposed)```

**Rule Assertion:** ```sorted(space_names_user_list) == sorted(space_names_proposed_list)```  
