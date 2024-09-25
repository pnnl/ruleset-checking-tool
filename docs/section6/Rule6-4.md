
# Lighting - Rule 6-4

**Rule ID:** 6-4  
**Rule Description:** Where a complete lighting system exists and where a lighting system has been designed and submitted with design documents, the baseline LPD is equal to expected value in Table G3.7. Where lighting neither exists nor is submitted with design documents, baseline LPD shall be determined in accordance with Table G3-7 for "Office-Open Plan" space type.

**Appendix G Section:** Section G3.1-6 Modeling Requirements for the Baseline

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:** None  
**Manual Check:** No

**Evaluation Context:** Each Data Element  
**Data Lookup:** Table G3.7  
**Function Call:**  

  - get_lighting_status_type()
  - match_data_element()
  - data_lookup()


## Rule Logic: 

- For each building segment in the baseline model: `building_segment_b in B_RMR.building.building_segments:`  

  - Get matching building segment in R_RMR: `building_segment_p = match_data_element(P_RMR, BuildingSegments, building_segment_b.id)`

    - Get lighting status type dictionary for P_RMR: `space_lighting_status_type_dict_p = get_lighting_status_type(building_segment_p)`  
  
  - For each thermal block in building segment: `thermal_block_b in building_segment_b.thermal_blocks:`  
  
    - For each zone in thermal block: `zone_b in thermal_block_b.zones:`  

      - For each space in zone: `space_b in zone_b.spaces:`  

        - For each space in zone: `space_b in zone_b.spaces:`  

          - Get total lighting power density in space, EXCLUDING retail display lighting located in Sales Area space types: `total_space_LPD_b = 0`
          - Look at each lighting object in the space: `for interior_lighting in space_b.interior_lighting:`
            - create a boolean is_part_of_total and set it to true: `is_part_of_total = TRUE`
            - check whether the space type is one of the retail space types: `if space_b.lighting_space_type == "SALES AREA":`
              - check whether this specific interior_lighting object is Retail display.  If it is, set is_part_of_total to FALSE: `if interior_lighting.purpose_type == "RETAIL_DISPLAY": is_part_of_total = FALSE`
            - Add the LPD of this interior_lighting if it is not retail display lighting located in a retail space: `if is_part_of_total: total_space_LPD_b += interior_lighting.power_per_area`

          - Get lighting status type for space: `space_lighting_status_type = space_lighting_status_type_dict_p[match_data_element(P_RMR, Spaces, space_b.id).id]`

          - Check if lighting space type is specified, get lighting power density allowance from Table G3.7: `if space_b.lighting_space_type: LPD_allowance_b = data_lookup(table_G3_7, space_b.lighting_space_type)`

          - Else, lighting space type is not specified, assume "Office-Open Plan" as lighting space type to get lighting power density allowance from Table G3.7: `else: LPD_allowance_b = data_lookup(table_G3_7, "OFFICE-OPEN PLAN")`

            **Rule Assertion:**

            - Case 1: If space lighting status type is as-designed or as-existing, and lighting space type is not specified: `if ( space_lighting_status_type == "AS-DESIGNED OR AS-EXISTING" ) AND ( NOT space_b.lighting_space_type ): FAIL and raise_warning "P_RMR LIGHTING STATUS TYPE IS AS-DESIGNED OR AS-EXISTING. BUT LIGHTING SPACE TYPE IN B_RMR IS NOT SPECIFIED."`

            - Case 2: Else if space lighting status type is as-designed or as-existing, and space total interior lighting power density in B_RMR matches Table G3.7: `else if ( space_lighting_status_type == "AS-DESIGNED OR AS-EXISTING" ) AND ( total_space_LPD_b == LPD_allowance_b ): PASS`  

            - Case 3: Else if space lighting status type is as-designed or as-existing, and space total interior lighting power density in B_RMR does not match Table G3.7: `else if ( space_lighting_status_type == "AS-DESIGNED OR AS-EXISTING" ) AND ( total_space_LPD_b != LPD_allowance_b ): FAIL`

            - Case 4: Else if space lighting status type is not-yet designed or matches Table_9_5_1, and space total interior lighting power density in B_RMR matches Table G3.7: `else if ( space_lighting_status_type == "NOT-YET DESIGNED OR MATCH TABLE_9_5_1" ) AND ( total_space_LPD_b == LPD_allowance_b ): PASS`

            - Case 5: Else, space lighting status type is not-yet designed or matches Table_9_5_1, and space total interior lighting power density in B_RMR does not match Table G3.7: `else if ( space_lighting_status_type == "NOT-YET DESIGNED OR MATCH TABLE_9_5_1" ) AND ( total_space_LPD_b != LPD_allowance_b ): FAIL`

**Notes:**
  1. Requirements from addendum AF to 90.1-2019 have not been incorporated into this RDS.
  2. Updated the Rule ID from 6-7 to 6-5 on 6/3/2022
  3. Update the Rule ID from 6-5 to 6-4 on 6/8/2022

**[Back](../_toc.md)**
