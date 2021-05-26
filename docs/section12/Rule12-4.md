
# Receptacle - Rule 12-4

**Rule ID:** 12-4  
**Rule Description:** User RMR Space Name in Baseline RMR?  
**Rule Assertion:** Baseline RMR = User RMR  
**Appendix G Section:** Section Table G3.1-12 Modeling Requirements for the Proposed design  
**Appendix G Section Reference:** None  

**Applicability:** All required data elements exist for B_RMR and U_RMR  
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

- Get the name of each space in the building segment in the Baseline model: ```for building_segment_baseline in B_RMR.building.building_segments:```  
  - For each thermal_block in building segment: ```thermal_block_baseline in building_segment_baseline.thermal_blocks:```
  - For each zone in thermal block: ```zone_baseline in thermal_block_baseline.zones:```
  - For each space in zone: ```space_baseline in zone_baseline.spaces:```  
    - Get the name of the space: ```space_name_baseline = space_baseline.name```
    - Add to the list of space names in the Baseline model: ```space_names_baseline_list.append(space_name_baseline)```  

**Rule Assertion:** ```sorted(space_names_user) == sorted(space_names_baseline)```  
