
# Envelope - Rule 5-23  

**Rule ID:** 5-23  
**Rule Description:** Manual fenestration shading devices, such as blinds or shades, shall be modeled or not modeled the same as in the baseline building design.  
**Rule Assertion:** B-RMD subsurface.has_manual_interior_shades=P-RMD subsurface.has_manual_interior_shades  
**Appendix G Section:** Section G3.1-5(a)(4) Building Modeling Requirements for the Proposed design and G3.1-5(d) Building Modeling Requirements for Baseline building  
**Appendix G Section Reference:**  None

**Applicability:** All required data elements exist for B_RMD  
**Applicability Checks:** None  

**Manual Checks:** None  
**Evaluation Context:**  Each Data Element  
**Data Lookup:** None  
**Function Call:**  

  1. match_data_element()

## Rule Logic:

- For each building segment in the Baseline model: `for building_segment_b in B_RMD.building.building_segments:`

  - For each zone in thermal block: `for zone_b in building_segment_b.zones:`

    - For each surface in zone: `for surface_b in zone_b.surfaces:`

      - Get matching surface in P_RMD: `surface_p = match_data_element(P_RMD, Surfaces, surface_b.id)`

        - For each subsurface in surface in P_RMD: `for subsurface_p in surface_p.subsurfaces:`

          - Calculate the total number of subsurfaces that have manual shades modeled: `if subsurface_p.has_manual_interior_shades: num_shades += 1`

        - Check if subsurfaces in P_RMD have different manual shade status, flag for manual check: `if ( num_shades != LEN(surface_p.subsurfaces) ) AND ( num_shades != 0 ): manual_check_flag = TRUE`

        - Else, for each subsurface in surface in B_RMD: `else: for subsurface_b in surface_b.subsurfaces:`

          - Check if subsurface is modeled with the same manual shade status as in P_RMD: `if subsurface_b.has_manual_interior_shades == surface_p.subsurfaces[0].has_manual_interior_shades: shade_match_flag = TRUE`

        **Rule Assertion:**

        - Case 1: For each surface, if manual check flag is True: `if manual_check_flag: CAUTION and raise_warning "SURFACE IN P-RMD HAS SUBSURFACES MODELED WITH DIFFERENT MANUAL SHADE STATUS. VERIFY IF SUBSURFACES MANUAL SHADE STATUS IN B-RMD ARE MODELED THE SAME AS IN P-RMD".`

        - Case 2: Else if shade_match_flag is True: `if shade_match_flag: PASS`

        - Case 3: Else: `else: FAIL`

**Notes:**

1. Update Rule ID from 5-31 to 5-23 on 10/26/2023

**[Back](../_toc.md)**
