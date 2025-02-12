# Envelope - Rule 5-5
**Schema Version** 0.0.23  
**Primary Rule:** False 
**Rule ID:** 5-5  
**Rule Description:** Baseline below-grade walls shall conform with assemblies detailed in Appendix A Concrete block, A4).  
**Appendix G Section:** Section G3.1-5(b) Building Envelope Modeling Requirements for the Baseline building  
**Appendix G Section Reference:** None  

**Applicability:** All required data elements exist for B_RMD  
**Applicability Checks:**  
  1. Surfaces that are a regulated below-grade wall 

**Evaluation Context:** Each Data Element  
**Data Lookup:** None  
**Function Call:**

  1. get_more_stringent_surface_conditioning_category()  
  2. get_opaque_surface_type()  

## Rule Logic:  

- Get surface conditioning category dictionary for B_RMD: ```scc_dictionary_b = get_more_stringent_surface_conditioning_category(B_RMD, P_RMD)```  

- For each building segment in the Baseline model: ```for building_segment_b in B_RMD.building.building_segments:```

  - For each zone in building segment: ```for zone_b in building_segment_b.zones:```  

    - For each surface in zone: ```for surface_b in zone_b.surfaces:```

        **Rule Assertion:**  

        Case 1: Surface is a below-grade wall and is regulated; outcome is UNDETERMINED: ```if ( ( get_opaque_surface_type(surface_b) == "BELOW-GRADE WALL" ) AND ( scc_dictionary_b[surface_b.id] != UNREGULATED ) ): 
        outcome = "UNDETERMINED" and raise_message "<Insert surface_b.id> is a regulated below-grade wall surface. Conduct a manual check to confirm that Baseline below-grade wall assemblies conform with assemblies detailed in Appendix A."```  

        Case 2: Else; outcome is NOT_APPLICABLE: ```else: outcome = NOT_APPLICABLE```  

**Notes:**

1. Update Rule ID from 5-7 to 5-5 on 10/26/2023

**[Back](../_toc.md)
