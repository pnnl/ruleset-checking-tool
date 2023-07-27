# get_zones_computer_rooms  

**Description:** Returns a dictionary with the zones that have at least one computer room space associated with them in the RMR as the keys. The values associated with each key are in a list form. The list associated with each key contains the computer room floor area as the first item in the list and the total zone floor area as the second item in the list.  

**Inputs:**  
- **U,P, or B-RMR**: To determine if any of the zones have computer rooms associated with them in the RMR and to perform the evaluation to determine the computer room floor area and the total zone floor area .  

**Returns:**  
- **zones_with_computer_room_dict_x**: A dictionary with the zones that have at least one computer room space associated with them in the RMR as the keys. The values associated with each key are in a list form. The list associated with each key contains the computer room floor area as the first item in the list and the total zone floor area as the second item in the list.   
 
**Function Call:** 
1. is_space_a_computer_room()    

## Logic:   
- Create object from the RMR input into the function: `X_RMR = RMR`
- Create empty dictionary: `zones_with_computer_room_dict_x = dict()`
- For each zone in X_RMR: `for zone_x in X_RMR...Zone:`
    - Reset zone has computer room boolean variable: `zone_has_computer_room_check = FALSE` 
    - Reset zone_computer_room_floor_area variable: `zone_computer_room_floor_area = 0`
    - Reset total_zone_floor_area variable: `total_zone_floor_area = 0`
    - For each space in zone: `for space_x in zone_x.Spaces:`        
        - Get space floor_area: `space_floor_area = space_x.floor_area`
        - Check if space is of type computer room, if yes then set the zone has computer room boolean variable to true and add the floor area to the total computer room floor area variable for the zone: `if is_space_a_computer_room(RMR,space_x) == true:`  
            - Set zone has computer room boolean variable to true: `zone_has_computer_room_check = TRUE`
            - Add floor area to zone_computer_room_floor_area: `zone_computer_room_floor_area = zone_computer_room_floor_area + space_floor_area`
        - Add floor area to total_zone_floor_area: `total_zone_floor_area = total_zone_floor_area + space_floor_area`  
    - Check if the zone has computer room boolean variable equals TRUE, if true then add to list of zones: `if zone_has_computer_room_check == TRUE:`
        - Add to zone as dictionary key and list of floor areas as the associated value: `zones_with_computer_room_dict_x[zone_x.id] = {zone_computer_room_floor_area: zone_computer_room_floor_area, total_zone_floor_area: total_zone_floor_area}`  

**Returns** `return zones_with_computer_room_dict_x`

**[Back](../_toc.md)**