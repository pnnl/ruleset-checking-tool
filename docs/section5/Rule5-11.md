# Envelope - Rule 5-11
**Schema Version** 0.0.23  
**Primary Rule:** False 
**Rule ID:** 5-11  
**Rule Description:**  Baseline slab-on-grade assemblies must conform with assemblies detailed in Appendix A ( Slab-on-grade floors shall match the F-factor for unheated slabs from the same tables (A6).).  
**Appendix G Section:** Section G3.1-5(b) Building Envelope Modeling Requirements for the Baseline building  
**Appendix G Section Reference:** None  

**Applicability:** All required data elements exist for B_RMD  
**Applicability Checks:**  
  1. Surfaces that are a regulated slab-on-grade

**Evaluation Context:** Each Data Element  
**Data Lookup:** None  
**Function Call:**

  1. get_surface_conditioning_category()  
  2. get_opaque_surface_type()  

## Rule Logic:  

- Get surface conditioning category dictionary for B_RMD: ```scc_dictionary_b = get_surface_conditioning_category(B_RMD)```  

- For each building segment in the Baseline model: ```for building_segment_b in B_RMD.building.building_segments:```  

  - For each zone in building segment: ```for zone_b in building_segment_b.zones:```

    - For each surface in zone: ```for surface_b in zone_b.surfaces:```  

      **Rule Assertion:**
        
      Case 1: Surface is a heated or unheated slab-on-grade: ```if get_opaque_surface_type(surface_p) in ["HEATED SLAB-ON-GRADE", "UNHEATED SLAB-ON-GRADE"]:
      outcome = "UNDETERMINED" and raise_message "<Insert surface_b.id> is a regulated slab-on-grade surface. Conduct a manual check to confirm that Baseline slab-on-grade assemblies conform with assemblies detailed in Appendix A."```  

      Case 2: Else; outcome is NOT_APPLICABLE: ```else: outcome = NOT_APPLICABLE```


**Notes:**

1. Update Rule ID from 5-14 to 5-11 on 10/26/2023


**[Back](../_toc.md)