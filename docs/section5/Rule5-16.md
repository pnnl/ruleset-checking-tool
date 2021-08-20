
# Envelope - Rule 5-18  

**Rule ID:** 5-18  
**Rule Description:** For building area types included in Table G3.1.1-1, vertical fenestration areas for new buildings and additions shall equal that in Table G3.1.1-1 based on the area of gross above-grade walls that separate conditioned spaces and semi-heated spaces from the exterior.  
**Rule Assertion:** Baseline RMR = expected value  
**Appendix G Section:** Section G3.1-5(c) Building Envelope Modeling Requirements for the Baseline building  
**Appendix G Section Reference:**  

- Table G3.1-5. Building Envelope, Baseline Building Performance, c. Vertical Fenestration Areas  
- Table G3.1.1-1  

**Applicability:** All required data elements exist for B_RMR
**Applicability Checks:** 

1. Building has spaces that are NEW, ADDITION or ALTERATION.  

**Manual Checks:** None  
**Evaluation Context:**  Each Data Element  
**Data Lookup:** Table G3.1.1-1  
**Function Call:**  

  1. get_overall_building_segment_wwr()

## Rule Logic:  

- **Applicability Check 1:** `length( [ if space.status_type for space in U_RMR...spaces is in [NEW, ADDITION, ALTERATION] ] ) > 0:`  

- Get window wall ratio dictionary for building: `building_wwr_dictionary_b = get_overall_building_segment_wwr(B_RMR)`

- For each building segment in the Baseline model: `for building_segment_b in B_RMR.building.building_segments:`

  - Check if building segment area type is included in Table G3.1.1-1: `if data_lookup(table_G3_1_1_1, building_segment_b.area_type_vertical_fenestration):`

    **Rule Assertion:**

      - Case 1: If building segment window-wall-ratio matches Table G3.1.1-1 allowance: `if building_wwr_dictionary_b[building_segment_b.id] == data_lookup(table_G3_1_1_1, building_segment_b.area_type_vertical_fenestration): PASS`

      - Case 2: Else: `else: CAUTION and raise_warning "BASELINE BUILDING SEGMENT AREA TYPE IS INCLUDED IN TABLE G3.1.1-1. BUT BUILDING SEGMENT FENESTRATION AREA DOES NOT MATCH TABLE G3.1.1-1. CHECK IF BUILDING SEGMENT HAS EXISTING ENVELOPE THAT CAN BE EXCLUDED FROM THE WINDOW-WALL-RATIO CALCULATION."`

**[Back](../_toc.md)**
