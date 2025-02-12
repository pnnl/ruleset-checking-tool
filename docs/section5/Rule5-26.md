
# Envelope - Rule 5-26  

**Rule ID:** 5-26  
**Rule Description:**  Skylight area must be allocated to surfaces in the same proportion in the baseline as in the proposed design.  
**Rule Assertion:** B-RMD (subsurface.glazed_area+subsurface.opaque_area) = expected value for each zone  
**Appendix G Section:** Section G3.1-5(e) Building Envelope Modeling Requirements for the Baseline building  
**Appendix G Section Reference:** None  

**Applicability:** All required data elements exist for B_RMD  
**Applicability Checks:**  None  

**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  
**Function Call:**  

  1. get_building_segment_skylight_roof_areas()  
  2. get_more_stringent_surface_conditioning_category()
  3. get_opaque_surface_type()
  4. match_data_element()

## Rule Logic:

- Get building segment skylight roof areas dictionary for B_RMD: `skylight_roof_areas_dictionary_b = get_building_segment_skylight_roof_areas(B_RMD)`

- Get building segment skylight roof areas dictionary for P_RMD: `skylight_roof_areas_dictionary_p = get_building_segment_skylight_roof_areas(P_RMD)`

- Get surface conditioning category dictionary for B_RMD: `scc_dictionary_b = get_more_stringent_surface_conditioning_category(B_RMD, P_RMD)`  

- For each building segment in the Baseline model: `For building_segment_b in B_RMD.building.building_segments:`

  - Get total skylight area for building segment: `total_skylight_area_b = skylight_roof_areas_dictionary_b[building_segment_b.id][0]`

  - Get matching building segment in P_RMD: `building_segment_p = match_data_element(P_RMD, BuildingSegments, building_segment_b.id)`
  
    - Get total skylight area for building segment in P_RMD: `total_skylight_area_p = skylight_roof_areas_dictionary_p[building_segment_p.id][0]`

  - For each zone in building segment: `for zone_b in building_segment_b.zones:`
  
    - For each surface in zone: `for surface_b in zone_b.surfaces:`  

      - Check if surface is roof and is regulated: `if ( get_opaque_surface_type(surface_b.id) == "ROOF" ) AND ( scc_dictionary_b[surface_b.id] != "UNREGULATED" ):`

        - Add total skylight area to roof total skylight area: `total_skylight_area_surface_b = sum(subsurface.glazed_area + subsurface.opaque_area for subsurface in surface_b.subsurfaces)`

        - Get matching surface in P_RMD: `surface_p = match_data_element(P_RMD, Surfaces, surface_b.id)`

          - Add total skylight area to roof total skylight area in P_RMD: `total_skylight_area_surface_p = sum(subsurface.glazed_area + subsurface.opaque_area for subsurface in surface_p.subsurfaces)`

          **Rule Assertion:**

          - Case 1: For each surface, if total skylight area in B_RMD is in the same proportion as in P_RMD: `if total_skylight_area_surface_b / total_skylight_area_b == total_skylight_area_surface_p / total_skylight_area_p: PASS`

          - Case 2: Else: `else: FAIL`

**Notes:**

1. Update Rule ID from 5-36 to 5-26 on 10/26/2023


**[Back](../_toc.md)
