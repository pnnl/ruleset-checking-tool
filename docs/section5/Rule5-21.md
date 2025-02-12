
# Envelope - Rule 5-21  

**Rule ID:** 5-21  
**Rule Description:** Subsurface that is not regulated (not part of building envelope) must be modeled with the same area, U-factor and SHGC in the baseline as in the proposed design.  
**Rule Assertion:** B-RMD Fenestration: U-Factor, SHGC, glazed_area, fenestration.opaque_area = P-RMD SFenestration: U-Factor, SHGC, glazed_area, fenestration.opaque_area  
**Appendix G Section:** Section G3.1-1(a) Building Modeling Requirements for the Baseline building  
**Appendix G Section Reference:**  None  

**Applicability:** All required data elements exist for B_RMD  
**Applicability Checks:** None  

**Manual Checks:** None  
**Evaluation Context:**  Each Data Element  
**Data Lookup:** None  
**Function Call:**  

  1. match_data_element()
  2. get_more_stringent_surface_conditioning_category()

## Rule Logic:

- Get surface conditioning category dictionary for B_RMD: `scc_dictionary_b = get_surface_conditioning_category(B_RMD, P_RMD)`

- For each building segment in the Baseline model: `for building_segment_b in B_RMD.building.building_segments:`

  - For each zone in thermal block: `for zone_b in building_segment_b.zones:`

    - For each surface in zone: `for surface_b in zone_b.surfaces:`

      - Check if surface is unregulated: `if scc_dictionary_b[surface_b.id] == "UNREGULATED":`

        - For each subsurface in surface: `for subsurface_b in surface_b:`

          - Get matching subsurface in P_RMD: `subsurface_p = match_data_element(P_RMD, Subsurfaces, subsurface_b.id)`

            **Rule Assertion:**

            - Case 1: For each subsurface in B_RMD, if subsurface U-factor, SHGC, glazed area and opaque area is equal to that in P_RMD: `if ( subsurface_b.u_factor == subsurface_p.u_factor ) AND ( subsurface_b.solar_heat_gain_coefficient == subsurface_p.solar_heat_gain_coefficient ) AND ( subsurface_b.glazed_area == subsurface_p.glazed_area ) AND ( surface_b.opaque_area == surface_p.opaque_area ): PASS`

            - Case 2: Else: `else: FAIL and raise_warning "SUBSURFACE THAT IS NOT REGULATED (NOT PART OF BUILDING ENVELOPE) IS NOT MODELED WITH THE SAME AREA, U-FACTOR AND SHGC IN THE BASELINE AS IN THE PROPOSED DESIGN."`

**Notes:**

1. Update Rule ID from 5-28 to 5-21 on 10/26/2023

**[Back](../_toc.md)**
