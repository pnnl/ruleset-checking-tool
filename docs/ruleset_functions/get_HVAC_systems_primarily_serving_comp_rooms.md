# get_HVAC_systems_primarily_serving_comp_rooms  

**Description:** Returns a list of HVAC systems in which greater than 50% of the area served by the HVAC system is computer room space.  

**Inputs:**  
- **RMD**: To develop a list of HVAC systems in which greater than 50% of the area served by the HVAC system is computer room space.    

**Returns:**  
- **hvac_systems_primarily_serving_comp_rooms_list**: A list of hvac systems in which greater than 50% of the area served by the HVAC system is computer room space.    
 
**Function Call:**  

1. get_hvac_zone_list_w_area()  

## Logic:   
- Get dictionary list of zones and the total floor area served by each HVAC system: `hvac_zone_list_w_area_dict = get_hvac_zone_list_w_area(RMD)`
- For each hvac_x in the X_RMD: `for hvac in RMD...HeatingVentilatingAirConditioningSystem:`
    - Get the total floor area served by the hvac system: `hvac_sys_total_floor_area = hvac_zone_list_w_area_dict_x[hvac_x.id]["total_area"]`
    - Reset hvac system includes computer room boolean variable: `hvac_system_serves_computer_room_space = FALSE` 
    - Reset hvac_sys_computer_room_floor_area variable: `hvac_sys_computer_room_floor_area = 0`
    - Get list of zones served by hvac_x: `hvac_zone_list = hvac_zone_list_w_area_dict_x[hvac.id]["zone_list"]`
    - For each zone_x in hvac_zone_list_x: `for zone in hvac_zone_list:`
        - For each space in zone: `for space in zone.Spaces:`        
            - Check if space is of type computer room, if yes then set the hvac system has computer room boolean variable to true and add the floor area to the total computer room floor area variable for the hvac system: `if space_x.lighting_space_type == "COMPUTER_ROOM":`
                - Set hvac system serves computer room boolean variable to true: `hvac_system_serves_computer_room_space = TRUE`
                - Get space floor_area: `space_floor_area = space_x.floor_area`
                - Add floor area to hvac_sys_computer_room_floor_area: `hvac_sys_computer_room_floor_area += space_floor_area`   
    - Check if the hvac system serves computer room boolean variable equals TRUE, if true then proceed otherwise loop to next hvac system: `if hvac_system_serves_computer_room_space == TRUE:`
        - Check if computer room floor area is greater than 50% of the total floor area served by the hvac system, if yes then carry on with the check: `if hvac_sys_computer_room_floor_area/hvac_sys_total_floor_area > 0.5:` 
            - Add to the list of hvac systems, hvac_systems_primarily_serving_comp_rooms_list: `hvac_systems_primarily_serving_comp_rooms_list = hvac_systems_primarily_serving_comp_rooms_list.append(hvac)`          

**Returns** `return hvac_systems_primarily_serving_comp_rooms_list`

**[Back](../_toc.md)**
