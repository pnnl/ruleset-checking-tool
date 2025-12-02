
# Lighting - Rule 6-1

**Rule ID:** 6-1  
**Rule Description:** The total building interior lighting power shall not exceed the interior lighting power allowance determined using either Table G3.7 or G3.8.  
**Appendix G Section:** Section G1.2.1(b) Mandatory Provisions related to interior lighting power

**Appendix G Section Reference:**  

- Table G3.7, Performance Rating Method Lighting Power Density Allowances and Occupancy Sensor Reductions Using the Space-by-Space Method
- Table G3.8, Performance Rating Method Lighting Power Densities Using the Building Area Method  

**Applicability:** All required data elements exist for P_RMD  
**Manual Check:** Yes  
**Evaluation Context:** Each BuildingSegment  
**Data Lookup:** Table G3.7 and Table G3.8  
**Function Call:** None

## Rule Logic:

- For each building segment in the Proposed Model: `building_segment_p in P_RMD.building.building_segments`  

  - Initialize a variable to track if any space in the building segment is a crawl space, interstitial space, or plenum with lighting: `has_crawl_interstitial_plenum_with_lighting = FALSE`

  - Initialize a variable to track if any space does not specify lighting space type: `check_BAM_flag = FALSE`

- If building segment specifies lighting building area type, get the allowable lighting power density from Table G3-8: `if building_segment_p.lighting_building_area_type in table_G3_8: allowable_LPD_BAM = data_lookup(table_G3_8, building_segment_p.lighting_building_area_type)`  

  - For each thermal block in building segment: `thermal_block_p in building_segment_p.thermal_blocks:`  

    - For each zone in thermal block: `zone_p in thermal_block_p.zones:`  

      - For each space in zone: `space_p in zone_p.spaces:`  
        
        - Get the space total interior lighting power density: `space_total_LPD_p = sum(interior_lighting.power_per_area for interior_lighting in space_p.interior_lighting)`

        - Add lighting power to building segment total: `building_segment_design_lighting_wattage += (space_total_LPD_p * space_p.floor_area)`  

        - Check if the space is a crawl space, interstitial space, or plenum: `if space_p.function in [CRAWL_SPACE, INTERSTITIAL_SPACE, PLENUM]:`
      
          - If the space has interior lighting, set flag to TRUE: `if space_total_LPD_p > 0: has_crawl_interstitial_plenum_with_lighting = TRUE`
        
          - Continue to the next space, to take a conservative approach and avoid increasing the allowable lighting wattage for these spaces - since it is not clear if they should have lighting power allowance: `continue`
        - If building segment specifies lighting building area type , add space floor area to the total building segment floor area: `if allowable_LPD_BAM: total_building_segment_area_p += space_p.floor_area`  

        - Check if any space does not specify lighting space type, flag for Building Area Method: `if NOT space_p.lighting_space_type: check_BAM_flag = TRUE`  

        - Else, get the allowable lighting power density from Table G3-7: `else: allowable_LPD_space = data_lookup(table_G3_7, space_p.lighting_space_type)`  

          - Add to the total allowable lighting wattage for the building segment using Space-by-Space method: `allowable_lighting_wattage_SBS += allowable_LPD_space * space_p.floor_area`  

**Rule Assertion:**

- Case 1: For each building segment, if both lighting building area type and lighting space type in all spaces are specified, and the total lighting power in P_RMD is less than or equal to the higher of the building area method and space-by-space method allowances:  
  `if ( allowable_LPD_BAM ) and ( NOT check_BAM_flag ) and ( building_segment_design_lighting_wattage <= max(allowable_LPD_BAM * total_building_segment_area_p, allowable_lighting_wattage_SBS) ): PASS`  

- Case 2: Else if both lighting building area type and lighting space type in all spaces are specified, and the total lighting power in P_RMD is more than the higher of the building area method and space-by-space method allowances:  
  `else if ( allowable_LPD_BAM ) and ( NOT check_BAM_flag ) and ( building_segment_design_lighting_wattage > max(allowable_LPD_BAM * total_building_segment_area_p, allowable_lighting_wattage_SBS) ):`  
    - If `has_crawl_interstitial_plenum_with_lighting`:  
      `UNDETERMINED and raise_warning "the model included at least one plenum, crawlspace, or interstitial space with lighting power modeled. unable to determine whether these spaces should be included in the check. (list space ids that caused criteria, or include them in calc_vals)"`  
    - Else:  
      `FAIL`  

- Case 3: Else if lighting building area type is not specified, and lighting space type in all spaces are specified, and the total lighting power in P_RMD is less than or equal to the space-by-space method allowance:  
  `else if ( NOT allowable_LPD_BAM ) and ( NOT check_BAM_flag ) and ( building_segment_design_lighting_wattage <= allowable_lighting_wattage_SBS ): PASS and raise_warning 'project passes based on space-by-space method. verify if project uses space-by-space method.'`  

- Case 4: Else if lighting building area type is not specified, and lighting space type in all spaces are specified, and the total lighting power in P_RMD is more than the space-by-space method allowance:  
  `else if ( NOT allowable_LPD_BAM ) and ( NOT check_BAM_flag ) and ( building_segment_design_lighting_wattage > allowable_lighting_wattage_SBS ):`  
    - If `has_crawl_interstitial_plenum_with_lighting`:  
      `UNDETERMINED and raise_warning "the model included at least one plenum, crawlspace, or interstitial space with lighting power modeled. unable to determine whether these spaces should be included in the check. (list space ids that caused criteria, or include them in calc_vals)"`  
    - Else:  
      `FAIL and raise_warning 'project fails based on space-by-space method. lighting_building_area_type is not known to determine building area method allowance.'`  

- Case 5: Else if lighting building area type is specified, and lighting space type is not specified in all spaces, and the total lighting power in P_RMD is less than or equal to building area method allowance:  
  `else if ( allowable_LPD_BAM ) and ( check_BAM_flag ) and ( building_segment_design_lighting_wattage <= allowable_LPD_BAM * total_building_segment_area_p ): PASS and raise_warning 'project passes based on building area method. verify if project uses building area method.'`  

- Case 6: Else if lighting building area type is specified, and lighting space type is not specified in all spaces, and the total lighting power in P_RMD is more than building area method allowance:  
  `else if ( allowable_LPD_BAM ) and ( check_BAM_flag ) and ( building_segment_design_lighting_wattage > allowable_LPD_BAM * total_building_segment_area_p ):`  
    - If `has_crawl_interstitial_plenum_with_lighting`:  
      `UNDETERMINED and raise_warning "the model included at least one plenum, crawlspace, or interstitial space with lighting power modeled. unable to determine whether these spaces should be included in the check. (list space ids that caused criteria, or include them in calc_vals)"`  
    - Else:  
      `FAIL and raise_warning 'project fails based on building area method. lighting_space_type is not known in all spaces to determine space-by-space method allowance.'`  

- Case 7: Else, lighting building area type is not specified, and lighting space type is not specified in all spaces:  
  `Else:`  
    - If `has_crawl_interstitial_plenum_with_lighting`:  
      `UNDETERMINED and raise_warning "the model included at least one plenum, crawlspace, or interstitial space with lighting power modeled. unable to determine whether these spaces should be included in the check. (list space ids that caused criteria, or include them in calc_vals)"`  
    - Else:  
      `FAIL and raise_warning 'lighting_building_area_type is not known and lighting_space_type is not known in all spaces to determine allowance.'`  


**Notes:**
Updated the Rule ID from 6-2 to 6-1 on 6/8/2022

**[Back](../_toc.md)**
