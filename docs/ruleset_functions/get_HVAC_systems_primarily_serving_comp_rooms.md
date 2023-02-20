# get_HVAC_systems_primarily_serving_comp_rooms  

**Description:** Returns a list of HVAC systems in which the computer room space loads are the dominant loads for an HVAC system serving multiple spaces including computer rooms and non computer rooms.  

**Inputs:**  
- **U,B, or P-RMI**: To develop a list of HVAC systems in which greater than 50% of the area served by the HVAC system is computer room space.    

**Returns:**  
- **hvac_systems_primarily_serving_comp_rooms_list_x**: A list of hvac systems in which greater than 50% of the area served by the HVAC system is computer room space.    
 
**Function Call:**  

1. get_hvac_zone_list_w_area()  
2. zones_with_computer_room_dict_x()  
3. normalize_interior_lighting_schedules()  
4. normalize_misc_equipment_schedules()  

## Logic:   
- Create RMI object from RMI function input (RMI = function input): `X_RMI = RMI` 
- Create dictionary incuding all zones with at least one computer room: `zone_computer_room_dict = zones_with_computer_room_dict_x(X_RMI)`  
- Create list of zones with at least one computer room: `zone_with_computer_room_list = zone_computer_room_dict.keys()`  
- Get dictionary list of zones and the total floor area served by each HVAC system: `hvac_zone_list_w_area_dict_x = get_hvac_zone_list_w_area (X_RMI)`
- For each hvac_x in the X_RMI: `for hvac_x in X_RMI...HeatingVentilationAirConditioningSystem:`
    - Get the total floor area served by the hvac system: `hvac_sys_total_floor_area_x = hvac_zone_list_w_area_dict_x[hvac_x.id]["TOTAL_AREA"]`
    - Reset hvac system includes computer room boolean variable: `hvac_system_serves_computer_room_space = FALSE` 
    - Reset hvac_sys_computer_room_floor_area variable: `hvac_sys_computer_room_floor_area = 0`
    - Get list of zones served by hvac_x: `hvac_zone_list_x = hvac_zone_list_w_area_dict_x[hvac_x.id]["ZONE_LIST"]`
    - For each zone_x in hvac_zone_list_x: `for zone_x in hvac_zone_list_x:`
        - Check if the zone is in the list of zones with at least one computer room, if not loop to next zone: `if zone_x in zone_with_computer_room_list:`  
            - Set hvac system serves computer room boolean variable to true: `hvac_system_serves_computer_room_space = TRUE`  
            - For each space in zone: `for space_x in zone_x.Spaces:`        
                - Get the area (ft^2) of the space: `area = space.floor_area`  
                - Check if space is of type computer room, if yes then set the hvac system has computer room boolean variable to true and add the floor area to the total computer room floor area variable for the hvac system: `if space_x.lighting_space_type in ["COMPUTER_ROOM"]:`
                
                We should actually probably be looking at the design day schedules for this. 
                
                Occupany schedule check:  
                - Get the multiplier schedule: `multiplier_sch = get_component_by_id(B_RMI,space.occupant_multiplier_schedule)`    
                - Get the maximum value in the mulitplier schedule: `max_sch = max(multiplier_sch)`  
                - Get the number of occupant: `num_occ = space.number_of_occupants`  
                - Get the occupant sensible heat gain per occupant: `occ_gain (Watts per occupant) = space.occupant_sensible_heat_gain`  
                - Calculate the peak Wattage heat gain: `peak_occ_heat_gain = max_sch * num_occ * occ_gain`  

                Conduct checks for the interior lighting objects:  
                - Get list of interior lighting objects: `lgting_obj_list = list(space.interior_lighting)`   
                - Get a normalized interior lighitng schedule for the space (do not adjust for controls): `norm_sch = normalize_interior_lighting_schedules(space_x,False)`  
                - Get the maximum value in the schedule, W/ft^2 (please check if I understoof the normalize_interior_lighting_schedules function correctly): `max_W_sf = max(norm_sch)`  
                - Calcuate max Wattage
                    
                    



                Conduct checks for the miscellaneous objects:  
                - Get list of misc equipment objects: `misc_obj_list = list(space.miscellaneous_equipment)`      
                - Reset misc_pass_cooling boolean variable: `misc_pass_cooling = true`   
                - For each misc equipment object: `for misc in misc_obj_list:`  
                    - Get the multiplier schedule: `multiplier_sch = get_component_by_id(B_RMI,misc.multiplier_schedule)`  
                    - Get the design_cooling_multiplier_schedule: `design_cooling_multiplier_sch = multiplier_sch.cooling_design_day_sequence`  
                    - Get the get_most_used_weekday_hourly_schedule (this will be a list with 24 values for each hour of a day): `most_used_weekday_hourly_schedule = get_most_used_weekday_hourly_schedule(B_RMI, ASHRAE229,multiplier_sch)`  
                    - Reset y = 0: `y = 0`
                    - Check if each value in the design_cooling_multiplier_sch matches the corresponding hourly value in the get_most_used_weekday_hourly_schedule: `for x in list(design_cooling_multiplier_sch):`
                        - Check if the hourly values are equal between the design_cooling_multiplier_sch and the get_most_used_weekday_hourly_schedule : `if most_used_weekday_hourly_schedule[y] != x: misc_pass_cooling = false`  
                        - Add 1 to y: `y = y +1`  
                    
                    
                    
                    
                    
                    
                    
                    
                    - Get space floor_area: `space_floor_area = space_x.floor_area`
                    - Add floor area to hvac_sys_computer_room_floor_area: `hvac_sys_computer_room_floor_area = hvac_sys_computer_room_floor_area + space_floor_area`   
        - Check if the hvac system serves computer room boolean variable equals TRUE, if true then proceed otherwise loop to next hvac system: `if hvac_system_serves_computer_room_space == TRUE:`
            - Check if computer room floor area is greater than 50% of the total floor area served by the hvac system, if yes then carry on with the check: `if hvac_sys_computer_room_floor_area/hvac_sys_total_floor_area_x > 0.5:` 
                - Add to the list of hvac systems, hvac_systems_primarily_serving_comp_rooms_list_x: `hvac_systems_primarily_serving_comp_rooms_list_x = hvac_systems_primarily_serving_comp_rooms_list_x.append(hvac_x)`          

**Returns** `return hvac_systems_primarily_serving_comp_rooms_list_x`

**[Back](../_toc.md)**