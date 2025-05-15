# Envelope - Rule 5-1  
**Schema Version** 0.0.33  
**Primary Rule** True  
**Rule ID:** 5-1   
**Rule Description:** There are four baseline rotations (i.e., four baseline models differing in azimuth by 90 degrees and four sets of baseline model results) if vertical fenestration area per each orientation differ by more than 5%.  
**Rule Assertion:** Options are PASS/FAIL     
**Appendix G Section:** Table G3.1#5a baseline column   
**90.1 Section Reference:** None  

**Data Lookup:** None    

**Evaluation Context:** Each RPD 

**Applicability Checks:**  
None
   
**Function Calls:**  
1. get_opaque_surface_type()  


## Rule Logic:   

Get the fenestration area for each unique orientation (i.e., azimuth) and then check if the minimum and maximum areas differ by 5% or more
- Create a blank dictionary that will have all unique azimuths paired with the total vertical fenestration area: `azimuth_fen_area_dict_b = {}`  
- For each building in the B_RMD: `for bldg in B_RMD.buildings:`    
    - For each building_segment in the bldg: `for bldg_seg in bldg.building_segments`      
        - For each zone in the building_segment: `for zone in bldg_seg.zones`   
            - For each surface in zone: `for surface in zone.surfaces:`  
                - Check if surface is above-grade wall: `if get_opaque_surface_type(surface) == "ABOVE-GRADE WALL":`   
                    - Get the azimuth: `surface_azimuth = surface.azimuth`  
                    - Check if the azimuth is not in a key in the dictionary of azimuths and fen area, if it is not then add it: `if surface_azimuth not in azimuth_fen_area_dict_b:`   
                        - Add the unique azimuth to the dictionary as a key and set initial fen area to 0: `azimuth_fen_area_dict_b[surface_azimuth]= 0`  
                    - Reset the total surface fenestration area variable to 0: `total_surface_fenestration_area = 0`  
                    - For each subsurface associated with the surface: `for sub_surface in surface.subsurfaces:`   
                        - Check if subsurface is door: `if sub_surface.classification == "DOOR":`
                            - If glazed area in door is more than 50% of the total door area, add door area to total_surface_fenestration_area: `if sub_surface.glazed_area > subsurface.opaque_area: total_surface_fenestration_area += sub_surface.glazed_area + sub_surface.opaque_area`
                        - Else, subsurface is not door, add total area to total_surface_fenestration_area (because we checked that the surface is an above grade wall we can assume that the subsurface classification is not and could not be a skylight so no need to check this): `total_surface_fenestration_area += subsurface.glazed_area + subsurface.opaque_area`      
                    - Add the total_surface_fenestration_area summed for the surface to the total fen area associated with the azimuth: `azimuth_fen_area_dict_b[surface_azimuth] += total_surface_fenestration_area`    

- Loop through the dictionary keys and put the area in bins depending on the azimuth (bins will be in 3 degree increments). Use this logic: if azimuth >= 0 and < 3  then put area in the 0-3 bin, if azimuth >=3 and < 6 then put the area in the the 3-6 bin, etc. `for azi in azimuth_fen_area_dict_b.keys():`  
    - Lookup the bin that the azimuth falls into based on the value of the azimuth using this logic. Bin lookup table based on this logic: if azimuth >= 0 and < 3  then put the fen area in the 0-3 bin, if azimuth >=3 and < 6 then put the area in the the 3-6 bin, etc. (this assumes the RCT team will create a lookup table to make it easy to lookup the bin that the azimuth (azi) falls into): `bin = lookup(azi, lookuptable)`  
    - Add the area to the bin in a revised binned dictionary (bin is key, area is value in dictionary): `azimuth_fen_area_dict_b[bin] += azimuth_fen_area_dict_b[azi]`    

Check if the area differs by 5 percent or more.
- Get the max fen area: `max_fen_area = azimuth_fen_area_dict_b[max(azimuth_fen_area_dict_b, key=azimuth_fen_area_dict_b.get)]`  
- Get the min fen area: `min_fen_area = azimuth_fen_area_dict_b[min(azimuth_fen_area_dict_b, key=azimuth_fen_area_dict_b.get)]`  
- Calculate the % difference, take the maximum calculated: `percent_difference = max(abs(max_fen_area- min_fen_area)/max_fen_area,abs(min_fen_area- max_fen_area)/min_fen_area)` 
- Check if the % difference is 5% or more, if it is then set rotation_expected_b boolean to TRUE: `if percent_difference >= 5%: rotation_expected_b = TRUE`  
- Else, set rotation_expected_b to FALSE: `else: rotation_expected_b = FALSE`  

- Set no_of_output_instance variable to 0 (counts the number of output instances): `no_of_output_instance =0`
Determine which RMDs have been created/provided
- Create variable for list of RMDs: `rmds = RulesetProjectDescription.ruleset_model_descriptions`
- Check for user RMD: `has_user = any[rmd.type == USER for rmd in rmds]`  
- Check for proposed RMD: `has_proposed = any[rmd.type == PROPOSED for rmd in rmds]`
- Check for baseline 0 degree RMD: `has_baseline_0 = any[rmd.type == BASELINE_0 for rmd in rmds]`
- Check for baseline 90 degree RMD: `has_baseline_90 = any[rmd.type == BASELINE_90 for rmd in rmds]`
- Check for baseline 180 degree RMD: `has_baseline_180 = any[rmd.type == BASELINE_180 for rmd in rmds]`
- Check for baseline 270 degree RMD: `has_baseline_270 = any[rmd.type == BASELINE_270 for rmd in rmds]`    
- Get the number of ruleset_model_descriptions: `no_of_rmds = len(rmds)`  

- Check that there is an output_instance associated with each RMD and add to the no_of_output_instance variable for each one `For rmd in rmds:`  
    - Check for proposed output: `if rmd.type == PROPOSED and rmd.output.Output2019ASHRAE901.output_instance != Null: has_proposed_output = TRUE`
    - Check for baseline 0 degree output: `if rmd.type == BASELINE_0 and rmd.output.Output2019ASHRAE901.output_instance != Null: has_baseline_0_output = TRUE`
    - Check for baseline 90 degree output: `if rmd.type == BASELINE_90 and rmd.output.Output2019ASHRAE901.output_instance != Null: has_baseline_90_output = TRUE`
    - Check for baseline 180 degree output: `if rmd.type == BASELINE_180 and rmd.output.Output2019ASHRAE901.output_instance != Null: has_baseline_180_output = TRUE`
    - Check for baseline 270 degree output: `if rmd.type == BASELINE_270 and rmd.output.Output2019ASHRAE901.output_instance != Null: has_baseline_270_output = TRUE` 
    - Check if there is an output_instance associated with the RMD: `if rmd.output.Output2019ASHRAE901.output_instance != Null: no_of_output_instance += 1 `
    
- **Rule Assertion:** 
- Case 1: If the fenestration area differs by 5% or more by orientation and there are 6 RMDs (for user, proposed, baseline at 0 degrees, baseline at 90 degrees, baseline at 180 degrees, and baseline at 270 degrees) and 5 output files (excludes an output for the user model) then Pass: `if rotation_expected_b == TRUE and has_user == TRUE and has_proposed == TRUE and has_baseline_0 == TRUE and has_baseline_90 == TRUE and has_baseline_180 == TRUE and has_baseline_270 == TRUE and has_proposed_output == TRUE and has_baseline_0_output == TRUE and has_baseline_90_output == TRUE and has_baseline_180_output == TRUE and has_baseline_270_output == TRUE and no_of_rmds == 6 and no_of_output_instance == 5: outcome = "PASS" `  
- Case 2: Else if rotation is not expected then pass as long as they have the minimally required RMDs and outputs: `if rotation_expected_b == FALSE and has_user == TRUE and has_proposed == TRUE and has_baseline_0 == TRUE and has_proposed_output == TRUE and has_baseline_0_output == TRUE: outcome = "PASS" `  
- Case 43: Else: `Else: outcome = "FAIL" and raise_message "Fail unless Table G3.1#5a exception #2 is applicable and it can be demonstrated that the building orientation is dictated by site considerations.`  



**Notes/Questions:**
None


**[Back](_toc.md)**
