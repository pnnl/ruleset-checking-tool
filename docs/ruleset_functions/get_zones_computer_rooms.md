## get_zones_computer_rooms

**Description:** Get the list of zones that have computer rooms associated with them in the P-RMR.  

**Inputs:**
- **P-RMR**: To determine if any of the zones have computer rooms associated with them.

**Returns:**
- **applicable_computer_room_list_p**: A list that saves all zones that have computer rooms associated with them.
 
**Function Call:** 


**Logic:**
- For each zone in P_RMR: `for zone_p in P_RMR...zones:`
    - Reset applicability flag: `rule_applicability_check = FALSE` 
    - For each space in zone: `for space_p in zone_p.zones:`
        - Check if space is of type computer room, if yes then set applicability flag to true: `if space_p.lighting_space_type in [COMPUTER_ROOM]:`
            - Set applicability flag: `rule_applicability_check = TRUE`

    **Rule Logic**
    - Check if the applicability flag equals TRUE, if true then add to list of zones: `if rule_applicability_check == TRUE:`
        - Add to list of applicable zones: `applicable_computer_room_list_p = applicable_computer_room_list_p.append(zone_p.id)`

**[Back](../_toc.md)**