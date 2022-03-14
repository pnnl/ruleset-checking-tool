# PLEASE DO NOT REVIEW get_zones_G3.1.1c_40_EFLHs
# IN PROGRESS - I PLAN TO MAKE MAJOR CHANGES

**Description:** Get the list of zones in which baseline HVAC system type 3 or 4 has been used for spaces (zones???) that differ by more than 40 equivalent full load hrs/week from other spaces (zones???) served by the system.   

**Inputs:**  
- **B_RMR**: To determine which (if any) baseline HVAC system type 3 or 4 has been used for spaces (zones???) that differ by more than 40 equivalent full load hrs/week from other spaces (zones???) served by the system.   

**Returns:**  
- **applicable_zones_G3.1.1c_40_EFLHs_dict_b**: A dictionary that saves all zones that have baseline HVAC system type 3 or 4 modeled in the baseline because the zone differs by more than 40 equivalent full load hrs/week from other spaces (zones???) served by the predominant HVAC system. The associated hvac id is saved as the value associated with the zone id key.  
 
**Function Call:**  

1. get_baseline_system_types  

# IN PROGRESS - I PLAN TO MAKE MAJOR CHANGES

## Logic:  
- For each building_segment_b in B_RMR: `for building_segment_b in B_RMR..BuildingSegment:`
    - Set function applicability flag to FALSE: `hvac_sys_G3.1.1c_applies_check = FALSE`  
    - Get dictionary of baseline hvac system types and ids from function: `baseline_hvac_sys_type_ids_dict_b = get_baseline_system_types(B_RMR)`
    - Check if there is an HVAC system of type 5, 6, 7, or 8 associated with the building segment, if so then carry on, if not skip building segment: `if all (k in baseline_hvac_sys_type_ids_dict_b for k in ("SYS-5", "SYS-6", "SYS-7", "SYS-8", "SYS-7a", "SYS-8a","SYS-5b", "SYS-6b", "SYS-7b", "SYS-7c")):`    
        - For each zone_b in building_segment_b.zones: `For zone_b in building_segment_b.zones:`
            - Get the floor number that the zone is associated with: `zone_floor_number_b = zone_b.zone_floor_number`
            - Add to the list of floors in the building segment, keep adding as the code loops through the zones: `floor_list_b = floor_list_b.append(zone_floor_number_b)`    

        This is a stuggle because a system 5, 6,7, or 8 could serve more than one floors if the floors have identical thermal blocks. If floors are identical then we can do this per floor. Thsi means that we should only look at one floor
        
        Potential functions to create
        Returns list of hvac systems associated with a zone (do all zones in RMR and make dictionary)
        Returns list of zones with labs
        Returns equivalent full-load hours per week from other spaces served by the system, are considered to differ significantly (is this on average), so a functions that returns average EFLHs per week?
        Returns list of dictionary of floor as key and list of zones as values


        Potential functions to use
        longest_fan_schedule
        get_hvac_zone_list_w_area Returns hvac_zone_list_w_area_dictionary: A dictionary that saves the list of zones and the total floor area served by each HVAC system, i.e. {hvac_system_1.id: {"ZONE_LIST": [zone_1.id, zone_2.id, zone_3.id], "TOTAL_AREA": 10000}, hvac_system_2.id: {"ZONE_LIST": [zone_10.id], "TOTAL_AREA": 500}}
        get list of zones with computer rooms
       

        
        Create a dictionary with zone ID as key and a list with zone descriptor information (including the HVAC system with the longest fan schedule) for access later in the logic. This dictionary will be used later in the logic.
        - for each zone_b in the building_segment_b: `for zone_b in building_segment_b.zones:`
            - Reset list of hvac systems associated with the zone: `heating_ventilation_air_conditioning_systems_list_b = []`   
            Gets the floor number associated with the zone
            
            Gets a list of the hvac systems associated with the zone
            - For each terminal unit associated with the zone: `for terminal_b in zone_b.terminals:`
                - Get the served_by_heating_ventilation_air_conditioning_systems: `heating_ventilation_air_conditioning_systems_b = terminal_b.served_by_heating_ventilation_air_conditioning_systems`
                - Add to list of heating_ventilation_air_conditioning_systems_list_b as the code loops through the terminal units: `heating_ventilation_air_conditioning_systems_list_b = heating_ventilation_air_conditioning_systems_list_b.append(heating_ventilation_air_conditioning_systems_b)`                
            - Convert the list of heating_ventilation_air_conditioning_systems_list_b associated with the zone to a set and the back to a list to eliminate duplicates after looping through terminal units: `heating_ventilation_air_conditioning_systems_list_b = list(set(heating_ventilation_air_conditioning_systems_list_b))`   
            Determine which hvac system associated with the zone has the longest fan schedule as that will be the system to compare to the proposed in terms of fan schedule per PNNL PRM RM (note in the baseline per the rules of App G there would only be one HVAC system per zone so for the baseline this is not necessary unless an error was made in modeling the baseline HVAC systems)
            - For each hvac_b in heating_ventilation_air_conditioning_systems_list_b: `for hvac_b in heating_ventilation_air_conditioning_systems_list_b:`
                - For each fan_system_b in hvac_b: `for fan_system_b in hvac_b.fan_systems:` Need to modify for one fan system per hvac system
                    - Reset fan_schedule_b to zero for each zone: `fan_schedule_b =0`       
                    - For each value in the fan_schedule_b.operating_schedule: `for x in range(8760):`
                        - Sum value for each hour in fan_schedule_b.operating_schedule: `fan_schedule_b = fan_schedule_b + fan_system_b.operating_schedule(x)`
                    - Add sum to dictionary with fan_system_b.id as key and fan_schedule_b as value: `hvac_fan_schedule_dict[fan_system_b.ID] = fan_schedule_b`
                - Find the key for the fan_system_b with the longest schedule associated with hvac_b: `longest_sch_fan_system = max(hvac_fan_schedule_dict, key = hvac_fan_schedule_dict.get())`
                - Get max fan_schedule_b value for the longest_sch_fan_system key: `max_fan_sch_value = hvac_fan_schedule_dict[longest_sch_fan_system]`
                - Add max_fan_sch_value to dictionary with hvac_b.id as key: `zone_hvac_fan_schedule_dict[hvac_b.ID] = max_fan_sch_value`                     
            - Find the key for the hvac_b with the longest fan operating schedule for the zone: `longest_sch_fan_system = max(zone_hvac_fan_schedule_dict, key = zone_hvac_fan_schedule_dict.get())`
            - Get max fan operating schedule value for the longest_sch_fan_system key for the zone: `max_fan_sch_value = zone_hvac_fan_schedule_dict[longest_sch_fan_system]`
            - Set hvac_b equal to the hvac system with the longest fan operating schedule for the zone: `hvac_b = longest_sch_fan_system`             
            - Get the HVAC system type: `hvac_type_b = baseline_hvac_sys_type_ids_dict_b.keys()[list(baseline_hvac_sys_type_ids_dict_b.values()).index(hvac_b.id)]`
            - Store the HVAC system id as a variable::  `hvac_id_b = hvac_b.id`   
            Check if there are lab spaces or computer room spaces associated with the zone and calculate the weighted average EFLHs for the zone based on space occupancy schedules
             - Reset the computer room boolean variable to false, indicates if zone contains computer rooms spaces: `computer_room_zone_b = FALSE`
            - Reset the labs boolean variable to false, indicate if zone includes any lab spaces: `all_labs_zone_b = FALSE`
            - Reset total_zone_floor_area to 0, used for summing space floor area across the zone: `total_zone_floor_area = 0`
            - Reset sum_occ_area to 0, used for calculating EFLHs occ sch for zone" `sum_occ_area = 0`
            - For each space_b in zone_b: `for space_b in zone_b:`   
                Check if any spaces associated with the zone are labs or computer rooms
                - Check if any spaces associated with the zone_b are labs: `if space_b.lighting_space_type == LABORATORY_EXCEPT_IN_OR_AS_A_CLASSROOM`
                    - Set the lab boolean variable to true: `lab_zone_b = TRUE` 
                - Check if any of the space types are computer room: `if space_b.lighting_space_type == "COMPUTER_ROOM":`
                    - Set the computer room boolean variable to true: `computer_room_zone_b = TRUE`   
                Calculate the zone occupancy schedule EFLHs
                - Reset sum_occ_sch to 0 as the code loops through the spaces: `sum_occ_sch = 0`
                - For each value in the occupant_multiplier_schedule: `For i in range(8760):`
                    - Calculate EFLHs for the annual schedule, start by summing each hour of the year: `sum_occ_sch = sum_occ_sch + space_b.occupant_multiplier_schedule(i)`
                - Calculate EFLHS * Space Area for the space and keep a running tally for the zone: `sum_occ_area = sum_occ_area + (sum_occ_sch * space_b.floor_area)`
                - Calculate total floor area across the spaces in the zone: `total_zone_floor_area = total_zone_floor_area + space_b.floor_area`
            - Calculate the weighted average occupancy EFLHs for the zone: `zone_b_weighted_average_occ_EFLHS = sum_occ_area/total_zone_floor_area`   
            Create a dictionary with zone ID as key and a list with zone descriptor information
            - Create a list with the hvac_id_b, hvac_type_b, floor number, occ EFLHs, computer_room_zone_b, and labs_zone_b for the zone: `zone_b_descriptor_list = [hvac_id_b, hvac_type_b, zone_floor_number_b, zone_b_weighted_average_occ_EFLHS, computer_room_zone_b, labs_zone_b]`
            - Add the list of descriptors to a dictionary with the zone id as the key, start with empty list: `zone_info_b_dict[zone_b.id] = list()`
            - Add the list of descriptors to a dictionary with the zone id as the key: `zone_info_b_dict[zone_b.id].extend(zone_b_descriptor_list)`   
            
        After looping through all zones and creating the dictionary as described above, loop through each floor to check if G3.1.1 c applies to any HVAC systems in terms of spaces (zones?) exceeding on average other zone occupancy schedule by more than 40 EFLHs
        - Convert the list of floor_list_b associated with the zones to a set and the back to a list to eliminate duplicates: `floor_list_b = list(set(floor_list_b))`
        - for each floor_b in floor_list_b: `for floor_b in floor_list_b:`
            - Reset the counter: `counter = 0`
            - Reset EFLHs adder variable: `EFLHs = 0`
            - Get list of the zones on the floor (i.e. get list of the keys associated with the floor): `list_of_zones = [key for key, list_of_values in zone_info_b_dict.items() if floor_b in list_of_values]`
            - For each zone_b in list_of_zones: `for zone_b in list_of_zones:`
                - Get list of descriptors for the zone from the dictionary (created above) zone_info_b_dict: `zone_info_list_b = zone_info_b_dict(zone_b)`
                - Check if the hvac system is system type 5,6,7,8 HVAC : `if zone_info_list_b[1] in ["SYS-5", "SYS-6", "SYS-7", "SYS-8", "SYS-7a", "SYS-8a","SYS-5b", "SYS-6b", "SYS-7b", "SYS-7c"]:`
                    - Add to list of hvac system ids on floor that are system type 5,6,7,8: `floor_hvac_sys_type_IDs_list = floor_hvac_sys_type_IDs_list.append(zone_info_list_b[0])`
                - Check if the hvac system is system type 5 or 7 HVAC : `if zone_info_list_b[1] in ["SYS-5", "SYS-7", "SYS-7a", "SYS-5b",  "SYS-7b", "SYS-7c"]:`
                    - Create list of hvac system ids that are 5 or 7 on floor: `floor_hvac_sys_type_IDs_5_7_list = floor_hvac_sys_type_IDs_5_7_list.append(zone_info_list_b[0])`
            - Convert the list of floor_hvac_sys_type_IDs_list associated with the floor to a set and the back to a list to eliminate duplicates: `floor_hvac_sys_type_IDs_list = list(set(floor_hvac_sys_type_IDs_list))`
            - Convert the list of floor_hvac_sys_type_IDs_5_7_list associated with the floor to a set and the back to a list to eliminate duplicates: `floor_hvac_sys_type_IDs_5_7_list = list(set(floor_hvac_sys_type_IDs_5_7_list))`   
                
            Check if there are 2 systems of type 5 or 7 and if so determine if it is because there are labs and determine which is associated with labs
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
                        - Check if there are labs associated with the zone: `if zone_info_list_b[5] == TRUE:`
                            - Include the zone in a count: `y = y + 1`
                    - Check if the zone is associated with the second of the two system type 5 or 7 on the floor: `if zone_info_list_b[0] = floor_hvac_sys_type_IDs_5_7_list[1]:`
                        - Count the number of zones: `p = p + 1`
                        - Check if there are labs associated with the zone: `if zone_info_list_b[5] == TRUE:`
                            - Include the zone in a count: `j = j + 1`
                - Determine which HVAC system serves labs to comply with G3.1.1(d), the number of zones equals the number of zones with labs: `if h = y:`
                    - Set lab_sys_b equal to the system id: `lab_sys_b = floor_hvac_sys_type_IDs_5_7_list[0]`
                    - Set nonlab_sys_b equal to system id:  `nonlab_sys_b = floor_hvac_sys_type_IDs_5_7_list[1]`
                - Else if the number of zones equals the number of zones with labs for the second system (else, do nothing): `elif p = j:`
                    - Set lab_sys_b equal to the system id: `lab_sys_b = floor_hvac_sys_type_IDs_5_7_list[1]`
                    - Set nonlab_sys_b equal to system id:  `nonlab_sys_b = floor_hvac_sys_type_IDs_5_7_list[0]`            
                - Check if lab_sys_b is equal to none, set variable to true if equals "": `if lab_sys_b  == "":`
                    - Set lab_sys_b_applicability_flag to TRUE: `lab_sys_b_applicability_flag = TRUE`   
            Check that there are not more than expected system types 5,6,7, and 8. If there are no unexpected systems then proceed with checking if there are any system 3 or 4s as a result of EFLHs
            - Check if there are not none or more than 2 system types 5,6,7,8 and that the lab_sys_b_applicability_flag equals FALSE: `if len(floor_hvac_sys_type_IDs_list) < 3 AND len(floor_hvac_sys_type_IDs_list) != 0 AND lab_sys_b_applicability_flag == FALSE`
                - For each zone_b in list_of_zones: `for zone_b in list_of_zones:`
                    - Get list of values for the zone from the dictionary zone_info_b_dict: `zone_info_list_b = zone_info_b_dict(zone_b)`
                    - Check if the HVAC system is 3,4,5,6,7,8 and not serving a computer room and is not the lab system: `if zone_info_list_b[1] in ["SYS-3","SYS-3a","SYS-3b","SYS-3c" "SYS-4", "SYS-5", "SYS-6", "SYS-7", "SYS-8", "SYS-7a", "SYS-8a","SYS-5b", "SYS-6b", "SYS-7b", "SYS-7c"] AND zone_info_list_b[4] == FALSE AND zone_info_list_b[4] != lab_sys_b:`
                        - Increase counter: `counter = counter + 1`
                        - Add to the EFLHs: `EFLHs = EFLHs + zone_info_list_b[3]`
                - Set counter value for calculations below: `counter = counter -1`
                - Calculate EFLHs average for HVAC systems 3,4,5,6,7,8 not serving computer rooms or all labs per G3.1.1 d : `EFLHs_average = EFLHs/counter`
                - For each zone_b in list_of_zones: `for zone_b in list_of_zones:`
                    - Get list of values for the zone from the dictionary zone_info_b_dict: `zone_info_list_b = zone_info_b_dict(zone_b)`
                    - Check if the HVAC system is 3 or 4 and not a computer room: `if zone_info_list_b[1] in ["SYS-3","SYS-3a","SYS-3b","SYS-3c","SYS-4"] AND zone_info_list_b[4] == FALSE:`
                        - Check if the zone meets G3.1.1 c, schedules that differ by more than 40 equivalent full load hrs/week from other spaces: `if abs(((EFLHs-zone_info_list_b[3])/counter)-zone_info_list_b[3]) > 40:`
                            - Set applicability flag: `hvac_sys_G3.1.1c_applies_check = TRUE`
                            - Add zone as key to dictionary and hvac system as value: `applicable_zones_G3.1.1c_40_EFLHs_dict_b[zone_b.id] = zone_info_list_b[0]`  
                                           
**Returns** `return applicable_zones_G3.1.1c_40_EFLHs_dict_b`

**[Back](../_toc.md)**