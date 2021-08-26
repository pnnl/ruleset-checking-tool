
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

  1. get_overall_building_segment_wwr()  
  2. data_lookup()  
  3. match_data_element()

## Rule Logic:  

- Get window wall ratio dictionary for B_RMR: `building_wwr_dictionary_b = get_overall_building_segment_wwr(B_RMR)`

- Get window wall ratio dictionary for P_RMR: `building_wwr_dictionary_p = get_overall_building_segment_wwr(P_RMR)`

- For each building segment in the Baseline model: `for building_segment_b in B_RMR.building.building_segments:`

  - Check if building segment area type is not included in Table G3.1.1-1: `if NOT data_lookup(table_G3_1_1_1, building_segment_b.area_type_vertical_fenestration):`

    - Get matching building segment from P_RMR: `building_segment_p = match_data_element(P_RMR, BuildingSegments, building_segment_b.id)`

      **Rule Assertion:**

      - Case 1: If building segment window-wall-ratio is equal to that in P_RMR or 40%, whichever is smaller: `if building_wwr_dictionary_b[building_segment_b.id] == min(building_wwr_dictionary_p(building_segment_p.id), 0.4): PASS`

      - Case 2: Else: `else: FAIL and raise_warning "BASELINE BUILDING SEGMENT AREA TYPE IS NOT INCLUDED IN TABLE G3.1.1-1. BUT BUILDING SEGMENT WINDOW-WALL-RATIO DOES NOT EQUAL TO THAT IN P_RMR OR 40%, WHICHEVER IS SMALLER. CHECK IF BUILDING SEGMENT HAS EXISTING OR ALTERED ENVELOPE THAT CAN BE EXCLUDED FROM THE WINDOW-WALL-RATIO CALCULATION."`

**[Back](../_toc.md)**
