
# Lighting - Rule 6-6

**Rule ID:** 6-6  
**Rule Description:** Where lighting neither exists nor is submitted with design documents, lighting shall comply with but not exceed the requirements of Section 9. Lighting power shall be determined in accordance with the Building Area Method (Section 9.5.1)  
**Appendix G Section:** Section G3.1-6(c) Modeling Requirements for the Proposed design  
**Appendix G Section Reference:**  

- Table G3.8, Lighting Power Density Allowance Using the Building Area Method  

**Applicability:** All required data elements exist for P_RMR  
**Applicability Checks:** None  
**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** Table G3.8
## Rule Logic: 

- For each building_segment in the Proposed Model: ```building_segment_p in P_RMR.building.building_segments```  

  - Determine if the building segment uses Building Area Method: ```if building_segment_p.lighting_building_area_type != "None":```  

    - Get lighting power allowance: ```lighting_allowance_p = data_lookup(table_G3_8, building_segment_p.lighting_building_area_type)```  

    - For each thermal_block in building segment: ```thermal_block_p in building_segment_p.thermal_blocks:```  

      - For each zone in thermal block: ```zone in thermal_block_p.zones:```  

        - For each space in thermal zone: ```space in zone_p.spaces:```  

          - Get interior lighting in space: ```interior_lighting_p = space.interior_lighting```  

            **Rule Assertion:** ```interior_lighting_p.power_per_area == lighting_allowance_p```  
