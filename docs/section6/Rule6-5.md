
# Lighting - Rule 6-5

**Rule ID:** 6-5  
**Rule Description:** Baseline building is modeled with automatic shutoff controls in buildings >5000 sq.ft.  
**Appendix G Section:** Section G3.1-6 Modeling Requirements for the Baseline building  
**Appendix G Section Reference:**  None  

**Applicability:** All required data elements exist for B_RMD  
**Applicability Checks:**
  1. Building total area is more than 5,000sq.ft.  

**Manual Check:** Yes  

**Function Call:**  

  - compare_schedules()
  - normalize_space_schedules()

**Evaluation Context:** Each Data Element  
**Data Lookup:** None  

## Rule Logic:
- For each building in Baseline model: `for building_b in B_RMD`
  - Get building_open_schedule: `building_open_schedule_b = match_data_element(B_RMD, Schedules, building_b.building_open_schedule)`
  - For each space in the building: `for space_b in building_b...spaces:`
    - Add space floor area to building total floor area: `building_total_area_b += space_b.floor_area`  

  - **Applicability Check 1:**`if building_total_area_b > 5000:`  

  - For each space in building_b: `space_b in building_b...spaces:`  
    - Get total lighting power density in space: `total_space_LPD_b = sum(interior_lighting.power_per_area for interior_lighting in space_b.interior_lighting)`
    
    - Skip evaluating plenums, crawlspaces, and interstitial spaces that have no lighting power: `if total_space_LPD_b ==0 and space_b.function in [PLENUM, CRAWL_SPACE, INTERSTITIAL_SPACE]: continue`  

    - Get normalized space lighting schedule: `normalized_schedule_b = normalize_interior_lighting_schedules(space_b.interior_lighting, false)`  

    - Get matching space in P_RMD: `space_p = match_data_element(P_RMD, Spaces, space_b.id)`  

     - Get normalized space lighting schedule in P_RMD: `normalized_schedule_p = normalize_interior_lighting_schedules(space_p.interior_lighting, false)`

    - Check if automatic shutoff control is modeled in space during building closed hours (i.e. if lighting schedule hourly value in B_RMD is equal to P_RMD during building closed hours): `schedule_comparison_result = compare_schedules(normalized_schedule_b, normalized_schedule_p, inverse(building_open_schedule_b))`  

    **Rule Assertion:**

    - Case 1: If space has lighting power and is crawl space, interstitial space, or plenum: UNDETERMINED `if ( total_space_LPD_b > 0 ) AND ( space_function_b in [CRAWL_SPACE, INTERSTITIAL_SPACE, PLENUM] ): UNDETERMINED and raise_warning f"Space function is {space_function_b} and has lighting power modeled. Unable to determine whether this space should be included in the check."`
  
    - Case 2: For building closed hours, if lighting schedule hourly value in B_RMD is equal to P_RMD: `if schedule_comparison_result["total_hours_compared"] == schedule_comparison_result["total_hours_matched"]: PASS`  

    - Case 3: Else: `else: Failed`  


**Notes:**
  1. Updated the Rule ID from 6-9 to 6-6 on 6/3/2022
  2. Updated the Rule ID from 6-6 to 6-5 on 6/8/2022  
  3. Updated to exclude crawl space, plenum or interstitial space on 9/29/2025.

**[Back](../_toc.md)**
