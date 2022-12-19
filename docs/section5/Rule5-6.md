
# Envelope - Rule 5-6  

**Schema Version:** 0.0.23  
**Rule ID:** 5-6  
**Rule Description:** Building above-grade opaque surface U-factors must be modeled in proposed design as designed.  
**Appendix G Section:** Section G3.1-5(a) Building Envelope Modeling Requirements for the Proposed building  
**Appendix G Section Reference:** None  

**Applicability:** All required data elements exist for P_RMR  
**Applicability Checks:** None  

**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  
**Function Call:**

  - match_data_element()
  - get_opaque_surface_type()

## Rule Logic:  

- For each building segment in the Proposed model: `for building_segment_p in P_RMR.building.building_segments:`  

  - For each zone in building segment: `for zone_p in building_segment_p.zones:`  

    - For each surface in zone: `for surface_p in zone_p.surfaces:`  

      - Check if surface is above-grade opaque surface: `if get_opaque_surface_type(surface_p) in ["ROOF", "FLOOR", "ABOVE-GRADE WALL"]:`

        - Get matching surface from U-RMR: `surface_u = match_data_element(U_RMR, surfaces, surface_p.id)`

          **Rule Assertion:**  

          Case 1: Surface U-factor in P_RMR matches U_RMR: `if surface_p.construction.u_factor == surface_u.construction.u_factor: PASS`  

          Case 2: Else: `else: FAIL`  
