## get_zones_G3.1.1c_40_EFLHs

**Description:** Get the list of zones in which baseline HVAC system type 3 or 4 has been used for spaces (zones???) that differ by more than 40 equivalent full load hrs/week from other spaces (zones???) served by the system.   

**Inputs:**
- **B_RMR**: To determine which (if any) baseline HVAC system type 3 or 4 has been used for spaces (zones???) that differ by more than 40 equivalent full load hrs/week from other spaces (zones???) served by the system.   

**Returns:**
- **applicable_zones_G3.1.1c_40_EFLHs_list_b**: A list that saves all zones that have baseline HVAC system type 3 or 4 has been used for spaces (zones???) that differ by more than 40 equivalent full load hrs/week from other spaces (zones???) served by the system. 
 
**Function Call:** 

1. get_baseline_system_types


**Logic:**
- For each building_segment_b in B_RMR: `for building_segment_b in B_RMR:`
- Set applicability flag to FALSE: `rule_applicability_check = FALSE`  
- Get dictionary of baseline hvac system types and ids: `baseline_hvac_sys_type_ids_dict_b = get_baseline_system_types(B_RMR)`
    - For each hvac_b in the building_segment: `For hvac_b in building_segment_b.heating_ventilation_air_conditioning_systems:`
        - Get hvac system type for hvac_b: `hvac_sys_type_b = baseline_hvac_sys_type_ids_dict_b.keys()[list(baseline_hvac_sys_type_ids_dict_b.values()).index(hvac_b.id)]`
        - Check if HVAC system is type 5, 6, 7, or 8 exists, if so then carry on, if not skip building segment: `if get_baseline_system_types(hvac_b.id) in ["SYS-5", "SYS-6", "SYS-7", "SYS-8", "SYS-7a", "SYS-8a","SYS-5b", "SYS-6b", "SYS-7b", "SYS-7c"]:`
            # Create a dictionary with zone ID as key and a list with zone descriptor information (including the HVAC system with the longest fan schedule) for access later in the logic
            - for each zone_b in the building_segment_b: `for zone_b in building_segment_b:`
                - Reset the computer room boolean variable to false: `computer_room_zone_b = FALSE`
                - Reset the all labs boolean variable to false: `all_labs_zone_b = FALSE`
                - Get the floor number that the zone is associated with: `zone_floor_number_b = zone_b.zone_floor_number`
                    - Add to the list of floors in the building segment, keep adding as the code loops through the zones: `floor_list_b = floor_list_b.append(zone_floor_number_b)`
                - For each terminal unit associated with each zone: `for terminal_b in zone_b:`
                    - Get the served_by_heating_ventilation_air_conditioning_systems for each terminal: `heating_ventilation_air_conditioning_systems_b = terminal_b.served_by_heating_ventilation_air_conditioning_systems`
                    - Add to list of heating_ventilation_air_conditioning_systems_list_b as the code loops through the terminal units: `heating_ventilation_air_conditioning_systems_list_b = heating_ventilation_air_conditioning_systems_list_b.append(heating_ventilation_air_conditioning_systems_b)`                
                - Convert the list of heating_ventilation_air_conditioning_systems_list_b associated with the zone to a set and the back to a list to eliminate duplicates: `heating_ventilation_air_conditioning_systems_list_b = list(set(heating_ventilation_air_conditioning_systems_list_b))`
                - For each hvac_b in heating_ventilation_air_conditioning_systems_list_b: `for hvac_b in heating_ventilation_air_conditioning_systems_list_b:`
                    - For each fan_system_b in hvac_b: `for fan_system_b in hvac_b.fan_systems:`
                        - Reset fan_schedule_b to zero for each zone: `fan_schedule_b =0`       
                        - For each value in the fan_schedule_b.operating_schedule: `for x in range(8760):`
                            - Calculate sum across hourly values in fan_schedule_b.operating_schedule: `fan_schedule_b = fan_schedule_b + fan_system_b.operating_schedule(x)`
                        - Add sum to dictionary with fan_system_b.id as key and fan_schedule_b as value: `hvac_fan_schedule_dict[fan_system_b.ID] = fan_schedule_b`
                    - Find the key for the fan_system_b with the longest schedule associated with hvac_b: `longest_sch_fan_system = max(hvac_fan_schedule_dict, key = hvac_fan_schedule_dict.get())`
                    - Get max fan_schedule_b value for the longest_sch_fan_system key: `max_fan_sch_value = hvac_fan_schedule_dict[longest_sch_fan_system]`
                    - Add max_fan_sch_value to dictionary with hvac.id as key: `zone_hvac_fan_schedule_dict[hvac_b.ID] = max_fan_sch_value`                     
                - Find the key for the hvac_b with the longest fan operating schedule: `longest_sch_fan_system = max(zone_hvac_fan_schedule_dict, key = zone_hvac_fan_schedule_dict.get())`
                - Get max fan operating schedule value for the longest_sch_fan_system key: `max_fan_sch_value = zone_hvac_fan_schedule_dict[longest_sch_fan_system]`
                - Set hvac_b equal to the hvac system with the longest fan operating schedule for the zone: `hvac_b = longest_sch_fan_system`             
                - Get the HVAC system type: `hvac_type_b = baseline_hvac_sys_type_ids_dict_b.keys()[list(baseline_hvac_sys_type_ids_dict_b.values()).index(hvac_b.id)]`
                - Store the HVAC system id as a variable::  `hvac_id_b = hvac_b.id`
                
                - For each space_b in zone_b: `for space_b in zone_b:`
                    - Check if any spaces associated with the zone_b are labs: `if space_b.lighting_space_type == LABORATORY_EXCEPT_IN_OR_AS_A_CLASSROOM`
                        - Set the lab boolean variable to true: `lab_zone_b = TRUE` 
                    - Check if any of the space types are computer room: `if space_b.lighting_space_type == "COMPUTER_ROOM":`
                        - Set the computer room boolean variable to true: `computer_room_zone_b = TRUE`
                    - For each value in the occupant_multiplier_schedule: `For i in range(8760):`
                        - Calculate EFLHs for the annual schedule, start by summing each hour of the year: `sum_occ_sch = sum_occ_sch + space_b.occupant_multiplier_schedule(i)`
                    - Calculate EFLHS * Space Area for the space: `sum_occ_area = sum_occ_sch * space_b.floor_area`
                    - Calculate total floor area across spaces: `total_space_floor_area = total_space_floor_area + space_b.floor_area`
                - Calculate the weighted average occupancy EFLHs for the zone: `zone_b_weighted_average_occ_EFLHS = sum_occ_area/total_space_floor_area`
                
                - Create a list with the hvac_id_b, hvac_type_b, floor number, EFLHs, computer_room_zone_b, and labs_zone_b for the zone: `zone_b_descriptor_list = [hvac_id_b, hvac_type_b, zone_floor_number_b, zone_b_weighted_average_occ_EFLHS, computer_room_zone_b, labs_zone_b]`
                - Add the list of descriptors to a dictionary with the zone id as the key, start with empty list: `zone_info_b_dict[zone_b.id] = list()`
                - Add the list of descriptors to a dictionary with the zone id as the key: `zone_info_b_dict[zone_b.id].extend(zone_b_descriptor_list)`
            
            # Loop through each floor to check if G3.1.1 c applies to any HVAC systems in terms of spaces (zones?) exceeding on average other zone occupancy by more than 40 EFLHs
            - Convert the list of floor_list_b associated with the zones to a set and the back to a list to eliminate duplicates: `floor_list_b = list(set(floor_list_b))`
            - for each floor_b in floor_list_b: `for floor_b in floor_list_b:`
                - Reset the counter: `counter = 0`
                - Reset EFLHs adder variable: `EFLHs = 0`
                - Get list of the zones on the floor (i.e. get list of the keys associated with the floor): `list_of_zones = [key for key, list_of_values in zone_info_b_dict.items() if floor_b in list_of_values]`
                - For each zone_b in list_of_zones: `for zone_b in list_of_zones:`
                    - Get list of descriptors for the zone from the dictionary (created above) zone_info_b_dict: `zone_info_list_b = zone_info_b_dict(zone_b)`
                    - Check if the hvac system is system type 5,6,7,8 HVAC : `if zone_info_list_b[1] in ["SYS-5", "SYS-6", "SYS-7", "SYS-8", "SYS-7a", "SYS-8a","SYS-5b", "SYS-6b", "SYS-7b", "SYS-7c"]:`
                        - Create list of hvac system ids on floor that are system type 5,6,7,8: `floor_hvac_sys_type_IDs_list = floor_hvac_sys_type_IDs_list.append(zone_info_list_b[0])`
                    - Check if the hvac system is system type 5 or 7 HVAC : `if zone_info_list_b[1] in ["SYS-5", "SYS-7", "SYS-7a", "SYS-5b",  "SYS-7b", "SYS-7c"]:`
                        - Create list of hvac system ids that are 5 or 7 on floor: `floor_hvac_sys_type_IDs_5_7_list = floor_hvac_sys_type_IDs_5_7_list.append(zone_info_list_b[0])`
                - Convert the list of floor_hvac_sys_type_IDs_list associated with the floor to a set and the back to a list to eliminate duplicates: `floor_hvac_sys_type_IDs_list = list(set(floor_hvac_sys_type_IDs_list))`
                - Convert the list of floor_hvac_sys_type_IDs_5_7_list associated with the floor to a set and the back to a list to eliminate duplicates: `floor_hvac_sys_type_IDs_5_7_list = list(set(floor_hvac_sys_type_IDs_5_7_list))`
                
                # Check if there are 2 systems of type 5 or 7 and if so determine if it is because there are labs and determine which is associated with labs
                - Check if there are 2 system type 5 or 7 on the floor to see if the lab exception is applicable: `if len(floor_hvac_sys_type_IDs_5_7_list) == 2:`
                    - Reset lab_sys_b_applicability_flag to FALSE: `lab_sys_b_applicability_flag = FALSE`
                    - Reset h counter: `h = 0`
                    - Reset p counter: `p = 0`                   
                    - Reset y counter: `y = 0`
                    - Reset j counter: `j = 0`
                    - For each zone_b in list_of_zones: `for zone_b in list_of_zones:`
                        - Get list of descriptors for the zone from the dictionary (created above) zone_info_b_dict: `zone_info_list_b = zone_info_b_dict(zone_b)`
                        - Check if the zone is associated with the first of the two system type 5 or 7 on the floor: `if zone_info_list_b[0] = floor_hvac_sys_type_IDs_5_7_list[0]:`
                            - Count the number of zones: `h = h + 1`
                            - Check if there are labs associated with the zone: `if zone_info_list_b[5] = TRUE:`
                                - Include the zone in a count: `y = y + 1`
                        - Check if the zone is associated with the second of the two system type 5,6,7,8 on the floor: `if zone_info_list_b[0] = floor_hvac_sys_type_IDs_5_7_list[1]:`
                            - Count the number of zones: `p = p + 1`
                            - Check if there are labs associated with the zone: `if zone_info_list_b[5] = TRUE:`
                                - Include the zone in a count: `j = j + 1`
                    - Determine which HVAC system serves labs to comply with G3.1.1(d), the number of zones equals the number of zones with labs: `if h = y:`
                        - Set lab_sys_b equal to the system id: `lab_sys_b = floor_hvac_sys_type_IDs_5_7_list[0]`
                        - Set nonlab_sys_b equal to system id:  `nonlab_sys_b = floor_hvac_sys_type_IDs_5_7_list[1]`
                            - Else if the number of zones equals the number of zones with labs for the second system: `if p = j:`
                                - Set lab_sys_b equal to the system id: `lab_sys_b = floor_hvac_sys_type_IDs_5_7_list[1]`
                                - Set nonlab_sys_b equal to system id:  `nonlab_sys_b = floor_hvac_sys_type_IDs_5_7_list[0]`
                    
                    - Check if lab_sys_b is equal to none, set variable to true if equals "": `if lab_sys_b  == "":`
                        - Set lab_sys_b_applicability_flag to TRUE: `lab_sys_b_applicability_flag = TRUE`
                # Check that there are not more than expected system types 5,6,7, and 8. If there are no unexpected systems then proceed with checking if there are any system 3 or 4s as a result of EFLHs
                - Check if that there are not none or more than 2 system types 5,6,7,8 and that the lab_sys_b_applicability_flag equals FALSE: `if len(floor_hvac_sys_type_IDs_list) < 3 AND len(floor_hvac_sys_type_IDs_list) != 0 AND lab_sys_b_applicability_flag == FALSE`
                    - For each zone_b in list_of_zones: `for zone_b in list_of_zones:`
                        - Get list of values for the zone from the dictionary zone_info_b_dict: `zone_info_list_b = zone_info_b_dict(zone_b)`
                        - Check if the HVAC system is 3,4,5,6,7,8 and not serving a computer room and is not the lab system: `if zone_info_list_b[1] in ["SYS-3","SYS-3a","SYS-3b","SYS-3c" "SYS-4", "SYS-5", "SYS-6", "SYS-7", "SYS-8", "SYS-7a", "SYS-8a","SYS-5b", "SYS-6b", "SYS-7b", "SYS-7c"] AND zone_info_list_b[4] == FALSE AND zone_info_list_b[4] != lab_sys_b:`
                            - Increase counter: `counter = counter + 1`
                            - Add to the EFLHs: `EFLHs = EFLHs + zone_info_list_b[3]`
                    - Set counter value for calculations below: `counter = counter -1`
                    - Calculate EFLHs average for HVAC systems 3,4,5,6,7,8 not serving computer rooms: `EFLHs_average = EFLHs/counter`
                    - For each zone_b in list_of_zones: `for zone_b in list_of_zones:`
                        - Get list of values for the zone from the dictionary zone_info_b_dict: `zone_info_list_b = zone_info_b_dict(zone_b)`
                        - Check if the HVAC system is 3 or 4 and not a computer room: `if zone_info_list_b[1] in ["SYS-3","SYS-3a","SYS-3b","SYS-3c","SYS-4"] AND zone_info_list_b[4] == FALSE:`
                            - Check if the zone meets G3.1.1 c, schedules that differ by more than 40 equivalent full load hrs/week from other spaces: `if abs(((EFLHs-zone_info_list_b[3])/counter)-zone_info_list_b[3]) > 40:`
                                - Set applicability flag: `rule_applicability_check = TRUE`
                                - Add to list of applicable zones: `applicable_zones_G3.1.1c_40_EFLHs_list_b = applicable_zones_G3.1.1c_40_EFLHs_list_b.append(zone_b)`
                                           


**[Back](../_toc.md)**