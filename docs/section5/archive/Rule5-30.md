
# Envelope - Rule 5-30  

**Rule ID:** 5-30  
**Rule Description:** Proposed fenestration has the same shading projections as the user model.  
**Rule Assertion:** P-RMR subsurface:has_shading_overhang = U-RMR subsurface:has_shading_overhang; P-RMR subsurface:has_shading_sidefins = U-RMR subsurface:has_shading_sidefins  
**Appendix G Section:** Section G3.1-1(a) Building Modeling Requirements for the Proposed design  
**Appendix G Section Reference:**  None

**Applicability:** All required data elements exist for P_RMR  
**Applicability Checks:** None  

**Manual Checks:** None  
**Evaluation Context:**  Each Data Element  
**Data Lookup:** None  
**Function Call:**  

  1. match_data_element()
  2. get_opaque_surface_type()

## Rule Logic:

- For each building segment in the Proposed model: `for building_segment_p in P_RMR.building.building_segments:`

  - For each thermal block in building segment: `for thermal_block_p in building_segment_p.thermal_blocks:`

    - For each zone in thermal block: `for zone_p in thermal_block_p.zones:`

      - For each surface in zone: `for surface_p in zone_p.surfaces:`

        - Check if surface is above-grade wall or roof: `if get_opaque_surface_type(surface_p) in ["ABOVE-GRADE WALL", "ROOF"]:`

          - For each subsurface in surface: `for subsurface_p in surface_p:`

            - Get matching subsurface in U_RMR: `subsurface_u = match_data_element(U_RMR, Subsurfaces, surface_p.id)`

              **Rule Assertion:**

              - Case 1: For each subsurface, if subsurface shading projections in P_RMR are the same as in U_RMR: `if ( subsurface_p.has_shading_overhang == subsurface_u.has_shading_overhang ) AND ( subsurface_p.has_shading_sidefins == subsurface_u.has_shading_sidefins ): PASS`

              - Case 2: Else: `else: FAIL and raise_warning "FENESTRATION IN THE PROPOSED DESIGN DOES NOT HAVE THE SAME SHADING PROJECTIONS AS IN THE USER MODEL."`

**Notes:**

1. USER=PROPOSED match, archived on 10/26/2023

**[Back](../_toc.md)**
