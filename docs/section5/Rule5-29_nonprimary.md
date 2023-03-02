# Envelope - Rule 5-29  
**Schema Version** 0.0.23  
**Primary Rule:** False
**Rule ID:** 5-29  
**Rule Description:** Baseline fenestration shall be assumed to be flush with the exterior wall, and no shading projections shall be modeled.
**Appendix G Section:** Section G3.1-5(d) Building Modeling Requirements for the Baseline building  
**Appendix G Section Reference:**  None  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:** None  

**Evaluation Context:**  Each Data Element  
**Data Lookup:** None  
**Function Call:**
  1. get_opaque_surface_type()
  2. get_surface_conditioning_category()

## Rule Logic:

- Get surface conditioning category dictionary for B_RMR: ```scc_dictionary_b = get_surface_conditioning_category(B_RMR)```

- For each building segment in the Baseline model: ```for building_segment_b in B_RMR.building.building_segments:```

  - For each zone in building segment: ```for zone_b in building_segment_b.zones:```

    - For each space in zone: ```for space_b in zone_b.spaces:```

      - For each surface in space: ```for surface_b in space_b.surfaces:```

        - Check if surface is above-grade wall or roof and is exterior: ```if ( get_opaque_surface_type(surface_b) == "ABOVE-GRADE WALL" ) AND ( scc_dictionary_b[surface_b.id] != "UNREGULATED" ):```

          - For each subsurface in surface: ```for subsurface_b in surface_b.subsurfaces:```

            **Rule Assertion:**

            - Case 1: For each subsurface, if subsurface is flush with the exterior wall, and no shading projections are modeled, outcome is PASS: ```if ( NOT subsurface_b.has_shading_overhang ) AND ( NOT subsurface_b.has_shading_sidefins ): outcome = PASS```

            - Case 2: Else, outcome is FAIL: ```else: outcome = FAIL and raise_warning "BASELINE FENESTRATION WAS MODELED WITH SHADING PROJECTIONS AND/OR OVERHANGS, WHICH IS INCORRECT."```

**[Back](../_toc.md)**
