
# Envelope - Rule 5-31  

**Rule ID:** 5-31  
**Rule Description:** Manual fenestration shading devices, such as blinds or shades, shall be modeled or not modeled the same as in the baseline building design.  
**Rule Assertion:** B-RMR subsurface.has_manual_interior_shades=P-RMR subsurface.has_manual_interior_shades  
**Appendix G Section:** Section G3.1-5(a)(4) Building Modeling Requirements for the Proposed design and G3.1-5(d) Building Modeling Requirements for Baseline building  
**Appendix G Section Reference:**  None

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:** None  

**Manual Checks:** None  
**Evaluation Context:**  Each Data Element  
**Data Lookup:** None  
**Function Call:**  

  1. match_data_element()
  2. get_opaque_surface_type()

## Rule Logic:

- For each building segment in the Baseline model: `for building_segment_b in B_RMR.building.building_segments:`

  - For each thermal block in building segment: `for thermal_block_b in building_segment_b.thermal_blocks:`

    - For each zone in thermal block: `for zone_b in thermal_block_b.zones:`

      - For each surface in zone: `for surface_b in zone_b.surfaces:`

        - Check if surface is above-grade wall: `if get_opaque_surface_type(surface_b) == "ABOVE-GRADE WALL":`

          - For each subsurface in surface: `for subsurface_b in surface_b:`

            - Get matching subsurface in P_RMR:`subsurface_p = match_data_element(P_RMR, Subsurfaces, subsurface_b.id)`

              **Rule Assertion:**

              - Case 1: For each subsurface, if manual fenestration shading devices are modeled or not modeled the same in B_RMR as in P_RMR: `if subsurface_b.has_manual_interior_shades == subsurface_p.has_manual_interior_shades: PASS`

              - Case 2: Else: `else: FAIL`

**[Back](../_toc.md)**

**Notes**
1. Will B_RMR and P_RMR have different number of subsurfaces or different ID?
