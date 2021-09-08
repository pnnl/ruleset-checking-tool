
# Envelope - Rule 5-18  

**Rule ID:** 5-18  
**Rule Description:** For building area types included in Table G3.1.1-1, vertical fenestration areas for new buildings and additions shall equal that in Table G3.1.1-1 based on the area of gross above-grade walls that separate conditioned spaces and semi-heated spaces from the exterior.  
**Rule Assertion:** B-RMR total (subsurface.glazed_area+subsurface.opaque_area) = expected value  
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

## Rule Logic:  

- Get window wall areas dictionary for building: `window_wall_areas_dictionary_b = get_building_segment_window_wall_areas(B_RMR)`

- For each building segment in the Baseline model: `for building_segment_b in B_RMR.building.building_segments:`

  - Check if building segment area type is included in Table G3.1.1-1: `if data_lookup(table_G3_1_1_1, building_segment_b.area_type_vertical_fenestration):`

    - Calculate building segment window wall ratio: `building_segment_wwr_b = window_wall_areas_dictionary_b[building_segment_b.id][0] / window_wall_areas_dictionary_b[building_segment_b.id][1]`

      **Rule Assertion:**

      - Case 1: If building is all new and building segment window-wall-ratio matches Table G3.1.1-1 allowance: `if ( B_RMR.building.is_all_new ) AND ( building_segment_wwr_b == data_lookup(table_G3_1_1_1, building_segment_b.area_type_vertical_fenestration) ): PASS`

      - Case 2: Else if building is all new and building segment window-wall-ratio does not match Table G3.1.1-1 allowance: `if ( B_RMR.building.is_all_new ) AND ( building_segment_wwr_b != data_lookup(table_G3_1_1_1, building_segment_b.area_type_vertical_fenestration) ): FAIL`

      - Case 3: Else if building is not all new and building segment window-wall-ratio matches Table G3.1.1-1 allowance: `if ( NOT B_RMR.building.is_all_new ) AND ( building_segment_wwr_b == data_lookup(table_G3_1_1_1, building_segment_b.area_type_vertical_fenestration) ): CAUTION and raise_warning "BUILDING IS NOT ALL NEW AND BASELINE WWR MATCHES VALUES PRESCRIBED IN TABLE G3.1.1-1. HOWEVER, THE FENESTRATION AREA PRESCRIBED IN TABLE G3.1.1-1 DOES NOT APPLY TO THE EXISTING ENVELOPE PER TABLE G3.1 BASELINE COLUMN #5 (C). FOR EXISTING ENVELOPE, THE BASELINE FENESTRATION AREA MUST EQUAL THE EXISTING FENESTRATION AREA PRIOR TO THE PROPOSED WORK. A MANUAL CHECK IS REQUIRED TO VERIFY COMPLIANCE."`

      - Case 4: Else, building is not all new and building segment window-wall-ratio does not match Table G3.1.1-1 allowance: `if ( NOT B_RMR.building.is_all_new ) AND ( building_segment_wwr_b != data_lookup(table_G3_1_1_1, building_segment_b.area_type_vertical_fenestration) ): CAUTION and raise_warning "BUILDING IS NOT ALL NEW AND BASELINE WWR DOES NOT MATCH VALUES PRESCRIBED IN TABLE G3.1.1-1. HOWEVER, THE FENESTRATION AREA PRESCRIBED IN TABLE G3.1.1-1 DOES NOT APPLY TO THE EXISTING ENVELOPE PER TABLE G3.1 BASELINE COLUMN #5(c). FOR EXISTING ENVELOPE, THE BASELINE FENESTRATION AREA MUST EQUAL THE EXISTING FENESTRATION AREA PRIOR TO THE PROPOSED WORK. A MANUAL CHECK IS REQUIRED TO VERIFY COMPLIANCE."`

**[Back](../_toc.md)**
