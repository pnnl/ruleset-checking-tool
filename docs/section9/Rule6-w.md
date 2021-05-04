
# Lighting - Rule 6-w

**Rule ID:** 6-w  
**Rule Description:** Proposed building is modeled with dayligthing controls and no daylighting control is modeled for baseline  
**Appendix G Section:** Lighting  
**Appendix G Section Reference:** None  

**Applicability:** All required data elements exist for P_RMR and B_RMR  
**Applicability Checks:** None  
**Manual Check:** Yes  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  
## Rule Logic: 

- Check if each space has window or skylight in the building segment in the Proposed model: ```For building_segment in P_RMR.building.building_segments:```  

  - Get thermal_block from building segment: ```thermal_block in building_segment.thermal_blocks:```

  - Get thermal_zone from thermal block: ```thermal_zone in thermal_block.zones:```

  - Get space from thermal zone: ```space in thermal_zone.spaces:```  

  - Get surfaces in space: ```surface in space.surfaces```  

    - Check if the surface is exterior and has openings: ```if ( surface.adjacent_to in [AMBIENT] ) AND ( surface.fenestration_subsurfaces ): daylight_flag_proposed == 1```  

    **Rule Assertion:** For each space in the Proposed model:  

    - Case 1, the space has window or skylight and daylight control is modeled: ```daylight_control_flag == 1 AND space.has_daylight_control == 1: PASS```  

    - Case 2, the space has window or skylight and daylight control is not modeled:  ```daylight_control_flag == 1 AND space.has_daylight_control == 0: CAUTION```

    - Case 3, the space does not have window or skylight and daylight control is modeled: ```daylight_control_flag == 0 AND space.has_daylight_control == 1: FAIL```

- Check if any space has daylight control in the Baseline model: ```For building_segment in B_RMR.building.building_segments:```  

  - Get thermal_block from building segment: ```thermal_block in building_segment.thermal_blocks:```

  - Get thermal_zone from thermal block: ```thermal_zone in thermal_block.zones:```

  - Get space from thermal zone: ```space in thermal_zone.spaces:```

  **Rule Assertion:** For each space in the Baseline model: ```space.has_daylight_control == 0```  
