
# Receptacle - Rule 12-8

**Rule ID:** 12-8  
**Rule Description:** Receptacle control credit modeled correctly in User RMR and Baseline RMR are the same  
**Rule Assertion:** User RMR = expected value, Baseline RMR = User RMR  
**Appendix G Section:** Receptacle  
**Appendix G Section Reference:** None  

**Applicability:** All required data elements exist for B_RMR and U_RMR  
**Applicability Checks:**  

  1. Rule 12-4 = True  

**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  

## Rule Logic:  

- **Applicability Check 1:** ```if (rule-12-4.status == True):```
- Get the receptacle load of each space in the building segment in the User model: ```For building_segment in U_RMR.building.building_segments:```  
  - Get thermal_block from building segment: ```thermal_block in building_segment.thermal_blocks:```
  - Get thermal_zone from thermal block: ```thermal_zone in thermal_block.zones:```
  - Get space from thermal zone: ```space in thermal_zone.spaces:```  
    - Get the name of the space: ```space_name = space.name```
    - Get the receptacle load in the space: ```space_receptacle = space.equipment_internal_gains```
      - Get the receptacle load control credit: ```receptacle_control = space_receptacle.receptacle_control_credit```
      - Save the receptacle load schedule for all spaces in the User model: ```space_receptacle_schedules_user[space_name] = ELFH(receptacle_sch) / ( 1 - receptacle_control )```

- Get the receptacle load of each space in the building segment in the Baseline model: ```For building_segment in B_RMR.building.building_segments:```  
  - Get thermal_block from building segment: ```thermal_block in building_segment.thermal_blocks:```
  - Get thermal_zone from thermal block: ```thermal_zone in thermal_block.zones:```
  - Get space from thermal zone: ```space in thermal_zone.spaces:```  
    - Get the name of the space: ```space_name = space.name```
    - Get the receptacle load in the space: ```space_receptacle = space.equipment_internal_gains```
      - Get the receptacle load schedule: ```receptacle_sch = space_receptacle.schedule_name```
      - Save the receptacle load schedule for all spaces in the Baseline model: ```space_receptacle_schedules_baseline[space_name] = ELFH(receptacle_sch)```

**Rule Assertion:** ```space_receptacle_schedules_user == space_receptacle_schedules_baseline```  
