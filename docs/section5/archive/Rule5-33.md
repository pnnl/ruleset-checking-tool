
# Envelope - Rule 5-33  

**Rule ID:** 5-33  
**Rule Description:** Automatically controlled fenestration shading devices must be modeled in the proposed design the same as in user model.  
**Rule Assertion:** P-RMR subsurface:has_automatic_shades = U-RMR subsurface:has_automatic_shades  
**Appendix G Section:** Section G3.1-5(a)(4) Building Modeling Requirements for the Proposed design  
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

            - Case 1: For each subsurface in P_RMR, if automatically controlled shading devices are modeled the same as in U_RMR: `if subsurface_p.has_automatic_shades == subsurface_u.has_automatic_shades: PASS`

            - Case 2: Else: `else: FAIL`

**Notes:**

1. USER=PROPOSED match, archived on 10/26/2023

**[Back](../_toc.md)**
