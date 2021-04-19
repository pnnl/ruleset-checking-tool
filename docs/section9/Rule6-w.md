
# Lighting - Rule 6-w

**Rule ID:** 6-w  
**Rule Description:** Proposed building is modeled with dayligthing controls and no daylighting control is modeled for baseline  
**Appendix G Section:** Section G3.1-6(h) Modeling Requirements for the Proposed design  
**Appendix G Section Reference:**  

**Applicability:** All required data elements exist for P_RMR and B_RMR  
**Applicability Checks:** None  
**Manual Check:** Yes  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  
## Rule Logic: 

- Check if each space has window or skylight in the building segment in the Proposed model: ```For building_segment_proposed in P_RMR.building.building_segments:```  

  - For each thermal_block in building segment: ```thermal_block_proposed in building_segment_proposed.thermal_blocks:```

  - For each zone in thermal block: ```zone_proposed in thermal_block_proposed.zones:```

  - For each space in zone: ```space_proposed in zone_proposed.spaces:```  

    - Get surfaces in space: ```surface_proposed in space_proposed.surfaces```  

      - Check if the surface is exterior and has openings: ```if ( surface_proposed.adjacent_to == AMBIENT ) AND ( COUNT( surface_proposed.fenestration_subsurfaces ) >= 1 ): daylight_flag_proposed == TRUE```  

    - Get interior_lighting in space: ```interior_lighting_proposed = space_proposed.interior_lightings```  

      - Check if any interior_lighting has daylight control: ```if ( lighting.has_daylighting_control  == TRUE for lighting in interior_lighting_proposed ): has_daylight_control_flag == TRUE```(Note XC, assuming if any of the lights in the space has daylight control, has_daylight_control_flag is true; not differentiating wattage in primary daylight/secondary daylight/top daylight area)  

    **Rule Assertion:** For each space in the Proposed model:  

    - Case 1, the space has window or skylight and daylight control is modeled: ```daylight_control_flag == TRUE AND has_daylight_control_flag == TRUE: PASS```  

    - Case 2, the space has window or skylight and daylight control is not modeled:  ```daylight_control_flag == TRUE AND has_daylight_control_flag == FALSE: CAUTION```

    - Case 3, the space does not have window or skylight and daylight control is modeled: ```daylight_control_flag == FALSE AND has_daylight_control_flag == TRUE: FAIL```

- Check if any space has daylight control in the Baseline model: ```For building_segment_baseline in B_RMR.building.building_segments:```  

  - For each thermal_block in building segment: ```thermal_block_baseline in building_segment_baseline.thermal_blocks:```

  - For each zone in thermal block: ```zone_baseline in thermal_block_baseline.zones:```

  - For each space in zone: ```space_baseline in zone_baseline.spaces:```  

    - Get interior_lighting in space: ```interior_lighting_baseline = space_baseline.interior_lightings```  

      **Rule Assertion:** For each interior_lighting in the Baseline model: ```interior_lighting_baseline.has_daylighting_control == FALSE```  
