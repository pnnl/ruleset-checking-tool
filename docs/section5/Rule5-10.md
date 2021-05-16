
# Envelope - Rule 5-10  

**Rule ID:** 5-10  
**Rule Description:**  Fenestration for new buildings, existing buildings, and additions shall be assumed to be flush with the exterior wall, and no shading projections shall be modeled.  
**Rule Assertion:** Baseline RMR = expected value  
**Appendix G Section:** Section G3.1-5(d) Building Envelope Modeling Requirements for the Baseline building  
**Appendix G Section Reference:** None  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  None  

**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  

## Rule Logic:  

- For each building segment in the Baseline model: ```for building_segment_b in B_RMR.building.building_segments:```  

  - For each thermal_block in building segment: ```for thermal_block_b in building_segment_b.thermal_blocks:```  

  - For each zone in thermal block: ```for zone_b in thermal_block_b.zones:```  

  - For each space in thermal zone: ```for space_b in zone_b.spaces:```  

    - For each surface in space: ```for surface_b in space_b.surfaces:```  

      - Get vertical glazings in exterior wall: ```if ( 60<= surface_b.tilt <= 90 ) AND ( surface_b.adjacent_to == "AMBIENT" ): windows_b = surface_b.fenestration_subsurfaces```  

        **Rule Assertion:** Baseline vertical fenestrations are flush with the exterior wall, and no shading projects shall be modeled: ```if (window.has_shading_overhang == TRUE) OR (window.has_shading_sidefins == TRUE) for window in windows_b: raise_warning```  
