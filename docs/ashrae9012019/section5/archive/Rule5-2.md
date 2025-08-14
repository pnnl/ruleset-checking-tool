
# Envelope - Rule 5-2  

**Rule ID:** 5-2  
**Rule Description:** Orientation is the same in user model and proposed model.  
**Appendix G Section:** Section G3.1-5(a) Building Envelope Modeling Requirements for the Proposed building  
**Appendix G Section Reference:** None  

**Applicability:** All required data elements exist for P_RMR  
**Applicability Checks:** None  

**Manual Check:** None  
**Evaluation Context:** Building  
**Data Lookup:** None  

## Rule Logic:  

- For each building segment in the Proposed model: ```for building_segment_p in P_RMR.building.building_segments:```  

  - For each thermal_block in building segment: ```for thermal_block_p in building_segment_p.thermal_blocks:```  

    - For each zone in thermal block: ```for zone_p in thermal_block_p.zones:```  

      - For each surface in zone: ```for surface_p in zone_p.surfaces:```  

        - Get matching surface from U_RMR: ```surface_u = match_data_element(U_RMR, surfaces, surface_p.id)```  

          - If surface azimuth in P_RMR does not match U_RMR, flag surface: ```if surface_p.azimuth != surface_u.azimuth: surface_check.append(surface)```  

- **Rule Assertion:**  
  Case 1: All surface azimuth in P_RMR matches U-RMR: ```if len(surface_check) == 0: PASS```  

  Case 2: Else: ```else: FAIL```  


**Notes:**

1. USER-PROPOSED match rule, move to archive (10/26/2023)