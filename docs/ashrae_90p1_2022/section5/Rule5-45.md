# Envelope - Rule 5-45  

**Rule ID:** 5-45  
**Rule Description:** The baseline above-grade wall surfaces shall be modeled with a thermal emittance of 0.90.  
**Rule Assertion:** B-RMD SurfaceOpticalProperties:absorptance_thermal_exterior = 0.90 
**Appendix G Section:** Table G3.1 Section 5(j) Baseline  
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

      - Check if surface is above grade wall and is regulated, get surface optical properties: `if ( get_opaque_surface_type(surface_b.id) == "ABOVE-GRADE WALL" ) AND ( scc_dictionary_b[surface_b.id] != "UNREGULATED" ): surface_optical_properties_b = surface_b.surface_optical_properties`

        **Rule Assertion:**  

        - Case 1: If above-grade wall surface thermal emittance is equal to 0.90: `if surface_optical_properties_b.absorptance_thermal_exterior == 0.90: PASS`

        - Case 2: Else: `Else: FAIL`

**Notes:**
- None


**[Back](../_toc.md)**