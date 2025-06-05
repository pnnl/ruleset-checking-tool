
# Envelope - Rule 5-29  

**Rule ID:** 5-29  
**Rule Description:** The  baseline roof surfaces shall be modeled using a thermal emittance of 0.9.  
**Rule Assertion:** B-RMD SurfaceOpticalProperties:thermal_emittance = 0.9  
**Appendix G Section:** Section G3.1-5(f) Building Envelope Modeling Requirements for the Baseline building  
**Appendix G Section Reference:** None  

**Applicability:** All required data elements exist for B_RMD  
**Applicability Checks:**  None  

**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  
**Function Call:**  

  1. get_opaque_surface_type()
  2. get_surface_conditioning_category()

## Rule Logic:  

- Get surface conditioning category dictionary for B_RMD: ```scc_dictionary_b = get_surface_conditioning_category(B_RMD)```  

- For each building segment in the Baseline model: `for building_segment_b in B_RMD.building.building_segments:`

  - For each zone_b in building_segment_b: `for zone_b in building_segments.zones:`

    - For each surface_b in zone_b: `for surface_b in zone_b.surfaces;`

      - Check if surface is roof and is regulated, get surface optical properties: `if ( get_opaque_surface_type(surface_b.id) == "ROOF" ) AND ( scc_dictionary_b[surface_b.id] != "UNREGULATED" ): surface_optical_properties_b = surface_b.surface_optical_properties`

        **Rule Assertion:**  

        - Case 1: If roof surface thermal emittance is equal to 0.9: `if surface_optical_properties_b.absorptance_thermal_exterior == 0.9: PASS`

        - Case 2: Else: `Else: FAIL`

**Notes:**

1. Update Rule ID from 5-40 to 5-30 on 10/26/2023
2. Update Rule ID from 5-30 to 5-29 on 12/22/2023


**[Back](../_toc.md)**
