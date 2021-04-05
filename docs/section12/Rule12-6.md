
# Lighting - Rule 12-6

**Rule ID:** 12-6  
**Rule Description:** User RMR Receptacle Schedule in Proposed RMR?  
**Rule Assertion:** Proposed RMR = User RMR  
**Appendix G Section:** Receptacle  
**Appendix G Section Reference:** None  

**Applicability:** All required data elements exist for P_RMR and U_RMR  
**Applicability Checks:**  

  1. Rule 12-3 = True  

**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  

## Rule Logic:  

- **Applicability Check 1:** ```if (rule-12-3.status == True):```
- Get the receptacle load of each space in the building segment in the User model: ```For building_segment in U_RMR.building.building_segments:```  
  - Get thermal_block from building segment: ```thermal_block in building_segment.thermal_blocks:```
  - Get thermal_zone from thermal block: ```thermal_zone in thermal_block.thermal_zones:```
  - Get space from thermal zone: ```space in thermal_zone.spaces:```  
    - Get the name of the space: ```space_name = space.name```
    - Get the receptacle load in the space: ```space_receptacle = space.equipment_internal_gains```
      - Get the receptacle load schedule: ```receptacle_sch = space_receptacle.schedule_name```
      - Save the receptacle load schedule for all spaces in the User model: ```space_receptacle_schedules_user[space_name] = receptacle_sch```

- Get the receptacle load of each space in the building segment in the Proposed model: ```For building_segment in P_RMR.building.building_segments:```  
  - Get thermal_block from building segment: ```thermal_block in building_segment.thermal_blocks:```
  - Get thermal_zone from thermal block: ```thermal_zone in thermal_block.thermal_zones:```
  - Get space from thermal zone: ```space in thermal_zone.spaces:```  
    - Get the name of the space: ```space_name = space.name```
    - Get the receptacle load in the space: ```space_receptacle = space.equipment_internal_gains```
      - Get the receptacle load schedule: ```receptacle_sch = space_receptacle.schedule_name```
      - Save the receptacle load schedule for all spaces in the Proposed model: ```space_receptacle_schedules_proposed[space_name] = receptacle_sch```

**Rule Assertion:** ```space_receptacle_schedules_user == space_receptacle_schedules_proposed```  
