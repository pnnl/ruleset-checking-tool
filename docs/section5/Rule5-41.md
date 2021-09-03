
# Envelope - Rule 5-41  

**Rule ID:** 5-41  
**Rule Description:** The  proposed roof surfaces shall be modeled using the same thermal emittance as in the user model.  
**Rule Assertion:** P-RMR SurfaceOpticalProperties:thermal_emittance = U-RMR SurfaceOpticalProperties:thermal_emittance  
**Appendix G Section:** Section G3.1-1(a) Building Envelope Modeling Requirements for the Proposed design  
**Appendix G Section Reference:** None  

**Applicability:** All required data elements exist for P_RMR  
**Applicability Checks:**  None  

**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  
**Function Call:**  

  1. get_opaque_surface_type()
  2. get_surface_conditioning_category()
  3. match_data_element()

## Rule Logic:  

- Get surface conditioning category dictionary for P_RMR: `scc_dictionary_p = get_surface_conditioning_category(P_RMR)`

- For each building segment in the Proposed model: `for building_segment_p in P_RMR.building.building_segments:`  

  - For each thermal block in building segment: `for thermal_block_p in building_segment_p.thermal_blocks:`  

    - For each zone in thermal block: `for zone_p in thermal_block_p.zones:`  

      - For each surface in zone: `for surface_p in zone_p.surfaces;`

        - Check if surface is roof and is regulated, get matching surface in U_RMR: `if ( get_opaque_surface_type(surface_p.id) == "ROOF" ) AND ( scc_dictionary_p[surface_p.id] != "UNREGULATED" ): surface_u = match_data_element(U_RMR, Surfaces, surface_p.id)`  

          **Rule Assertion:**  

          - Case 1: If roof surface thermal emittance in P_RMR matches that in U_RMR: `if surface_p.surface_optical_properties.absorptance_thermal_exterior == surface_u.surface_optical_properties.absorptance_thermal_exterior: PASS`

          - Case 2: Else if roof surface thermal emittance in P_RMR does not match that in U_RMR but is equal to 0.9: `else if surface_p.surface_optical_properties.absorptance_thermal_exterior == 0.9: PASS and raise_warning "ROOF SURFACE EMITTANCE IN P-RMR DOES NOT MATCH THAT IN U-RMR BUT IS EQUAL TO 0.9. WHERE AGED TEST DATA ARE UNAVAILABLE, THE ROOF SURFACE MAY BE MODELED WITH A REFLECTANCE OF 0.30 AND A THERMAL EMITTANCE OF 0.90. P-RMR MAY NOT BE EQUAL TO U-RMR IF AGED TEST DATA IS NOT AVAILABLE."`

          - Case 3: Else: `Else: FAIL`

**[Back](../_toc.md)**
