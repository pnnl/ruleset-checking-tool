
# Lighting - Rule 6-6

**Rule ID:** 6-6  
**Rule Description:** Where lighting neither exists nor is submitted with design documents, lighting shall comply with but not exceed the requirements of Section 9. Lighting power shall be determined in accordance with the Building Area Method (Section 9.5.1)  
**Appendix G Section:** Section G3.1-6(c) Modeling Requirements for the Proposed design  
**Appendix G Section Reference:**  

- Table 9.5.1, Lighting Power Density Allowance Using the Building Area Method  

**Applicability:** All required data elements exist for P_RMR  
**Applicability Checks:** None  
**Manual Check:**  

1. Where a complete lighting system neither exists nor is submitted with design documents, the RCT cannot verify if lighting system is existing, designed or not designed. Manual review is required.  

**Evaluation Context:** Each Data Element  
**Data Lookup:** Table 9.5.1  
## Rule Logic: 

- **Manual Check 1:** Manual review is required where a complete lighting system neither exists nor is submitted with design documents.  

- For each building_segment in the Proposed Model: ```building_segment_p in P_RMR.building.building_segments```  

  - Get lighting power allowance: ```lighting_allowance_p = data_lookup(table_9_5_1, building_segment_p.lighting_building_area_type)```  

  - For each thermal_block in building segment: ```thermal_block_p in building_segment_p.thermal_blocks:```  

    - For each zone in thermal block: ```zone_p in thermal_block_p.zones:```  

      - For each space in thermal zone: ```space_p in zone_p.spaces:```  

        - Get interior lighting in space: ```interior_lighting_p = space_p.interior_lighting```  

        - Get interior lighting in U_RMR: ```interior_lighting_u = match_data_element(U_RMR, InteriorLightings, space_p.interior_lighting.id)```  
          **Rule Assertion:** 

          - Case 1: If lighting building area type is not specified: ```if NOT building_segment_p.lighting_building_area_type: FAIL```  

          - Case 2: If lighting power does not equal to the value prescribed in Table 9.5.1 or lighting power in P_RMR is not the same as U_RMR: ```if ( ( interior_lighting_p.power_per_area != lighting_allowance_p ) OR ( interior_lighting_p != interior_lighting_u ) ): FAIL```  
