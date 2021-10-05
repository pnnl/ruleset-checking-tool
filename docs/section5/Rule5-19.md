
# Envelope - Rule 5-19  

**Rule ID:** 5-19  
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

  1. get_building_segment_window_wall_areas()  
  2. data_lookup()  
  3. match_data_element()

## Rule Logic:  

- Get window wall areas dictionary for B_RMR: `window_wall_areas_dictionary_b = get_building_segment_window_wall_areas(B_RMR)`

- Get window wall areas dictionary for P_RMR: `window_wall_areas_dictionary_p = get_building_segment_window_wall_areas(P_RMR)`

- For each building segment in the Baseline model: `for building_segment_b in B_RMR.building.building_segments:`

  - Check if building segment area type is not included in Table G3.1.1-1: `if NOT data_lookup(table_G3_1_1_1, building_segment_b.area_type_vertical_fenestration):`

    - Calculate building segment window wall ratio: `building_segment_wwr_b = window_wall_areas_dictionary_b[building_segment_b][0] / window_wall_areas_dictionary_b[building_segment_b][1]`

    - Get matching building segment in P_RMR: `building_segment_p = match_data_element(P_RMR, BuildingSegments, building_segment_b.id)`

      - Calculate building segment window wall ratio in P_RMR: `building_segment_wwr_p = window_wall_areas_dictionary_p[building_segment_p][0] / window_wall_areas_dictionary_p[building_segment_p][1]`

      **Rule Assertion:**

      - Case 1: If building is all new and building segment window-wall-ratio is equal to that in P_RMR or 40%, whichever is smaller: `if ( B_RMR.building.is_all_new ) AND ( building_segment_wwr_b == min(building_segment_wwr_p, 0.4) ): PASS`

      - Case 2: Else if building is all new and building segment window-wall-ratio is not equal to that in P_RMR or 40%, whichever is smaller: `if ( B_RMR.building.is_all_new ) AND ( building_segment_wwr_b != min(building_segment_wwr_p, 0.4) ): FAIL`

      - Case 3: Else if building is not all new and building segment window-wall-ratio is equal to that in P_RMR or 40%, whichever is smaller: `if ( NOT B_RMR.building.is_all_new ) AND ( building_segment_wwr_b == min(building_segment_wwr_p, 0.4) ): CAUTION and raise_warning "BUILDING IS NOT ALL NEW AND BASELINE WWR MATCHES THE SMALLER OF PROPOSED DESIGN WWR OR 40%. HOWEVER, THIS RULE DOES NOT APPLY TO THE EXISTING ENVELOPE PER TABLE G3.1 BASELINE COLUMN #5 (C). FOR EXISTING ENVELOPE, THE BASELINE FENESTRATION AREA MUST EQUAL THE EXISTING FENESTRATION AREA PRIOR TO THE PROPOSED WORK. A MANUAL CHECK IS REQUIRED TO VERIFY COMPLIANCE."`

      - Case 4: Else, building is not all new and building segment window-wall-ratio is not equal to that in P_RMR or 40%, whichever is smaller: `if ( NOT B_RMR.building.is_all_new ) AND ( building_segment_wwr_b != min(building_segment_wwr_p, 0.4) ): CAUTION and raise_warning "BUILDING IS NOT ALL NEW AND BASELINE WWR DOES NOT MATCH THE SMALLER OF PROPOSED DESIGN WWR OR 40%. HOWEVER, THIS RULE DOES NOT APPLY TO THE EXISTING ENVELOPE PER TABLE G3.1 BASELINE COLUMN #5 (C). FOR EXISTING ENVELOPE, THE BASELINE FENESTRATION AREA MUST EQUAL THE EXISTING FENESTRATION AREA PRIOR TO THE PROPOSED WORK. A MANUAL CHECK IS REQUIRED TO VERIFY COMPLIANCE."`

**[Back](../_toc.md)**
