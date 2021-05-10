
# Envelope - Rule 5-11  

**Rule ID:** 5-11  
**Rule Description:**  Manual window shading devices such as blinds or shades are not required to be modeled.  
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

      **Rule Assertion:** Baseline vertical fenestrations are not modeled with manual window shading devices: ```window.has_manual_interior_shades == FALSE for window in windows_baseline```  
