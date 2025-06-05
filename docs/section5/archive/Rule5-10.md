
# Envelope - Rule 5-10  

**Rule ID:** 5-10  
**Rule Description:** Baseline above-grade wall assemblies must conform with assemblies detailed in  Appendix A (Steel-framed A3.3).  
**Appendix G Section:** Section G3.1-5(b) Building Envelope Modeling Requirements for the Baseline building  
**Appendix G Section Reference:** None  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:** None  

**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  
**Function Call:**

  1. get_surface_conditioning_category()  
  2. get_opaque_surface_type()  

## Rule Logic:  

- Get surface conditioning category dictionary for B_RMR: ```scc_dictionary_b = get_surface_conditioning_category(B_RMR)```  

- For each building segment in the Baseline model: ```for building_segment_b in B_RMR.building.building_segments:```  

  - For each thermal_block in building segment: ```for thermal_block_b in building_segment_b.thermal_blocks:```  

    - For each zone in thermal block: ```for zone_b in thermal_block_b.zones:```  

      - For each surface in zone: ```for surface_b in zone_b.surfaces:```  

        - If surface is above-grade wall and is regulated, get surface construction: ```if ( ( get_opaque_surface_type(surface_b) == "ABOVE-GRADE WALL" ) AND ( scc_dictionary_b[surface_b.id] != UNREGULATED ) ): construction_b = surface_b.construction```  

          **Rule Assertion:**  

          Case 1: Above-grade wall construction is specified with layers and a U-factor is provided: ```if (  ( construction_b.surface_construction_input_option == "LAYERS" ) AND ( construction_b.u_factor ) ): PASS```  

          Case 2: Else: ```else: FAIL```  
