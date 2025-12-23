
# Envelope - Rule 5-9  

**Rule ID:** 5-9  
**Rule Description:** Below-grade wall C-factor must be the same in the proposed model as in the user model  
**Appendix G Section:** Section G3.1-5(a) Building Envelope Modeling Requirements for the Proposed building  
**Appendix G Section Reference:** None  

**Applicability:** All required data elements exist for P_RMR  
**Applicability Checks:** None  

**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  
**Function Call:**

  - get_opaque_surface_type()
  - match_data_element()

## Rule Logic:  

- For each building segment in the Proposed model: `for building_segment_p in P_RMR.building.building_segments:`  

  - For each thermal_block in building segment: `for thermal_block_p in building_segment_p.thermal_blocks:`  

    - For each zone in thermal block: `for zone_p in thermal_block_p.zones:`  

      - For each surface in zone: `for surface_p in zone_p.surfaces:`  

        - Check if surface is below-grade wall: `if get_opaque_surface_type(surface_p) == "BELOW-GRADE WALL":`

          - Get matching surface from U-RMR: `surface_u = match_data_element(U_RMR, surfaces, surface_p.id)`  

            **Rule Assertion:**  

            - Case 1: Surface construction C-factor in P_RMR matches U_RMR: `if surface_p.construction.c_factor == surface_u.construction.c_factor: PASS`  

            - Case 2: Else: `else: FAIL`  

**Notes:**

1. USER=PROPOSED match is archived 10/26/2023