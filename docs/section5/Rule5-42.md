
# Envelope - Rule 5-42  

**Rule ID:** 5-42  
**Rule Description:** The baseline roof surfaces shall be modeled using a solar reflectance of 0.30.  
**Rule Assertion:** B-RMR SurfaceOpticalProperties:absorptance_solar_exterior = 0.7  
**Appendix G Section:** Section G3.1-5(g) Building Envelope Modeling Requirements for the Baseline building  
**Appendix G Section Reference:** None  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  None  

**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  
**Function Call:**  

  1. get_opaque_surface_type()
  2. get_surface_conditioning_category()

## Rule Logic:  

- Get surface conditioning category dictionary for B_RMR: `scc_dictionary_b = get_surface_conditioning_category(B_RMR)`

- For each building segment in the Baseline model: `for building_segment_b in B_RMR.building.building_segments:`  

  - For each thermal_block in building segment: `for thermal_block_b in building_segment_b.thermal_blocks:`  

    - For each zone in thermal block: `for zone_b in thermal_block_b.zones:`  

      - For each surface in zone: `for surface_b in zone_b.surfaces;`

        - Check if surface is roof and is regulated, get surface optical properties: `if ( get_opaque_surface_type(surface_b.id) == "ROOF" ) AND ( scc_dictionary_b[surface_b.id] != "UNREGULATED" ): surface_optical_property_b = surface_b.optical_properties`  

          **Rule Assertion:**  

          - Case 1: If roof surface solar reflectance is equal to 0.3: `if surface_optical_property_b.absorptance_solar_exterior == 0.7: PASS`  

          - Case 2: Else: `Else: FAIL`

**[Back](../_toc.md)**
