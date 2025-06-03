# get_HVAC_systems_primarily_serving_comp_rooms  

**Description:** Returns a list of HVAC systems in which the computer room space loads are the dominant loads for an HVAC system serving multiple spaces including computer rooms and non computer rooms (i.e., computer room spaces accounts for greater than 50% of cooling load).  

**Inputs:**  
- **U,B, or P-RMI**: To develop a list of HVAC systems in which the computer room space loads are the dominant loads for an HVAC system serving multiple spaces including computer rooms and non computer rooms (i.e., computer room spaces accounts for greater than 50% of cooling load). 

**Returns:**  
- **hvac_systems_primarily_serving_comp_rooms_list_x**: A list of hvac systems in which the computer room space loads are the dominant loads for an HVAC system serving multiple spaces including computer rooms and non computer rooms (i.e., computer room spaces accounts for greater than 50% of cooling load). 
 
**Function Call:**  

1. get_hvac_zone_list_w_area()   
2. is_space_a_computer_room()  

## Logic:   
- Create RMI object from RMI function input (RMI = function input): `X_RMI = RMI` 
- Create list of zones with at least one computer room, For each zone_x in X_RMD: `for zone_x in X_RMI...Zone:`  
  - Loop through spaces associated with zone, for each space in zone_x: `for space_x in Zone.spaces:`  
    - If the space type is computer room then add zone to list of zones with at least one computer room: `if space_x.lighting_space_type in ["COMPUTER_ROOM"]:`  
      - Add zone to list of zones with at least one computer room: `if zone_x not in zone_with_computer_room_list: zone_with_computer_room_list.append(zone_x)`  
- Get dictionary list of zones and the total floor area served by each HVAC system: `hvac_zone_list_w_area_dict_x = get_hvac_zone_list_w_area (X_RMI)`
- For each hvac_x in the X_RMI: `for hvac_x in X_RMI...HeatingVentilationAirConditioningSystem:`
    - Reset hvac system includes computer room boolean variable: `hvac_system_serves_computer_room_space = FALSE` 
    - Reset total_Wattage_across_hvac_sys: `total_Wattage_across_hvac_sys = 0`  
    - Reset total_Wattage_across_hvac_sys_for_computer_room: `total_Wattage_across_hvac_sys_for_computer_room = 0`  
    - Get list of zones served by hvac_x: `hvac_zone_list_x = hvac_zone_list_w_area_dict_x[hvac_x.id]["ZONE_LIST"]`  
    - For each zone_x in hvac_zone_list_x: `for zone_x in hvac_zone_list_x:`
        - Check if the zone is in the list of zones with at least one computer room, if not loop to next zone: `if zone_x in zone_with_computer_room_list:`  
            - Set hvac system serves computer room boolean variable to true: `hvac_system_serves_computer_room_space = TRUE`  
            - Reset total_Wattage_zone: `total_Wattage_zone = 0`  
            - For each space in zone: `for space_x in zone_x.Spaces:`        
                - Reset space_is_a_computer_room to false: `space_is_a_computer_room = false`  
                - Reset total_Wattage_space: `total_Wattage_space = 0`  
                - Get the area (ft^2) of the space: `area = space.floor_area`  
                - Check if space is of type computer room, if yes then set the space is a computer room boolean variable to true: `if is_space_a_computer_room(RMI,space_x) == true: space_is_a_computer_room = true`  
                
                NOTE: Design day schedules used, these should have the same value for all hours (except for dwelling units which are irrelevant here) so no need to find the coincident peak across the schedules. No need to even find the peak but did just in case there is an odd value in the schedule.

                Occupancy Wattage calculation: 
                - Get the multiplier schedule: `multiplier_sch = get_component_by_id(B_RMI,space.occupant_multiplier_schedule)`    
                - Get the design_cooling_multiplier_schedule: `design_cooling_multiplier_sch = multiplier_sch.hourly_cooling_design_day if hasattr(multiplier_sch, "hourly_cooling_design_day") else multiplier_sch.hourly_cooling_design_year`  
                - Get the maximum value in the schedule (the schedule should have this value for every hour): `max_sch = max(design_cooling_multiplier_sch)`  
                - Get the number of occupant: `num_occ = space.number_of_occupants`  
                - Get the occupant sensible heat gain per occupant: `occ_gain (Watts per occupant) = space.occupant_sensible_heat_gain`  
                - Calculate the peak design Wattage heat gain: `peak_occ_heat_gain = max_sch * num_occ * occ_gain`  
                - Add to the running Wattage total for the space: `total_Wattage_space = total_Wattage_space + peak_occ_heat_gain`  
                    
                Interior lighting Wattage calculation: 
                - Get list of interior lighting objects: `lgting_obj_list = list(space.interior_lighting)`   
                - Reset the temp_total_power variable: `temp_total_power = 0`  
                - For each interior lighting object: `for int_lgt in lgting_obj_list:`  
                    - Get the multiplier schedule: `multiplier_sch = get_component_by_id(B_RMI,int_lgt.lighting_multiplier_schedule)`  
                    - Get the design_cooling_multiplier_schedule: `design_cooling_multiplier_sch = multiplier_sch.hourly_cooling_design_day if hasattr(multiplier_sch, "hourly_cooling_design_day") else multiplier_sch.hourly_cooling_design_year`    
                    - Get the maximum value in the schedule (the schedule should have this value for every hour): `max_sch = max(design_cooling_multiplier_sch)`  
                    - Get the power per area for the lighting object: `lgt_W_sf = int_lgt.power_per_area`  
                    - Calculate the power for the lighting object including schedule fraction: `lgt_W = lgt_W_sf * area * max_sch `  
                    - Add to total across the space: `temp_total_power = temp_total_power + lgt_W`  
                - Add to the running Wattage total for the space: `total_Wattage_space = total_Wattage_space + temp_total_power`  
                    
                Miscellaneous Wattage calculation:  
                - Get list of misc equipment objects: `misc_obj_list = list(space.miscellaneous_equipment)`        
                - Reset the temp_total_power variable: `temp_total_power = 0`                  
                - For each misc equipment object: `for misc in misc_obj_list:`  
                    - Get the multiplier schedule: `multiplier_sch = get_component_by_id(B_RMI,misc.multiplier_schedule)`  
                    - Get the design_cooling_multiplier_schedule: `design_cooling_multiplier_sch = multiplier_sch.hourly_cooling_design_day if hasattr(multiplier_sch, "hourly_cooling_design_day") else multiplier_sch.hourly_cooling_design_year`    
                    - Get the maximum value in the schedule (the schedule should have this value for every hour): `max_sch = max(design_cooling_multiplier_sch)`  
                    - Get the power for the misc object: `misc_power = misc.power`  
                    - Calculate the power for the misc object including schedule fraction and sensible fraction: `misc_W = misc_power * max_sch * misc.sensible_fraction `  
                    - Add to total across the space: `temp_total_power = temp_total_power + misc_W`  
                - Add to the running Wattage total for the space: `total_Wattage_space = total_Wattage_space + temp_total_power`  
            
                - Add to the total Wattage across all spaces serving zone: `total_Wattage_zone = total_Wattage_zone + total_Wattage_space`    
                - Check if the space serves a computer room: `if space_is_a_computer_room == true: total_zone_Wattage_of_computer_rooms_only = total_zone_Wattage_of_computer_rooms_only + total_Wattage_space`                     
        
        - Add to the total Wattage across all zones: `total_Wattage_across_hvac_sys = total_Wattage_across_hvac_sys + total_Wattage_zone`  
        - Add to the total Wattage across all zones including only computer rooms spaces: `total_Wattage_across_hvac_sys_for_computer_room = total_Wattage_across_hvac_sys_for_computer_room + total_zone_Wattage_of_computer_rooms_only`  
    - Check if the hvac system is associated with a computer room and if so that the computer room Wattage is more than 50% of the total Wattage: `if hvac_system_serves_computer_room_space == true and total_Wattage_across_hvac_sys_for_computer_room/hvac_system_serves_computer_room_space > 50%:         hvac_systems_primarily_serving_comp_rooms_list_x.append(hvac_x)`          

**Returns** `return hvac_systems_primarily_serving_comp_rooms_list_x`

**Notes/Questions:**   
1. Interpretation: When computer rooms account for more than 50% of the cooling load of an HVAC system, such HVAC system is considered “primarily serving computer rooms” and is subject to the exception 3 to Table G3.1#4, Proposed Building Performance column HVAC Fans Schedules rule. 


**[Back](../_toc.md)**