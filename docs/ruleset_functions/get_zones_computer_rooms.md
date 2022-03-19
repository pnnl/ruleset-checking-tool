# get_zones_computer_rooms  

**Description:** Returns a dictionary with the zones that have at least one computer room space associated with them in the P-RMR as the keys. The values associated with each key are in a list form. The list associated with each key contains the computer room floor area as the first item in the list and the total zone floor area as the second item in the list.  

**Inputs:**  
- **P-RMR**: To determine if any of the zones have computer rooms associated with them in the P-RMR and to perform the evaluation to determine the computer room floor area and the total zone floor area .  

**Returns:**  
- **zones_with_computer_room_dict_p**: A dictionary with the zones that have at least one computer room space associated with them in the P-RMR as the keys. The values associated with each key are in a list form. The list associated with each key contains the computer room floor area as the first item in the list and the total zone floor area as the second item in the list.   
 
**Function Call:** None  

## Logic:   
- Create dictionary: `zones_with_computer_room_dict_p = dict()`
- For each zone in P_RMR: `for zone_p in P_RMR...Zone:`
    - Reset zone has computer room boolean variable: `zone_has_computer_room_check = FALSE` 
    - Reset zone_computer_room_floor_area variable: `zone_computer_room_floor_area = 0`
    - Reset total_zone_floor_area variable: `total_zone_floor_area = 0`
    - For each space in zone: `for space_p in zone_p.Spaces:`        
        - Get space floor_area: `space_floor_area = space_p.floor_area * CONVERSION(m2_TO_ft2)`
        - Check if space is of type computer room, if yes then set the zone has computer room boolean variable to true and add the floor area to the total computer room floor area variable for the zone: `if space_p.lighting_space_type in ["COMPUTER_ROOM"]:`
            - Set zone has computer room boolean variable to true: `zone_has_computer_room_check = TRUE`
            - Add floor area to zone_computer_room_floor_area: `zone_computer_room_floor_area = zone_computer_room_floor_area + space_floor_area`
        - Add floor area to total_zone_floor_area: `total_zone_floor_area = total_zone_floor_area + space_floor_area`  
    - Check if the zone has computer room boolean variable equals TRUE, if true then add to list of zones: `if zone_has_computer_room_check == TRUE:`
        - Reset list with computer room floor area and zone total floor area:`floor_areas_list = []`
        - Create list with computer room floor area and zone total floor area: `floor_areas_list = [zone_computer_room_floor_area,total_zone_floor_area]`
        - Add to zone as dictionary key and list of floor areas as the associated value: `zones_with_computer_room_dict_p[zone_p.id] = floor_areas_list`  

**Returns** `return zones_with_computer_room_dict_p`

**[Back](../_toc.md)**