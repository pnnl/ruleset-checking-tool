
# Envelope - Rule 5-17  

**Rule ID:** 5-17  
**Rule Description:** Opaque surfaces that are not regulated (not part of opaque building envelope) must be modeled the same in the baseline as in the proposed design.  
**Appendix G Section:** Section G3.1-5 Building Envelope Modeling Requirements for the Baseline building  
**Appendix G Section Reference:** None  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:** None  

**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  
**Function Call:**

  - get_surface_conditioning_category()
  - get_opaque_surface_type()
  - match_data_element()

## Rule Logic:  

- Get surface conditioning category dictionary for B_RMR: `scc_dictionary_b = get_surface_conditioning_category(B_RMR)`  

- For each building segment in the Proposed model: `for building_segment_b in B_RMR.building.building_segments:`  

  - For each zone in thermal block: `for zone_b in building_segment_b.zones:`  

    - For each surface in zone: `for surface_b in zone_b.surfaces:`  

      - Check if surface is unregulated: `if ( scc_dictionary_b[surface_b.id] == UNREGULATED ):`  

        - Get surface type: `surface_type_b = get_opaque_surface_type(surface_b)`

        - Get matching surface from P_RMR: `surface_p = match_data_element(P_RMR, surfaces, surface_b.id)`  

          **Rule Assertion:**  

          - Case 1: If surface type is roof, floor or above-grade wall, and surface construction U-factor in B_RMR matches P_RMR: `if ( surface_type_b in ["ROOF", "FLOOR", "ABOVE-GRADE WALL"] ) AND ( surface_b.construction.u_factor == surface_p.construction.u_factor ): PASS`

          - Case 2: Else if surface type is heated slab-on-grade or unheated slab-on-grade, and surface construction F-factor in B_RMR matches P_RMR: `if ( surface_type_b in ["HEATED SLAB-ON-GRADE", "UNHEATED SLAB-ON-GRADE"] ) AND ( surface_b.construction.f_factor == surface_p.construction.f_factor ): PASS`

          - Case 3: Else if surface type is below-grade wall, and surface construction C-factor in B_RMR matches P_RMR: `if ( surface_type_b =="BELOW-GRADE WALL" ) AND ( surface_b.construction.c_factor == surface_p.construction.c_factor ): PASS`

          - Case 4: Else: `else: FAIL`

