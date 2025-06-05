
# Envelope - Rule 5-14  

**Rule ID:** 5-14  
**Rule Description:**  Baseline slab-on-grade assemblies must conform with assemblies detailed in Appendix A ( Slab-on-grade floors shall match the F-factor for unheated slabs from the same tables (A6).).  
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

        - If surface is heated slab-on-grade: ```if get_opaque_surface_type(surface_b) == "HEATED SLAB-ON-GRADE:```  

          **Rule Assertion:**  

          Case 1: If heated slab-on-grade construction is modeled in B_RMR: ```FAIL```  

        - Else if surface is unheated slab-on-grade and is regulated, get surface construction: ```else if ( ( get_opaque_surface_type(surface_b) == "UNHEATED SLAB-ON-GRADE" ) AND ( scc_dictionary_b[surface_b.id] != UNREGULATED ) ): construction_b = surface_b.construction```  

          **Rule Assertion:**  

          Case 2: Unheated slab-on-grade construction is specified with layers and an F-factor is provided: ```if (  ( construction_b.surface_construction_input_option == "LAYERS" ) AND ( construction_b.f_factor ) ): PASS```  

          Case 3: Else: ```else: FAIL```  
