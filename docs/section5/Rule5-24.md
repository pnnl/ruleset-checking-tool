
# Envelope - Rule 5-24  

**Rule ID:** 5-24  
**Rule Description:** If skylight area in the proposed design is 3% or less of the roof surface, the skylight area in baseline shall be equal to that in the proposed design.  
**Rule Assertion:** B-RMD total (subsurface.glazed_area+subsurface.opaque_area) = expected value  
**Appendix G Section:** Section G3.1-5(e) Building Envelope Modeling Requirements for the Baseline building  
**Appendix G Section Reference:** None  

**Applicability:** All required data elements exist for B_RMD
**Applicability Checks:**  
1. the skylight area in the proposed design is 3% or less.

**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  
**Function Call:**  

  1. get_building_segment_skylight_roof_areas()  
  2. match_data_element()

## Rule Logic:

- Get building skylight roof areas dictionary for B_RMD: `skylight_roof_areas_dictionary_b = get_building_segment_skylight_roof_areas(B_RMD)`

- Get building skylight roof areas dictionary for P_RMD: `skylight_roof_areas_dictionary_p = get_building_segment_skylight_roof_areas(P_RMD)`

- For each building segment in B_RMD: `for building_segment_b in B_RMD.building.building_segments:`  

  - Calculate skylight roof ratio for building segment: `skylight_roof_ratio_b = skylight_roof_areas_dictionary_b[building_segment_b.id][total_skylight_area] / skylight_roof_areas_dictionary_b[building_segment_b.id][total_envelope_roof_area]`

  - Get matching building segment in P_RMD: `building_segment_p = match_data_element(P_RMD, BuildingSegments, building_segment_b.id)`

    - Calculate skylight roof ratio of all building_segments in P_RMD: `skylight_roof_ratio_p = sum(skylight_roof_building_segment_p[total_skylight_area] for skylight_roof_building_segment_p in skylight_roof_areas_dictionary_b) / sum(skylight_roof_building_segment_p[total_envelope_roof_area] for skylight_roof_building_segment_p in skylight_roof_areas_dictionary_b)`

    - Check if skylight roof ratio in P_RMD is 3% or less: `if skylight_roof_ratio_p <= 0.03:`
    
    - if skylight roof ratio in P_RMD is greater than 3%, Rule is not applicable: `else: NOT_APPLICABLE` 

      **Rule Assertion:** 

      - Case 1: For each building segment in B_RMD, the skylight to roof ratio is equal to that in P_RMD: `if skylight_roof_ratio_b == skylight_roof_ratio_p: PASS`  

      - Case 2: Else: `Else: FAIL`


**Notes:**

1. Update Rule ID from 5-34 to 5-24 on 10/26/2023

**[Back](../_toc.md)