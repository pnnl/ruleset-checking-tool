
# Envelope - Rule 5-41

**Rule ID:** 5-41
**Rule Description:** Opaque roof surfaces that are not regulated (not part of opaque building envelope) must be modeled with the same thermal emittance and solar reflectance in the baseline as in the proposed design. 
**Appendix G Section:** Section G3.1-5 Building Envelope Modeling Requirements for the Baseline building  
**Appendix G Section Reference:** None  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:** None  

**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  
**Function Call:**

  - get_surface_conditioning_category()
  - get_opaque_surface_type()
  - match_data_element()

## Rule Logic:  

- Get surface conditioning category dictionary for B_RMR: `scc_dictionary_b = get_surface_conditioning_category(B_RMR)`  

- For each building segment in the Proposed model: `for building_segment_b in B_RMR.building.building_segments:`  

  - For each zone in building segment: `for zone_b in building_segment_b.zones:`  

    - For each surface in zone: `for surface_b in zone_b.surfaces:`  

      - Check if surface is an unregulated roof: `if (scc_dictionary_b[surface_b.id] == UNREGULATED) AND (get_opaque_surface_type(surface_b) == "ROOF"):`

        - Get matching surface from P_RMR: `surface_p = match_data_element(P_RMR, surfaces, surface_b.id)`

          **Rule Assertion:**  

          - Case 1: If thermal emittance and solar reflectance in B_RMR matches P_RMR; PASS: `if (surface_b.construction.optical_properties.absorptance_thermal_exterior == surface_p.construction.optical_properties.absorptance_thermal_exterior) AND (surface_b.construction.optical_properties.absorptance_solar_exterior == surface_p.construction.optical_properties.absorptance_solar_exterior): PASS`

          - Case 2: Else: `else: FAIL`

**Notes:**

1. Created on 11/9/2023 with Rule ID 5-41


**[Back](../_toc.md)