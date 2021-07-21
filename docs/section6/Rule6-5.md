
# Lighting - Rule 6-5

**Rule ID:** 6-5  
**Rule Description:** Where a lighting system has been designed and submitted with design documents, lighting power shall be determined in accordance with Sections 9.1.3 and 9.1.4.  
**Appendix G Section:** Section G3.1-6(b) Modeling Requirements for the Proposed Design  
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

          - Case 1: Lighting power in the proposed RMR is as designed and cannot be verified by RCT: ```if space_p.interior_lighting == interior_lighting_b: CAUTION```

          - Case 2: Lighting power in the proposed RMR does not match U_RMR: ```else: FAIL```
