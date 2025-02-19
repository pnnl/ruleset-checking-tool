
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

        **Rule Assertion:**

        - Case 1: If subsurface is modeled with the same manual shade status as in P_RMD: `if subsurface_b.has_manual_interior_shades == subsurface_p.has_manual_interior_shades: PASS`

        - Case 2: Else: `else: FAIL`

**Notes:**

1. Update Rule ID from 5-31 to 5-23 on 10/26/2023

**[Back](../_toc.md)**
