
# Envelope - Rule 5-29  

**Rule ID:** 5-29  
**Rule Description:** Baseline fenestration shall be assumed to be flush with the exterior wall, and no shading projections shall be modeled.  
**Rule Assertion:** B-RMR subsurface:has_shading_overhang = false; B-RMR subsurface:has_shading_sidefins = false  
**Appendix G Section:** Section G3.1-5(d) Building Modeling Requirements for the Baseline building  
**Appendix G Section Reference:**  None  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:** None  

**Manual Checks:** None  
**Evaluation Context:**  Each Data Element  
**Data Lookup:** None  
**Function Call:**  

  1. get_opaque_surface_type()
  2. get_surface_conditioning_category()

## Rule Logic:

- Get surface conditioning category dictionary for B_RMR: `scc_dictionary_b = get_surface_conditioning_category(B_RMR)`

- For each building segment in the Baseline model: `for building_segment_b in B_RMR.building.building_segments:`

  - For each thermal block in building segment: `for thermal_block_b in building_segment_b.thermal_blocks:`

    - For each zone in thermal block: `for zone_b in thermal_block_b.zones:`

      - For each surface in zone: `for surface_b in zone_b.surfaces:`

        - Check if surface is above-grade wall or roof and is exterior: `if ( get_opaque_surface_type(surface_b) == "ABOVE-GRADE WALL" ) AND ( scc_dictionary_b[surface_b.id] != "UNREGULATED" ):`

          - For each subsurface in surface: `for subsurface_b in surface_b:`

            **Rule Assertion:**

            - Case 1: For each subsurface, if subsurface is flush with the exterior wall, and no shading projections are modeled: `if ( NOT subsurface_b.has_shading_overhang ) AND ( NOT subsurface_b.has_shading_sidefins ): PASS`

            - Case 2: Else: `else: FAIL and raise_warning "BASELINE FENESTRATION WAS MODELED WITH SHADING PROJECTIONS AND/OR OVERHANGS, WHICH IS INCORRECT."`

**[Back](../_toc.md)**
