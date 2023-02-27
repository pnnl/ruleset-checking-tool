# Envelope - Rule 5-10
**Schema Version** 0.0.23  
**Primary Rule:** False 
**Rule ID:** 5-10  
**Rule Description:** Baseline above-grade wall assemblies must conform with assemblies detailed in  Appendix A (Steel-framed A3.3).  
**Appendix G Section:** Section G3.1-5(b) Building Envelope Modeling Requirements for the Baseline building  
**Appendix G Section Reference:** None  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:** 
  1. Surfaces that are a regulated above-grade wall
 
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  
**Function Call:**

  1. get_surface_conditioning_category()  
  2. get_opaque_surface_type()  

## Rule Logic:  

- Get surface conditioning category dictionary for B_RMR: ```scc_dictionary_b = get_surface_conditioning_category(B_RMR)```  

- For each building segment in the Baseline model: ```for building_segment_b in B_RMR.building.building_segments:```

  - For each zone in building segment: ```for zone_b in building_segment_b.zones:```  

    - For each surface in zone: ```for surface_b in zone_b.surfaces:```

        **Rule Assertion:**  

        Case 1: Surface is an above-grade wall and is regulated: ```if ( ( get_opaque_surface_type(surface_b) == "ABOVE-GRADE WALL" ) AND ( scc_dictionary_b[surface_b.id] != UNREGULATED ) ):
        outcome = "UNDETERMINED" and raise_message "<Insert surface_b.id> is a regulated above-grade wall surface. Conduct a manual check to confirm that Baseline above-grade wall assemblies conform with assemblies detailed in Appendix A."```  

        Case 2: Else; outcome is NOT_APPLICABLE: ```else: outcome = NOT_APPLICABLE```  
