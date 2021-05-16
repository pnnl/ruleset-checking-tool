
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

- For each building segment in the Baseline model: ```for building_segment_b in B_RMR.building.building_segments:```  

  - For each thermal_block in building segment: ```for thermal_block_b in building_segment_b.thermal_blocks:```  

  - For each zone in thermal block: ```for zone_b in thermal_block_b.zones:```  

  - For each space in thermal zone: ```for space_b in zone_b.spaces:```  

    - Get surface in space: ```for surface_b in space_b.surfaces:```  

      - Get vertical glazings in exterior wall: ```if ( 60<= surface_b.tile <= 90 ) AND ( surface_b.adjacent_to == "AMBIENT" ): windows_b = surface_b.fenestration_subsurfaces```  

        **Rule Assertion:** Baseline vertical fenestrations are not required to be modeled with manual window shading devices: ```if window.has_manual_interior_shades == TRUE for window in windows_b: raise_warning```  
