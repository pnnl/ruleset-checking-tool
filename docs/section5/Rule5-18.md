
# Envelope - Rule 5-18  

**Rule ID:** 5-18  
**Rule Description:** For building area types included in Table G3.1.1-1, vertical fenestration areas for new buildings and additions shall equal that in Table G3.1.1-1 based on the area of gross above-grade walls that separate conditioned spaces and semi-heated spaces from the exterior.  
**Rule Assertion:** B-RMR total (subsurface.glazed_area+subsurface.opaque_area) = expected value  
**Appendix G Section:** Section 5 Envelope  
**Appendix G Section Reference:** Section G3.1-5(c) Building Envelope Modeling Requirements for the Baseline building  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:** None  

**Manual Checks:** None  
**Evaluation Context:**  Each Data Element  
**Data Lookup:** Table G3.1.1-1  
**Function Call:**  

  1. get_area_type_window_wall_areas()

## Rule Logic:  

- Get window wall areas dictionary for building: `window_wall_areas_dictionary_b = get_area_type_window_wall_areas(B_RMR)`

- For each building segment in the Baseline model: `for building_segment_b in B_RMR.building.building_segments:`

  - Check if building segment area type is included in Table G3.1.1-1, save building segment area type to array if not already saved: `if ( building_segment_b.area_type_vertical_fenestration ) AND ( building_segment_b.area_type_vertical_fenestration NOT in area_type_array_b ): area_type_array_b.append(building_segment_b.area_type_vertical_fenestration)`

- For each unique area type in building: `for area_type_b in area_type_array_b:`

  - Calculate area type window wall ratio: `area_type_wwr = window_wall_areas_dictionary_b[area_type_b]["TOTAL_WINDOW_AREA"] / window_wall_areas_dictionary_b[area_type_b]["TOTAL_WALL_AREA"]`

    **Rule Assertion:**

    - Case 1: For each area type in building, if building is all new and area type window-wall-ratio matches Table G3.1.1-1 allowance: `if ( B_RMR.building.is_all_new ) AND ( area_type_wwr == data_lookup(table_G3_1_1_1, area_type_b) ): PASS`

    - Case 2: Else if building is all new and building segment window-wall-ratio does not match Table G3.1.1-1 allowance: `if ( B_RMR.building.is_all_new ) AND ( area_type_wwr != data_lookup(table_G3_1_1_1, area_type_b) ): FAIL`

    - Case 3: Else if building is not all new and area type window-wall-ratio matches Table G3.1.1-1 allowance: `if ( NOT B_RMR.building.is_all_new ) AND ( area_type_wwr == data_lookup(table_G3_1_1_1, area_type_b) ): CAUTION and raise_warning "BUILDING IS NOT ALL NEW AND BASELINE WWR MATCHES VALUES PRESCRIBED IN TABLE G3.1.1-1. HOWEVER, THE FENESTRATION AREA PRESCRIBED IN TABLE G3.1.1-1 DOES NOT APPLY TO THE EXISTING ENVELOPE PER TABLE G3.1 BASELINE COLUMN #5 (C). FOR EXISTING ENVELOPE, THE BASELINE FENESTRATION AREA MUST EQUAL THE EXISTING FENESTRATION AREA PRIOR TO THE PROPOSED WORK. A MANUAL CHECK IS REQUIRED TO VERIFY COMPLIANCE."`

    - Case 4: Else, building is not all new and building segment window-wall-ratio does not match Table G3.1.1-1 allowance: `if ( NOT B_RMR.building.is_all_new ) AND ( area_type_wwr != data_lookup(table_G3_1_1_1, area_type_b) ): CAUTION and raise_warning "BUILDING IS NOT ALL NEW AND BASELINE WWR DOES NOT MATCH VALUES PRESCRIBED IN TABLE G3.1.1-1. HOWEVER, THE FENESTRATION AREA PRESCRIBED IN TABLE G3.1.1-1 DOES NOT APPLY TO THE EXISTING ENVELOPE PER TABLE G3.1 BASELINE COLUMN #5(c). FOR EXISTING ENVELOPE, THE BASELINE FENESTRATION AREA MUST EQUAL THE EXISTING FENESTRATION AREA PRIOR TO THE PROPOSED WORK. A MANUAL CHECK IS REQUIRED TO VERIFY COMPLIANCE."`

**[Back](../_toc.md)**
