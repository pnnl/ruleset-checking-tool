# get_zones_computer_rooms  

**Description:** Get the list of zones that have at least one computer room space associated with them in the P-RMR.  

**Inputs:**  
- **P-RMR**: To determine if any of the zones have computer rooms associated with them in the P-RMR.  

**Returns:**  
- **zones_with_computer_room_list_p**: A list that saves all zones that have at least one computer room associated with them.  
 
**Function Call:** None  

## Logic:   
- For each zone in P_RMR: `for zone_p in P_RMR..Zone:`
    - Reset zone has computer room boolean variable: `zone_has_computer_room_check = FALSE` 
    - For each space in zone: `for space_p in zone_p.Spaces:`
        - Check if space is of type computer room, if yes then set zone has computer room boolean variable to true: `if space_p.lighting_space_type in ["COMPUTER_ROOM"]:`
            - Set zone has computer room boolean variable: `zone_has_computer_room_check = TRUE`
    - Check if the zone has computer room boolean variable equals TRUE, if true then add to list of zones: `if zone_has_computer_room_check == TRUE:`
        - Add to list of zones with computer room(s): `zones_with_computer_room_list_p = zones_with_computer_room_list_p.append(zone_p.id)`  

**Returns** `return zones_with_computer_room_list_p`

**[Back](../_toc.md)**