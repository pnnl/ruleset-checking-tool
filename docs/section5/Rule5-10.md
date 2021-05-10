
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

- For each building segment in the Baseline model: ```for building_segment_baseline in B_RMR.building.building_segments:```  

  - For each thermal_block in building segment: ```for thermal_block_baseline in building_segment_baseline.thermal_blocks:```  

  - For each zone in thermal block: ```for zone_baseline in thermal_block_baseline.zones:```  

  - For each space in thermal zone: ```for space_baseline in zone_baseline.spaces:```  

    - Get surface in space: ```for surface_baseline in space_baseline.surfaces:```  

      - Get vertical glazings in exterior wall: ```if ( surface_baseline.classification == "WALL" ) AND ( surface_baseline.adjacent_to == "AMBIENT" ): windows_baseline = surface_baseline.fenestration_subsurfaces```  

      **Rule Assertion:** Baseline vertical fenestrations are flush with the exterior wall, and no shading projects shall be modeled: ```(window.has_shading_overhang == FALSE) AND (window.has_shading_sidefins == False) for window in windows_baseline```  (Note XC, any data elements for flush with the exterior wall?)
