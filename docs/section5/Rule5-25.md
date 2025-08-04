
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
**Evaluation Context:** Each Building   
**Data Lookup:** None  
**Function Call:**  

  1. get_building_segment_skylight_roof_areas()  
  2. match_data_element()

## Rule Logic:

- For each building in the baseline model: `for building_b in B_RMD...buildings:`
  
  - Get the associated building in the proposed model: `building_p = match_data_element(P_RMD, Buildings, building_b.id)`
  
  - Get skylight roof areas dictionary for the baseline building: `skylight_roof_areas_dictionary_b = get_building_segment_skylight_roof_areas(building_b)`

  - Get skylight roof areas dictionary for the proposed building: `skylight_roof_areas_dictionary_p = get_building_segment_skylight_roof_areas(building_p)`

  - Calculate skylight to roof ratio for the baseline building: `skylight_roof_ratio_b = sum(area["total_skylight_area"] for area in skylight_roof_areas_b.values()) / sum(area["total_envelope_roof_area"] for area in skylight_roof_areas_b.values())`

  - Calculate skylight to roof ratio for the proposed building: `skylight_roof_ratio_p = sum(area["total_skylight_area"] for area in skylight_roof_areas_p.values()) / sum(area["total_envelope_roof_area"] for area in skylight_roof_areas_p.values())`

  - Check if skylight roof ratio in the proposed building is greater than 3%: `if skylight_roof_ratio_p > 0.03:`

    - If so, then this rule is applicable: `CONTINUE TO RULE ASSERTION`
    
    - If skylight roof ratio in the proposed building is less than or equal to 3%, Rule is not applicable: `else: NOT_APPLICABLE`

  **Rule Assertion:**

  - Case 1: The skylight to roof ratio is equal to 3%: `if skylight_roof_ratio_b == 0.03: PASS`  

  - Case 2: Else: `Else: FAIL`

**Notes:**

1. Update Rule ID from 5-35 to 5-25 on 10/26/2023


**[Back](../_toc.md)**
