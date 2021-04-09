
# Lighting - Rule 12-4

**Rule ID:** 12-4  
**Rule Description:** User RMR Space Name in Baseline RMR?  
**Rule Assertion:** Baseline RMR = User RMR  
**Appendix G Section:** Receptacle  
**Appendix G Section Reference:** None  

**Applicability:** All required data elements exist for B_RMR and U_RMR  
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

- Get the name of each space in the building segment in the Baseline model: ```For building_segment in B_RMR.building.building_segments:```  
  - Get thermal_block from building segment: ```thermal_block in building_segment.thermal_blocks:```
  - Get thermal_zone from thermal block: ```thermal_zone in thermal_block.zones:```
  - Get space from thermal zone: ```space in thermal_zone.spaces:```  
    - Get the name of the space: ```space_name = space.name```
    - Add to the list of space names in the Baseline model: ```space_names_baseline.append(space_name)```

**Rule Assertion:** ```space_names_user == space_names_baseline```  
