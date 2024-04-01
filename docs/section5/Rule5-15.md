
# Envelope - Rule 5-15  

**Rule ID:** 5-15  
**Rule Description:** For building areas not shown in Table G3.1.1-1, vertical fenestration areas for new buildings and additions shall equal that in the proposed design or 40% of gross above-grade wall area, whichever is smaller.  
**Rule Assertion:** Baseline RMR = expected value  
**Appendix G Section:** Section G3.1-5(c) Building Envelope Modeling Requirements for the Baseline building  
**Appendix G Section Reference:**  

- Table G3.1-5. Building Envelope, Baseline Building Performance, c. Vertical Fenestration Areas  
- Table G3.1.1-1  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:** None  

**Manual Checks:** None  
**Evaluation Context:**  Each Data Element  
**Data Lookup:** Table G3.1.1-1
**Function Call:**  

  1. get_area_type_window_wall_areas()  
  2. data_lookup()  
  3. match_data_element()

## Rule Logic:  

- Get window wall areas dictionary for B_RMR: `window_wall_areas_dictionary_b = get_area_type_window_wall_areas(B_RMR)`

- Get window wall areas dictionary for P_RMR: `window_wall_areas_dictionary_p = get_area_type_window_wall_areas(P_RMR)`

- For each building segment in B_RMR: `for building_segment_b in B_RMR...building_segments:`

  - Check if building segment area type is not included in Table G3.1.1-1: `if ( NOT building_segment_b.area_type_vertical_fenestration in table_G_3_1_1_1 ):`

    - Check if building segment is not all new, set manual_check_flag: `if NOT building_segment_b.is_all_new: manual_check_flag = TRUE`

**Rule Assertion:**

- Case 1: If all building segments with building areas not shown in Table G3.1.1-1 are new, and the total window-wall-ratio is equal to that in P_RMR or 40%, whichever is smaller: `if ( NOT manual_check_flag ) AND ( window_wall_areas_dictionary_b["OTHER"]["total_window_area"]/window_wall_areas_dictionary_b["OTHER"]["total_wall_area"] == min(window_wall_areas_dictionary_p["OTHER"]["total_window_area"]/window_wall_areas_dictionary_p["OTHER"]["total_wall_area"], 0.4) ): PASS`

- Case 2: Else if all building segments with building areas not shown in Table G3.1.1-1 are new, and the total window-wall-ratio is not equal to that in P_RMR or 40%, whichever is smaller: `if ( NOT manual_check_flag ) AND ( window_wall_areas_dictionary_b["OTHER"]["total_window_area"]/window_wall_areas_dictionary_b["OTHER"]["total_wall_area"] != min(window_wall_areas_dictionary_p["OTHER"]["total_window_area"]/window_wall_areas_dictionary_p["OTHER"]["total_wall_area"], 0.4) ): FAIL`

- Case 3: Else if any building segments with building areas not shown in Table G3.1.1-1 is not new, and the total window-wall-ratio is equal to that in P_RMR or 40%, whichever is smaller: `if ( manual_check_flag ) AND ( window_wall_areas_dictionary_b["OTHER"]["total_window_area"]/window_wall_areas_dictionary_b["OTHER"]["total_wall_area"] == min(window_wall_areas_dictionary_p["OTHER"]["total_window_area"]/window_wall_areas_dictionary_p["OTHER"]["total_wall_area"], 0.4) ): UNDETERMINED and raise_message "BUILDING IS NOT ALL NEW AND BASELINE WWR MATCHES THE SMALLER OF PROPOSED DESIGN WWR OR 40%. HOWEVER, THIS RULE DOES NOT APPLY TO THE EXISTING ENVELOPE PER TABLE G3.1 BASELINE COLUMN #5 (C). FOR EXISTING ENVELOPE, THE BASELINE FENESTRATION AREA MUST EQUAL THE EXISTING FENESTRATION AREA PRIOR TO THE PROPOSED WORK. A MANUAL CHECK IS REQUIRED TO VERIFY COMPLIANCE."`

- Case 4: Else, some building segments with building areas not shown in Table G3.1.1-1 is not new, and the total window-wall-ratio is not equal to that in P_RMR or 40%, whichever is smaller: `if ( manual_check_flag ) AND ( window_wall_areas_dictionary_b["OTHER"]["total_window_area"]/window_wall_areas_dictionary_b["OTHER"]["total_wall_area"] != min(window_wall_areas_dictionary_p["OTHER"]["total_window_area"]/window_wall_areas_dictionary_p["OTHER"]["total_wall_area"], 0.4) ): UNDETERMINED and raise_message "BUILDING IS NOT ALL NEW AND BASELINE WWR DOES NOT MATCH THE SMALLER OF PROPOSED DESIGN WWR OR 40%. HOWEVER, THIS RULE DOES NOT APPLY TO THE EXISTING ENVELOPE PER TABLE G3.1 BASELINE COLUMN #5 (C). FOR EXISTING ENVELOPE, THE BASELINE FENESTRATION AREA MUST EQUAL THE EXISTING FENESTRATION AREA PRIOR TO THE PROPOSED WORK. A MANUAL CHECK IS REQUIRED TO VERIFY COMPLIANCE."`

**Notes:**

1. Update Rule ID from 5-19 to 5-15 on 10/26/2023

**[Back](../_toc.md)**
