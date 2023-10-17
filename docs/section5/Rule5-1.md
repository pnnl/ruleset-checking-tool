# Envelope - Rule 5-1  
**Schema Version** 0.0.33
**Primary Rule** True
**Rule ID:** 5-1  
**Rule Description:** There are four baseline rotations (i.e., four baseline models differing in azimuth by 90 degrees and four sets of baseline model results) if vertical fenestration area per each orientation differ by more than 5%.
**Rule Assertion:** Options are PASS/FAIL     
**Appendix G Section:** Table G3.1#5a baseline column   
**90.1 Section Reference:** None  

**Data Lookup:** None    

**Evaluation Context:** Each RMD 

**Applicability Checks:**  
None
   
**Function Calls:**  
1. get_surface_conditioning_category()
2. get_opaque_surface_type()  


## Rule Logic:   

Get the fenestration area for each unique orientation (i.e., azimuth) and then check if the minimum and maximum areas differ by 5% or more
- Create a blank dictionary that will have all unique azimuths paired with the total vertical fenestration area: `azimuth_fen_area_dict = {}`  
- For each building in the B_RMI: `for bldg in B_RMI.buildings:`    
    - For each building_segment in the bldg: `for bldg_seg in bldg.building_segments`      
        - For each zone in the building_segment: `for zone in bldg_seg.zones`   
            - For each surface in zone: `for surface in zone.surfaces:`  
                - Check if surface is above-grade wall: `if get_opaque_surface_type(surface) == "ABOVE-GRADE WALL":`   
                    - Get the azimuth: `surface_azimuth = surface.azimuth`  
                    - Check if the azimuth is not in a key in the dictionary of azimuths and fen area, if it is not then add it: `if surface_azimuth not in azimuth_fen_area_dict:`   
                        - Add the unique azimuth to the dictionary as a key and set initial fen area to 0: `azimuth_fen_area_dict[surface_azimuth]= 0`  
                    - Reset the total surface fenestration area variable to 0: `total_surface_fenestration_area = 0`  
                    - For each subsurface associated with the surface: `for sub_surface in surface.subsurfaces:`   
                        - Check if subsurface is door: `if sub_surface.classification == "DOOR":`
                            - If glazed area in door is more than 50% of the total door area, add door area to total_surface_fenestration_area: `if sub_surface.glazed_area > subsurface.opaque_area: total_surface_fenestration_area += sub_surface.glazed_area + sub_surface.opaque_area`
                        - Else, subsurface is not door, add total area to total_surface_fenestration_area (because we checked that the surface is an above grade wall we are assuming the subsurface classification is not and could not be a skylight): `total_surface_fenestration_area += subsurface.glazed_area + subsurface.opaque_area`      
                    - Add the total_surface_fenestration_area summed for the surface to the total fen area associated with the azimuth: `azimuth_fen_area_dict[surface_azimuth] += total_surface_fenestration_area`    

Check if the area differs by 5 percent or more.
- Get the max fen area: `max_fen_area = azimuth_fen_area_dict[max(azimuth_fen_area_dict, key=azimuth_fen_area_dict.get)]`  
- Get the min fen area: `min_fen_area = azimuth_fen_area_dict[min(azimuth_fen_area_dict, key=azimuth_fen_area_dict.get)]`  
- Calculate the % difference, take the maximum calculated: `percent_difference = max(abs(max_fen_area- min_fen_area)/max_fen_area,abs(min_fen_area- max_fen_area)/min_fen_area)` 
- Check if the % difference is 5% or more, if it is then set rotation_expected boolean to TRUE: `if percent_difference >= 5%: rotation_expected = TRUE`  
- Else, set rotation_expected to FALSE: `else: rotation_expected = FALSE`  

- Set counter variable to 0 (counts the number of output instances): `counter =0`
- Get the number of ruleset_model_descriptions: `number_of_RMIs = len(ASHRAE229.ruleset_model_descriptions)`  
- Check that there is an output_instance associated with each RMI and add to the counter variable for each one `For RMI in ASHRAE229.ruleset_model_descriptions:`  
    - Check if there is an output_instance associated with the RMI: `if RMI.output.Output2019ASHRAE901.output_instance != Null: counter += 1 `
    
    - **Rule Assertion:** 
    - Case 1: If the fenestration area differs by 5% or more by orientation and there are 6 RMIs (for user, proposed, baseline at 0 degrees, baseline at 90 degrees, baseline at 180 degrees, and baseline at 270 degrees) and 5 output files (excludes an output for the user model) then Pass: `if rotation_expected == TRUE and and number_of_RMIs == 6 and counter == 5: outcome = "PASS" `  
    - Case 2: Else if the fenestration area differs by less than 5% and there are 3 RMIs (for user, proposed, baseline at 0 degrees) and 2 output files (excludes an output for the user model) then Pass: `if rotation_expected == FALSE and and number_of_RMIs == 3 and counter == 2: outcome = "PASS" `  
    - Case 43: Else: `Else: outcome = "FAIL" and raise_message "Fail unless Table G3.1#5a exception #2 is applicable and it can be demonstrated that the building orientation is dictated bysite considerations.`  



**Notes/Questions:**
1. I think some of the terminololgy regarding RMI/RMD has changed since I last worked on this. I need some help understanding the expected output_instances and how that relates to the ruleset_model_descriptions. I got turned around reading the descriptions. 



**[Back](_toc.md)**
