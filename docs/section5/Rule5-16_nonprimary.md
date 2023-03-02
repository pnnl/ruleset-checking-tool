# Envelope - Rule 5-16
**Schema Version** 0.0.23  
**Primary Rule:** False 
**Rule ID:** 5-16  
**Rule Description:** Slab-on-grade F-factor in the proposed design must be modeled as-designed  
**Appendix G Section:** Section G3.1-5(a) Building Envelope Modeling Requirements for the Proposed building  
**Appendix G Section Reference:** None  

**Applicability:** All required data elements exist for P_RMR  
**Applicability Checks:**  
  1. Surfaces that are slab-on-grade

**Evaluation Context:** Each Data Element  
**Data Lookup:** None  
**Function Call:**

  - get_opaque_surface_type()

## Rule Logic:  

- For each building segment in the Proposed model: `for building_segment_p in P_RMR.building.building_segments:`  

  - For each zone in building segment: `for zone_p in building_segment_p.zones:`  

    - For each surface in zone: `for surface_p in zone_p.surfaces:`  
      
      **Rule Assertion:**
        
      Case 1: Surface is a slab-on-grade, outcome is UNDETERMINED: ```if get_opaque_surface_type(surface_p) in ["HEATED SLAB-ON-GRADE", "UNHEATED SLAB-ON-GRADE"]:
      outcome = "UNDETERMINED" and raise_message "<Insert surface_b.id> is a slab-on-grade surface. Conduct a manual check to confirm that Proposed slab-on-grade assemblies are modeled as-designed."```

      Case 2: Else; outcome is NOT_APPLICABLE: ```else: outcome = NOT_APPLICABLE```  
