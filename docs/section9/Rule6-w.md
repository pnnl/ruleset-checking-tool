
# Lighting - Rule 6-12

**Rule ID:** 6-12  
**Rule Description:** Proposed building is modeled with dayligthing controls  
**Appendix G Section:** Section G3.1-6(h) Lighting: Modeling Requirements for the Proposed design  
**Appendix G Section Reference:**  

**Applicability:** All required data elements exist for P_RMR  
**Applicability Checks:** None  
**Manual Check:** Yes  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  
## Rule Logic: 

- Check if each space has window or skylight in the building segment in the Proposed model: ```For building_segment_p in P_RMR.building.building_segments:```  

  - For each thermal_block in building segment: ```thermal_block_p in building_segment_p.thermal_blocks:```  

  - For each zone in thermal block: ```zone_p in thermal_block_p.zones:```  

    - Get surfaces in zone: ```surface_p in zone_p.surfaces```  

      - Check if the surface is exterior and has openings: ```if ( surface_p.adjacent_to == AMBIENT ) AND ( COUNT( surface_p.fenestration_subsurfaces ) >= 1 ): daylight_flag_p == TRUE```  

    -  For each space in zone: ```space_p in zone_p.spaces:```  
      - Get interior_lighting in space: ```interior_lighting_p = space_p.interior_lighting```  

        - Check if any interior_lighting has daylight control: ```if ( lighting.has_daylight_control  == TRUE for lighting in interior_lighting_p ): has_daylight_control_flag == TRUE```  

        **Rule Assertion:** For each zone in the Proposed model:  

        - Case 1, the zone has window or skylight and daylight control is modeled: ```daylight_control_flag == TRUE AND has_daylight_control_flag == TRUE: PASS```  

        - Case 2, the zone has window or skylight and daylight control is not modeled:  ```daylight_control_flag == TRUE AND has_daylight_control_flag == FALSE: CAUTION```  

        - Case 3, the zonee does not have window or skylight and daylight control is modeled: ```daylight_control_flag == FALSE AND has_daylight_control_flag == TRUE: FAIL```  
