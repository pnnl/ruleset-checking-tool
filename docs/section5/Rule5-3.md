
# Envelope - Rule 5-3  

**Rule ID:** 5-3  
**Rule Description:** Baseline roof assemblies must conform with assemblies detailed in Appendix A.  
**Appendix G Section:** Section G3.1-5(b) Building Envelope Modeling Requirements for the Baseline building  
**Appendix G Section Reference:** None  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:** None  

**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  

## Rule Logic:  

- For each building segment in the Baseline model: ```for building_segment_b in B_RMR.building.building_segments:```  

  - For each thermal_block in building segment: ```for thermal_block_b in building_segment_b.thermal_blocks:```  

    - For each zone in thermal block: ```for zone_b in thermal_block_b.zones:```  

      - For each surface in zone, get surface type, ```for surface in zone_b.surfaces: surface_type_b = get_opaque_surface_type(surface)```  

        - If surface is roof or ceiling, get surface construction: ```if surface_type_b == "ROOF": construction_b = surface.construction```  

          **Rule Assertion:**  

          Case 1: Surface construction is specified with layers and a U-factor or R-value is provided: ```if (  ( construction_b.surface_construction_input_option == "LAYERS" ) AND ( construction.u_factor OR construction.r_value ) ): PASS```  

          Case 2: Else: ```else: FAIL```
