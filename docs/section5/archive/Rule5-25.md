
# Envelope - Rule 5-25  

**Rule ID:** 5-25  
**Rule Description:** Fenestration (window and skylight) U-factors in the proposed model must match the user model.  
**Rule Assertion:** P-RMR subsurface:U_factor = U-RMR subsurface:U_factor  
**Appendix G Section:** Section G3.1-1(a) Building Modeling Requirements for the proposed building  
**Appendix G Section Reference:**  None

**Applicability:** All required data elements exist for P_RMR  
**Applicability Checks:** None  

**Manual Checks:** None  
**Evaluation Context:**  Each Data Element  
**Data Lookup:** None  
**Function Call:**  

  1. match_data_element()

## Rule Logic:

- For each building segment in the Proposed model: `for building_segment_p in P_RMR.building.building_segments:`

  - For each thermal block in building segment: `for thermal_block_p in building_segment_p.thermal_blocks:`

    - For each zone in thermal block: `for zone_p in thermal_block_p.zones:`  

      - For each surface in zone: `for surface_p in zone_p.surfaces:`  

        - For each subsurface in surface: `for subsurface_p in surface_p.subsurfaces:`

          - Get matching subsurface in U_RMR: `subsurface_u = match_data_element(U_RMR, Subsurfaces, subsurface_p.id)`

            **Rule Assertion:**

            - Case 1: For each subsurface, subsurface U-factor in P_RMR is equal to that in U_RMR: `if subsurface_p.u_factor == subsurface_u.u_factor: PASS`

            - Case 2: Else: `else: FAIL`

**Notes:**

1. USER=PROPOSED match archived on 10/26/2023

**[Back](../_toc.md)**
