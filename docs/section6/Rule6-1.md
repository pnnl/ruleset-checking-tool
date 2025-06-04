
# Lighting - Rule 6-1

**Rule ID:** 6-1  
**Rule Description:** The total building interior lighting power shall not exceed the interior lighting power allowance determined using either Table G3.7 or G3.8.  
**Appendix G Section:** Section G1.2.1(b) Mandatory Provisions related to interior lighting power
**Schema Version:** 0.1.3

**Appendix G Section Reference:**  

- Table G3.7, Performance Rating Method Lighting Power Density Allowances and Occupancy Sensor Reductions Using the Space-by-Space Method
- Table G3.8, Performance Rating Method Lighting Power Densities Using the Building Area Method  

**Applicability:** All required data elements exist for P_RMR  
**Manual Check:** Yes  
**Evaluation Context:** Each Data Element  
**Data Lookup:** Table G3.7 and Table G3.8  
**Function Call:** None

## Rule Logic:

- For each building segment in the Proposed Model: `building_segment_p in P_RMR.building.building_segments`  

  - If building segment specifies lighting building area type, get the allowable lighting power density from Table G3-8: `if building_segment_p.lighting_building_area_type in table_G3_8: allowable_LPD_BAM = data_lookup(table_G3_8, building_segment_p.lighting_building_area_type)`  

    - Look at each zone in the building segment: `zone_p in building_segment_p.zones:`  

      - For each space in zone: `space_p in zone_p.spaces:`
        - Get total lighting power density in space, EXCLUDING retail display lighting located in Sales Area space types: `total_space_LPD_p = 0`
          - Look at each lighting object in the space: `for interior_lighting in space_p.interior_lighting:`
            - create a boolean is_part_of_total and set it to true: `is_part_of_total = TRUE`
            - check whether the space type is one of the retail space types: `if space_p.lighting_space_type == "SALES AREA":`
              - check whether this specific interior_lighting object is Retail display.  If it is, set is_part_of_total to FALSE: `if interior_lighting.purpose_type == "RETAIL_DISPLAY": is_part_of_total = FALSE`
            - Add the LPD of this interior_lighting if it is not retail display lighting located in a retail space: `if is_part_of_total: building_segment_design_lighting_wattage += interior_lighting.power_per_area * space_p.floor_area` 

        - If building segment specifies lighting building area type , add space floor area to the total building segment floor area: `if allowable_LPD_BAM: total_building_segment_area_p += space_p.floor_area`  

        - Check if any space does not specify lighting space type, flag for Building Area Method: `if NOT space_p.lighting_space_type: check_BAM_flag = TRUE`  

        - Else, get the allowable lighting power density from Table G3-7: `else: allowable_LPD_space = data_lookup(table_G3_7, space_p.lighting_space_type)`  

          - Add to the total allowable lighting wattage for the building segment using Space-by-Space method: `allowable_lighting_wattage_SBS += allowable_LPD_space * space_p.floor_area`  

**Rule Assertion:**

- Case 1: For each building segment, if both lighting building area type and lighting space type in all spaces are specified, and the total lighting power in P_RMR is less than or equal to the higher of the Building Area Method and Space-by-Space Method allowances: `if ( allowable_LPD_BAM ) and ( NOT check_BAM_flag ) and ( building_segment_design_lighting_wattage <= max(allowable_LPD_BAM * total_building_segment_area_p, allowable_lighting_wattage_SBS) ): PASS`  

- Case 2: Else if both lighting building area type and lighting space type in all spaces are specified, and the total lighting power in P_RMR is more than the higher of the Building Area Method and Space-by-Space Method allowances: `else if ( allowable_LPD_BAM ) and ( NOT check_BAM_flag ) and ( building_segment_design_lighting_wattage > max(allowable_LPD_BAM * total_building_segment_area_p, allowable_lighting_wattage_SBS) ): FAIL`  

- Case 3: Else if lighting building area type is not specified, and lighting space type in all spaces are specified, and the total lighting power in P_RMR is less than or equal to the Space-by-Space Method allowance: `else if ( NOT allowable_LPD_BAM ) and ( NOT check_BAM_flag ) and ( building_segment_design_lighting_wattage <= allowable_lighting_wattage_SBS ): PASS and raise_warning 'PROJECT PASSES BASED ON SPACE-BY-SPACE METHOD. VERIFY IF PROJECT USES SPACE-BY-SPACE METHOD.'`  

- Case 4: Else if lighting building area type is not specified, and lighting space type in all spaces are specified, and the total lighting power in P_RMR is more than the Space-by-Space Method allowance: `else if ( NOT allowable_LPD_BAM ) and ( NOT check_BAM_flag ) and ( building_segment_design_lighting_wattage > allowable_lighting_wattage_SBS ): FAIL and raise_warning 'PROJECT FAILS BASED ON SPACE-BY-SPACE METHOD. LIGHTING_BUILDING_AREA_TYPE IS NOT KNOWN TO DETERMINE BUILDING AREA METHOD ALLOWANCE.'`  

- Case 5: Else if lighting building area type is specified, and lighting space type is not specified in all spaces, and the total lighting power in P_RMR is less than or equal to Building Area Method allowance: `else if ( allowable_LPD_BAM ) and ( check_BAM_flag ) and ( building_segment_design_lighting_wattage <= allowable_LPD_BAM * total_building_segment_area_p ): PASS and raise_warning 'PROJECT PASSES BASED ON BUILDING AREA METHOD. VERIFY IF PROJECT USES BUILDING AREA METHOD.'`  

- Case 6: Else if lighting building area type is specified, and lighting space type is not specified in all spaces, and the total lighting power in P_RMR is more than Building Area Method allowance: `else if ( allowable_LPD_BAM ) and ( check_BAM_flag ) and ( building_segment_design_lighting_wattage > allowable_LPD_BAM * total_building_segment_area_p ): FAIL and raise_warning 'PROJECT FAILS BASED ON BUILDING AREA METHOD. LIGHTING_SPACE_TYPE IS NOT KNOWN IN ALL SPACES TO DETERMINE SPACE-BY-SPACE METHOD ALLOWANCE.'`  

- Case 7: Else, lighting building area type is not specified, and lighting space type is not specified in all spaces: `Else: FAIL and raise_warning 'LIGHTING_BUILDING_AREA_TYPE IS NOT KNOWN AND LIGHTING_SPACE_TYPE IS NOT KNOWN IN ALL SPACES TO DETERMINE ALLOWANCE.'`  

**Notes Before Update for Reference Only:**
Updated the Rule ID from 6-2 to 6-1 on 6/8/2022

The RDS needs to be updated in the future based on the following:
- If lighting_building_area_type and lighting_space_type are know known, then calculate allowance based on both, pass if less than max  

- If lighting_building_area_type is not specified, lighting_space_type for all spaces in the building segment is included: then determine allowance based on lighting space type.  
    - If PASS- Output should say that project passed based on space by space method. Reviewer should verify if the project uses space by space method.  
    - If FAIL- then CAUTION and say that it fails space by space method and lighting_building_area_type is not known to determine allowance based on BAT.  

- If lighting_building_area_type provided but lighting_space_type not included:   
    - If PASS - Output should say that project passed based on building area method. Reviewer should verify if the project uses building area method.
    - If FAIL- then CAUTION and say that it fails building area method and lighting_space_type is not known to determine allowance based on space by sspace method.    

**[Back](../_toc.md)**
