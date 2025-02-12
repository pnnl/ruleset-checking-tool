
# Envelope - Rule 5-16  

**Rule ID:** 5-16  
**Rule Description:** The vertical fenestration shall be distributed on each face of the building in the same proportion as in the proposed design.  
**Rule Assertion:** B-RMD total (subsurface.glazed_area+subsurface.opaque_area) = expected value for each surface  
**Appendix G Section:** Section 5 Envelope  
**Appendix G Section Reference:**  Section G3.1-5(c) Building Envelope Modeling Requirements for the Baseline building

**Applicability:** All required data elements exist for B_RMD  
**Applicability Checks:** None  

**Manual Checks:** None  
**Evaluation Context:**  Each Data Element  
**Data Lookup:** None  
**Function Call:**  

  1. get_area_type_window_wall_areas()  
  2. match_data_element()
  3. get_opaque_surface_type()
  4. get_more_stringent_surface_conditioning_category()

## Rule Logic:

- Get area type window wall areas dictionary for B_RMD: `window_wall_areas_dictionary_b = get_area_type_window_wall_areas(B_RMD)`

  - For each area type in window wall areas dictionary: `for area_type_b in window_wall_areas_dictionary_b.keys():`
  
    - Calculate total fenestration area for B_RMD: `total_fenestration_area_b += window_wall_areas_dictionary_b[area_type_b]["TOTAL_WINDOW_AREA"]`

- Get area type window wall areas dictionary for P_RMD: `window_wall_areas_dictionary_p = get_area_type_window_wall_areas(P_RMD)`

  - For each area type in window wall areas dictionary: `for area_type_p in window_wall_areas_dictionary_p.keys():`
  
    - Calculate total fenestration area for B_RMD: `total_fenestration_area_p += window_wall_areas_dictionary_p[area_type_p]["TOTAL_WINDOW_AREA"]`

- Get surface conditioning category dictionary for B_RMD: `scc_dictionary_b = get_more_stringent_surface_conditioning_category(B_RMD, P_RMD)`

- For each building segment in the Baseline model: `For building_segment_b in B_RMD.building.building_segments:`

  - For each zone in building segment: `for zone_b in building_segment_b...zones:`

    - For each surface in zone: `for surface_b in zone_b.surfaces:`

      - Check if surface is above-grade wall and is regulated: `if ( get_opaque_surface_type(surface_b.id) == "ABOVE-GRADE WALL" ) AND ( scc_dictionary_b[surface_b.id] != "UNREGULATED" ):`

        - For each subsurface in surface: `for subsurface_b in surface_b.subsurfaces:`

          - Check if subsurface is door, and if the glazed vision area is more than 50% of the total area, add subsurface total area to surface total fenestration area: `if ( subsurface_b.classification == "DOOR" ) AND ( subsurface_b.glazed_area > subsurface_b.opaque_area ): total_fenestration_area_surface_b += subsurface_b.glazed_area + subsurface_b.opaque_area`  

          - Else if subsurface is not door, add total subsurface area to surface total fenestration area: `else if subsurface_b.classification != "DOOR" : total_fenestration_area_surface_b += subsurface_b.glazed_area + subsurface_b.opaque_area`

        - Get matching surface in P_RMD: `surface_p = match_data_element(P_RMD, Surfaces, surface_b.id)`

          - For each subsurface in surface: `for subsurface_p in surface_p.subsurfaces:`

            - Check if subsurface is door, and if the glazed vision area is more than 50% of the total area, add subsurface total area to surface total fenestration area: `if ( subsurface_p.classification == "DOOR" ) AND ( subsurface_p.glazed_area > subsurface_p.opaque_area ): total_fenestration_area_surface_p += subsurface_p.glazed_area + subsurface_p.opaque_area`

            - Else if subsurface is not door, add total subsurface area to surface total fenestration area: `else if subsurface_p.classification != "DOOR" : total_fenestration_area_surface_p += surface_p.glazed_area + surface_p.opaque_area`

          **Rule Assertion:**

          - Case 1: For each surface, if total fenestration area in B_RMD is in the same proportion as in P_RMD: `if total_fenestration_area_surface_b / total_fenestration_area_b == total_fenestration_area_surface_p / total_fenestration_area_p: PASS`

          - Case 2: Else: `else: FAIL and show_message "THE VERTICAL FENESTRATION IS NOT DISTRIBUTED ACROSS BASELINE OPAQUE SURFACES IN THE SAME PROPORTION AS IN THE PROPOSED DESIGN. VERIFY IF ENVELOPE IS EXISTING OR ALTERED AND CAN BE EXCLUDED FROM THIS CHECK."`


**Notes:**

1. Update Rule ID from 5-21 to 5-17 on 10/26/2023
2. Update Rule ID from 5-17 to 5-16 on 12/22/2023

**[Back](../_toc.md)**


