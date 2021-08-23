
# Lighting - Rule 6-7

**Rule ID:** 6-7  
**Rule Description:** Where a complete lighting system exists and where a lighting system has been designed and submitted with design documents, the baseline LPD is equal to expected value in Table G3.7. Where lighting neither exists nor is submitted with design documents, baseline LPD shall be determined in accordance with Table G3-8.

**Appendix G Section:** Section G3.1-6 Modeling Requirements for the Baseline

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:** None  
**Manual Check:** Yes

**Evaluation Context:** Each Data Element  
**Data Lookup:** Table G3.7 and Table G3.8  
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

          - Get total lighting power density in space: `total_space_LPD_b = sum(interior_lighting.power_per_area for interior_lighting in space_b.interior_lighting)`

          - Get lighting status type for space: `space_lighting_status_type = space_lighting_status_type_dict_p[match_data_element(P_RMR, Spaces, space_b.id).id]`

            **Rule Assertion:**

            - Case 1: If space lighting status type is as-designed or as-existing, and space total interior lighting power density in B_RMR matches Table G3.7: `if ( space_lighting_status_type == "AS-DESIGNED OR AS-EXISTING" ) AND ( total_space_LPD_b == data_lookup(table_G3_7, space_b.lighting_space_type) ): PASS`  

            - Case 2: Else if space lighting status type is as-designed or as-existing, and if lighting space type is not specified: `else if ( space_lighting_status_type == "AS-DESIGNED OR AS-EXISTING" ) AND ( NOT space_b.lighting_space_type ): CAUTION and raise_warning "LIGHTING SPACE TYPE IS NOT SPECIFIED TO DETERMINE BASELINE LPD."`

            - Case 3: Else if space lighting status type is as-designed or as-existing, and space total interior lighting power density in B_RMR is higher than Table G3.7 and lighting space type is Sales Area: `else if ( space_lighting_status_type == "AS-DESIGNED OR AS-EXISTING" ) AND ( total_space_LPD_b > data_lookup(table_G3_7, space_b.lighting_space_type) ) AND ( space_b.lighting_space_type == "SALES AREA" ): CAUTION and raise_warning "BASELINE SPACE LIGHTING POWER DENSITY DOES NOT MATCH TABLE G3.7 AND SPACE IS SALES AREA. CHECK IF ADDITIONAL DISPLAY LIGHTING IS INCLUDED. "`

            - Case 4: Else if space lighting status type is as-designed or as-existing, and space total interior lighting power density in B_RMR does not match Table G3.7: `else if ( space_lighting_status_type == "AS-DESIGNED OR AS-EXISTING" ) AND ( total_space_LPD_b != data_lookup(table_G3_7, space_b.lighting_space_type) ): FAIL`

            - Case 5: Else if space lighting status type is not-yet designed or matches Table_9_5_1, and space total interior lighting power density in B_RMR matches Table G3.7: `else if ( space_lighting_status_type == "NOT-YET DESIGNED OR MATCH TABLE_9_5_1" ) AND ( total_space_LPD_b == data_lookup(table_G3_7, space_b.lighting_space_type) ): PASS`

            - Case 6: Else if space lighting status type is not-yet designed or matches Table_9_5_1, and space total interior lighting power density in B_RMR matches Table G3.8: `else if ( space_lighting_status_type == "NOT-YET DESIGNED OR MATCH TABLE_9_5_1" ) AND ( total_space_LPD_b == data_lookup(table_G3_8, building_segment_b.lighting_building_area_type) ): PASS`

            - Case 7: Else: `else: FAIL`

