# Envelope - Rule 5-40
**Schema Version:** 0.0.29
**Mandatory Rule:** True    
**Rule ID:** 5-40
**Rule Description:** Opaque roof surfaces that are not regulated (not part of opaque building envelope) must be modeled with the same thermal emittance and solar reflectance in the baseline as in the proposed design. 
**Appendix G Section:** Section G3.1-5 Building Envelope Modeling Requirements for the Baseline building  
**Appendix G Section Reference:** None  

**Applicability:** All required data elements exist for B_RMD
**Applicability Checks:** None  

**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  
**Function Call:**

  - get_more_stringent_surface_conditioning_category()
  - get_opaque_surface_type()
  - match_data_element()

## Rule Logic:  

- Get surface conditioning category dictionary for B_RMD: `scc_dictionary_b = get_more_stringent_surface_conditioning_category(B_RMD, P_RMD)`  

- For each building segment in the Baseline model: `for building_segment_b in B_RMD...building.building_segments:`  

  - For each zone in building segment: `for zone_b in building_segment_b.zones:`  

    - For each surface in zone: `for surface_b in zone_b.surfaces:`  

      - Check if surface is an unregulated roof: `if (scc_dictionary_b[surface_b.id] == UNREGULATED) AND (get_opaque_surface_type(surface_b) == "ROOF"):`

        - Get matching surface from P_RMD: `surface_p = match_data_element(P_RMD, Surface, surface_b.id)`

          **Rule Assertion:**  

          - Case 1: If thermal emittance and solar reflectance in B_RMD matches P_RMD; PASS: `if (surface_b.optical_properties.absorptance_thermal_exterior == surface_p.optical_properties.absorptance_thermal_exterior) AND (surface_b.optical_properties.absorptance_solar_exterior == surface_p.optical_properties.absorptance_solar_exterior): PASS`
          
          - Case 2: Else if the thermal emittance or solar reflectance in B_RMD or P_RMD is NULL; UNDETERMINED: `if any(absorptance_property == "NULL" for absorptance_property in [surface_b.optical_properties.absorptance_thermal_exterior, surface_p.optical_properties.absorptance_thermal_exterior, surface_b.optical_properties.absorptance_solar_exterior, surface_p.optical_properties.absorptance_solar_exterior]): UNDETERMINED`

          - Case 3: Else: `else: FAIL`

**Notes:**

1. Created on 11/9/2023 with Rule ID 5-41
2. Update Rule ID from 5-41 to 5-40 on 12/22/2023


**[Back](../_toc.md)
