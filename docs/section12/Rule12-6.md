
# Receptacle - Rule 12-6

**Rule ID:** 12-6  
**Rule Description:** User RMR Receptacle Schedule in Proposed RMR?  
**Rule Assertion:** Proposed RMR = User RMR  
**Appendix G Section:** Section G3.1-12 Modeling Requirements for the Proposed design  
**Appendix G Section Reference:** None  

**Applicability:** All required data elements exist for P_RMR and U_RMR  
**Applicability Checks:**  

  1. Rule 12-3 = True  

**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  

## Rule Logic:  

- **Applicability Check 1:** ```if (rule-12-3.status == TRUE):```
- Get the receptacle load of each space in the building segment in the User model: ```for building_segment_user in U_RMR.building.building_segments:```  
  - For each thermal_block in building segment: ```thermal_block_user in building_segment_user.thermal_blocks:```
  - For each zone in thermal block: ```zone_user in thermal_block_user.zones:```
  - For each space in thermal zone: ```space_user in zone_user.spaces:```  
    - For each miscellaneous equipment in the space, get the equipment schedule: ```for space_equipment_user in space_user.miscellaneous_equipments: equipment_sch_user_dict[space_equipment_user] = space_equipment_user.schedule_name```
    - Get matching space from Proposed RMR: ```space_proposed = match_data_element(P_RMR, spaces, space_user.name)```
      - For each miscellaneous equipment in the space, get the equipment schedule: ```for space_equipment_proposed in space_proposed.miscellaneous_equipments: equipment_sch_proposed_dict[space_equipment_proposed] = space_equipment_proposed.schedule_name```
    **Rule Assertion:** ```equipment_sch_user_dict == equipment_sch_proposed_dict```  
