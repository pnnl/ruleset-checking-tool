
# Lighting - Rule 6-4

**Rule ID:** 6-4  
**Rule Description:** Where a complete lighting system exists, the actual lighting power for each thermal block shall be used in the model.  
**Appendix G Section:** Section G3.1-6(a) Modeling Requirements for the Proposed Design  
**Appendix G Section Reference:** None  

**Applicability:** All required data elements exist for P_RMR  
**Applicability Checks:** None  
**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  
## Rule Logic: 

- For each building_segment in the proposed model: ```building_segment_p in P_RMR.building.building_segments:```  

  - For each thermal_block in building segment: ```thermal_block_p in building_segment_p.thermal_blocks:```  

    - For each zone in thermal block: ```zone_p in thermal_block_p.zones:```  

      - For each space in zone: ```space_p in zone_p.spaces:```  

        - Get interior lighting in U_RMR: ```interior_lighting_b = match_data_element(U_RMR, InteriorLightings, space_p.interior_lighting.id)```

          **Rule Assertion:** 

          - Case 1: Lighting power in the proposed RMR is as existing and cannot be verified by RCT: ```if space_p.interior_lighting == interior_lighting_b: CAUTION```

          - Case 2: Lighting power in the proposed RMR does not match U_RMR: ```else: FAIL```
