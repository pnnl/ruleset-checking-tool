
# Envelope - Rule 5-23  

**Rule ID:** 5-23  
**Rule Description:** Subsurface area in the proposed design must be as-designed.  
**Rule Assertion:** P-RMR subsurface on each surface (subsurface.glazed_area+subsurface.opaque_area) = U-RMR (subsurface.glazed_area+subsurface.opaque_area)  
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

        - Get total subsurface area in surface: `total_subsurface_area_p = sum((subsurface.glazed_area + subsurface.opaque_area) for subsurface in surface_p.subsurfaces):`

        - Get matching surface in U_RMR: `surface_u = match_data_element(U_RMR, Surfaces, surface_p.id)`

          - Get total subsurface area in surface in U_RMR: `total_subsurface_area_u = sum((subsurface.glazed_area + subsurface.opaque_area) for subsurface in surface_u.subsurfaces):`

          **Rule Assertion:**

          - Case 1: For each surface, if total subsurface area in P_RMR is equal to that in U_RMR: `if total_subsurface_area_p == total_subsurface_area_u: PASS`

          - Case 2: Else: `else: FAIL`
    ## Note:  
    - For future rrevision: Each surface in U-RMR may have multiple subsurface objects of different types, U-factors, SHGC, VT, overhangs, etc. So I think we need to check equivalency for each subsurface in U-RMR vs P-RMR without any aggregation, similar to how U-factor equivalency is checked for 5-25. 

**Notes:**

1. USER = PROPOSED match archived on 10/26/2023

**[Back](../_toc.md)**
