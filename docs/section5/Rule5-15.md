
# Envelope - Rule 5-15  

**Rule ID:** 5-15  
**Rule Description:**  The  exterior roof surfaces shall be modeled using a solar reflectance of 0.30.  
**Rule Assertion:** Baseline RMR = expected value  
**Appendix G Section:** Section G3.1-5(f) Building Envelope Modeling Requirements for the Baseline building  
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

    - Get surfaces in space: ```for surface_baseline in space_baseline.surfaces:```  

      - Get surface optics for roof: ```if ( surface_baseline.classification == "CEILING" ) AND ( surface_baseline.adjacent_to == "AMBIENT" ): roof_surface_optics_baseline = surface_baseline.surface_optics```  

      **Rule Assertion:** Baseline roof solar reflectance is 0.30: ```roof_surface_optics_baseline.absorptance_solar_exterior == 0.70```  
