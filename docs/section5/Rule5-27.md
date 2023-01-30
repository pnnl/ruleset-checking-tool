
# Envelope - Rule 5-27  

**Rule ID:** 5-27  
**Rule Description:** Fenestration (window and skylight) SHGC in the proposed model must match the user model.  
**Rule Assertion:** P-RMR subsurface:SHGC = U-RMR subsurface:SHGC  
**Appendix G Section:** Section G3.1-1(a) Building Modeling Requirements for the proposed building  
**Appendix G Section Reference:**  None

**Applicability:** All required data elements exist for P_RMR  
**Applicability Checks:** None  

**Manual Checks:** None  
**Evaluation Context:** Each Data Element  
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

            - Case 1: For each subsurface, subsurface solar heat gain coefficient in P_RMR is equal to that in U_RMR: `if subsurface_p.solar_heat_gain_coefficient == subsurface_u.solar_heat_gain_coefficient: PASS`

            - Case 2: Else: `else: FAIL`

**[Back](../_toc.md)**
