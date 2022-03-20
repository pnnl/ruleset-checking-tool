# get_HVAC_systems_primarily_serving_comp_rooms  

**Description:** Returns a list of HVAC systems in which greater than 50% of the area served by the HVAC system is computer room space.  

**Inputs:**  
- **P-RMR**: To develop a list of HVAC systems in which greater than 50% of the area served by the HVAC system is computer room space.    

**Returns:**  
- **hvac_systems_primarily_serving_comp_rooms_list_p**: A list of hvac systems in which greater than 50% of the area served by the HVAC system is computer room space.    
 
**Function Call:**  

1. hvac_zone_list_w_area_dictionary()  

## Logic:   
- Get dictionary list of zones and the total floor area served by each HVAC system: `hvac_zone_list_w_area_dict_p = hvac_zone_list_w_area_dictionary (P_RMR)`
- For each hvac_p in the P_RMR: `for hvac_p in P_RMR...HeatingVentilationAirConditioningSystem:`
    - Get the total floor area served by the hvac system: `hvac_sys_total_floor_area_p = hvac_zone_list_w_area_dict_p[hvac_p.id]["TOTAL_AREA"]`
    - Reset hvac system includes computer room boolean variable: `hvac_system_serves_computer_room_space = FALSE` 
    - Reset hvac_sys_computer_room_floor_area variable: `hvac_sys_computer_room_floor_area = 0`
    - Get list of zones served by hvac_p: `hvac_zone_list_p = hvac_zone_list_w_area_dict_p[hvac_p.id]["ZONE_LIST"]`
    - For each zone_p in hvac_zone_list_p: `for zone_p in hvac_zone_list_p:`
        - For each space in zone: `for space_p in zone_p.Spaces:`        
            - Check if space is of type computer room, if yes then set the hvac system has computer room boolean variable to true and add the floor area to the total computer room floor area variable for the hvac system: `if space_p.lighting_space_type in ["COMPUTER_ROOM"]:`
                - Set hvac system serves computer room boolean variable to true: `hvac_system_serves_computer_room_space = TRUE`
                - Get space floor_area: `space_floor_area = space_p.floor_area`
                - Add floor area to hvac_sys_computer_room_floor_area: `hvac_sys_computer_room_floor_area = hvac_sys_computer_room_floor_area + space_floor_area`   
    - Check if the hvac system serves computer room boolean variable equals TRUE, if true then proceed otherwise loop to next hvac system: `if hvac_system_serves_computer_room_space == TRUE:`
        - Check if computer room floor area is greater than 50% of the total floor area served by the hvac system, if yes then carry on with the check: `if hvac_sys_computer_room_floor_area/hvac_sys_total_floor_area_p > 0.5:` 
            - Add to the list of hvac systems, hvac_systems_primarily_serving_comp_rooms_list_p: `hvac_systems_primarily_serving_comp_rooms_list_p = hvac_systems_primarily_serving_comp_rooms_list_p.append(hvac_p)`          

**Returns** `return hvac_systems_primarily_serving_comp_rooms_list_p`

**[Back](../_toc.md)**