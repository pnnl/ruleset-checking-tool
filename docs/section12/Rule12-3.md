
# Receptacle - Rule 12-3

**Rule ID:** 12-3  
**Rule Description:** User RMR Space Name in Proposed RMR?  
**Rule Assertion:** Proposed RMR = User RMR  
**Appendix G Section:** Receptacle  
**Appendix G Section Reference:** None  

**Applicability:** All required data elements exist for P_RMR and U_RMR  
**Applicability Checks:**  

  1. User RMR Space Count > 0  

**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  

## Rule Logic:  

- **Applicability Check 1:** ```length( for _space in U_RMR ) > 0:```
- Get the name of each space in the building segment in the User model: ```For building_segment in U_RMR.building.building_segments:```  
  - Get thermal_block from building segment: ```thermal_block in building_segment.thermal_blocks:```
  - Get thermal_zone from thermal block: ```thermal_zone in thermal_block.zones:```
  - Get space from thermal zone: ```space in thermal_zone.spaces:```  
    - Get the name of the space: ```space_name = space.name```
    - Add to the list of space names in the User model: ```space_names_user.append(space_name)```

- Get the name of each space in the building segment in the Proposed model: ```For building_segment in P_RMR.building.building_segments:```  
  - Get thermal_block from building segment: ```thermal_block in building_segment.thermal_blocks:```
  - Get thermal_zone from thermal block: ```thermal_zone in thermal_block.zones:```
  - Get space from thermal zone: ```space in thermal_zone.spaces:```  
    - Get the name of the space: ```space_name = space.name```
    - Add to the list of space names in the Proposed model: ```space_names_proposed.append(space_name)```

**Rule Assertion:** ```space_names_user == space_names_proposed```  
