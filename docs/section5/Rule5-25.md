
# Envelope - Rule 5-25  

**Rule ID:** 5-25  
**Rule Description:**  If the skylight area of the proposed design is greater than 3%, baseline skylight area shall be decreased in all roof components in which skylights are located to reach 3%.  
**Rule Assertion:** B-RMD total (subsurface.glazed_area+subsurface.opaque_area) = expected value for each zone  
**Appendix G Section:** Section G3.1-5(e) Building Envelope Modeling Requirements for the Baseline building  
**Appendix G Section Reference:** None  

**Applicability:** All required data elements exist for B_RMD  
**Applicability Checks:**
1. the skylight area in the proposed design is 3% or greater.  

**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  
**Function Call:**  

  1. get_building_segment_skylight_roof_areas()  
  2. match_data_element()

## Rule Logic:

- Get skylight roof areas dictionary for B_RMD: `skylight_roof_areas_dictionary_b = get_building_segment_skylight_roof_areas(B_RMD)`

- Get skylight roof areas dictionary for P_RMD: `skylight_roof_areas_dictionary_p = get_building_segment_skylight_roof_areas(P_RMD)`

- For each building segment in B_RMD: `for building_segment_b in B_RMD.building.building_segments:`

  - Calculate skylight roof ratio for building segment: `skylight_roof_ratio_b = skylight_roof_areas_dictionary_b[building_segment_b.id]["total_skylight_area"] / skylight_roof_areas_dictionary_b[building_segment_b.id]["total_envelope_roof_area"]`

  - Get matching building segment in P_RMD: `building_segment_p = match_data_element(P_RMD, BuildingSegments, building_segment_b.id)`

    - Calculate skylight roof ratio for building segment in P_RMD: `skylight_roof_ratio_p = skylight_roof_areas_dictionary_p[building_segment_p.id][0] / skylight_roof_areas_dictionary_p[building_segment_p.id][1]`

      - Check if skylight roof ratio in P_RMD is greater than 3%: `if skylight_roof_ratio_p > 0.03:`

        **Rule Assertion:**

        - Case 1: For each building segment in B_RMD, the skylight to roof ratio is equal to 3%: `if skylight_roof_ratio_b == 0.03: PASS`  

        - Case 2: Else: `Else: FAIL`

**Notes:**

1. Update Rule ID from 5-35 to 5-25 on 10/26/2023


**[Back](../_toc.md)**
