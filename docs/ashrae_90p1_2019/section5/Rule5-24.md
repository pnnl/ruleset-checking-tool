
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
**Evaluation Context:** Each Building  
**Data Lookup:** None  
**Function Call:**  

  1. get_building_segment_skylight_roof_areas()  
  2. match_data_element()

## Rule Logic:
- For each building in the baseline model: `for building_b in B_RMD...buildings:`
  
  - Get the associated building in the proposed model: `building_p = match_data_element(P_RMD, Buildings, building_b.id)`

  - Get building skylight roof areas dictionary for the baseline building: `skylight_roof_areas_dictionary_b = get_building_segment_skylight_roof_areas(building_b)`

  - Get building skylight roof areas dictionary for the proposed building: `skylight_roof_areas_dictionary_p = get_building_segment_skylight_roof_areas(building_p)`

  - Calculate skylight to roof ratio for the baseline building: `skylight_roof_ratio_b = sum(area["total_skylight_area"] for area in skylight_roof_areas_b.values()) / sum(area["total_envelope_roof_area"] for area in skylight_roof_areas_b.values())`

  - Calculate skylight to roof ratio for the proposed building: `skylight_roof_ratio_p = sum(area["total_skylight_area"] for area in skylight_roof_areas_p.values()) / sum(area["total_envelope_roof_area"] for area in skylight_roof_areas_p.values())`

  - Check if skylight roof ratio in the proposed building is 3% or less: `if skylight_roof_ratio_p <= 0.03:`

    - If so, then this rule is applicable: `CONTINUE TO RULE ASSERTION`
    
    - If skylight roof ratio in the proposed building is greater than 3%, Rule is not applicable: `else: NOT_APPLICABLE` 

  **Rule Assertion:** 

  - Case 1: The skylight to roof ratio is equal to that in the proposed: `if skylight_roof_ratio_b == skylight_roof_ratio_p: PASS`  

  - Case 2: Else: `Else: FAIL`


**Notes:**

1. Update Rule ID from 5-34 to 5-24 on 10/26/2023

**[Back](../_toc.md)