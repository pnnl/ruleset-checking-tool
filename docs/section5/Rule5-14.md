
# Envelope - Rule 5-14  

**Rule ID:** 5-14  
**Rule Description:** For building area types included in Table G3.1.1-1, vertical fenestration areas for new buildings and additions shall equal that in Table G3.1.1-1 based on the area of gross above-grade walls that separate conditioned spaces and semi-heated spaces from the exterior.  
**Rule Assertion:** B-RMD total (subsurface.glazed_area+subsurface.opaque_area) = expected value  
**Appendix G Section:** Section 5 Envelope  
**Appendix G Section Reference:** Section G3.1-5(c) Building Envelope Modeling Requirements for the Baseline building  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:** None  

**Manual Checks:** Yes
**Evaluation Context:**  Each Data Element  
**Data Lookup:** Table G3.1.1-1  
**Function Call:**  

  1. get_area_type_window_wall_areas()
  2. data_lookup()  

## Rule Logic:  

- Get window wall areas dictionary for building: `window_wall_areas_dictionary_b = get_area_type_window_wall_areas(B_RMR)`

- For each building segment in the Baseline model: `for building_segment_b in B_RMR...building_segments:`

  - If area type has not been saved in is_area_type_all_new_dict, save building segment area type with its is_all_new flag  : `if NOT building_segment_b.area_type_vertical_fenestration in is_area_type_all_new_dict.keys(): `is_area_type_all_new_dict`[building_segment_b.area_type_vertical_fenestration] = building_segment_b.is_all_new`

  - Else if building segment is_all_new flag is FALSE, update is_area_type_all_new_dict: `else if NOT building_segment_b.is_all_new: is_area_type_all_new_dict[building_segment_b.area_type_vertical_fenestration] = building_segment_b.is_all_new`

- For each unique area type in building: `for area_type_b in window_wall_areas_dictionary_b.keys():`

  - Check if area type is in Table G3.1.1-1 besides OTHER, calculate window-wall-ratio: `if area_type_b != "OTHER": area_type_wwr = window_wall_areas_dictionary_b[area_type_b]["TOTAL_WINDOW_AREA"] / window_wall_areas_dictionary_b[area_type_b]["TOTAL_WALL_AREA"]`

  - Else area type is None ```manual_review_flag = TRUE```    

  - Check if any building segment related to area type is not new, set manual_check_flag: `if NOT is_area_type_all_new_dict[area_type_b]: manual_check_flag = TRUE`

    **Rule Assertion:**
  
    - Case 1: For each area type that is in Table G3.1.1-1, if all related building segments are new and area type window-wall-ratio matches Table G3.1.1-1 allowance: `if ( NOT manual_check_flag) AND ( area_type_wwr == data_lookup(table_G3_1_1_1, area_type_b) ): PASS`

    - Case 2: Else if all building segments in building are new and building segment window-wall-ratio does not match Table G3.1.1-1 allowance: `else if ( NOT manual_check_flag ) AND ( area_type_wwr != data_lookup(table_G3_1_1_1, area_type_b) ): FAIL`

    - Case 3: Else if any building segment in building is not new and area type window-wall-ratio matches Table G3.1.1-1 allowance: `else if ( manual_check_flag ) AND ( area_type_wwr == data_lookup(table_G3_1_1_1, area_type_b) ): UNDETERMINED and raise_message "BUILDING IS NOT ALL NEW AND BASELINE WWR MATCHES VALUES PRESCRIBED IN TABLE G3.1.1-1. HOWEVER, THE FENESTRATION AREA PRESCRIBED IN TABLE G3.1.1-1 DOES NOT APPLY TO THE EXISTING ENVELOPE PER TABLE G3.1 BASELINE COLUMN #5 (C). FOR EXISTING ENVELOPE, THE BASELINE FENESTRATION AREA MUST EQUAL THE EXISTING FENESTRATION AREA PRIOR TO THE PROPOSED WORK. A MANUAL CHECK IS REQUIRED TO VERIFY COMPLIANCE."`

    - Case 4: Else, some building segment in building is not new and building segment window-wall-ratio does not match Table G3.1.1-1 allowance: `else: UNDETERMINED and raise_message "BUILDING IS NOT ALL NEW AND BASELINE WWR DOES NOT MATCH VALUES PRESCRIBED IN TABLE G3.1.1-1. HOWEVER, THE FENESTRATION AREA PRESCRIBED IN TABLE G3.1.1-1 DOES NOT APPLY TO THE EXISTING ENVELOPE PER TABLE G3.1 BASELINE COLUMN #5(c). FOR EXISTING ENVELOPE, THE BASELINE FENESTRATION AREA MUST EQUAL THE EXISTING FENESTRATION AREA PRIOR TO THE PROPOSED WORK. A MANUAL CHECK IS REQUIRED TO VERIFY COMPLIANCE."`


**Notes:**

1. Update Rule ID from 5-18 to 5-14 on 10/26/2023

**[Back](../_toc.md)**
