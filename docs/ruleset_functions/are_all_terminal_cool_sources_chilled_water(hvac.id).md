# are_all_terminal_cool_sources_chilled_water   

**Description:** Returns TRUE if the cool source associated with all terminal units associated with the hvac system is CHILLED_WATER. It returns FALSE if any terminal unit has a cool source other than CHILLED_WATER.   

**Inputs:**  
- **B-RMR**: To evaluate if the cool source associated with all terminal units associated with the hvac system is CHILLED_WATER.   
- **hvac_b.id**: The id of the hvac system to evaluate.  

**Returns:**  
- **are_all_terminal_cool_sources_chilled_water**: The function returns TRUE if the cool source associated with all terminal units associated with the hvac system is CHILLED_WATER. It returns FALSE if any terminal unit has a cool source other than CHILLED_WATER.  
 
**Function Call:**  
1. get_list_of_terminal_units_served_by_hvac_sys()      

## Logic: 
- Get list of the terminal units associated with the hvac system: `list_of_terminal_units_served_by_hvac_sys = get_list_of_terminal_units_served_by_hvac_sys(B_RMR, hvac_b.id)`  
- Check if there is at least one terminal unit in the list: `if len(list_of_terminal_units_served_by_hvac_sys) >= 1:`
    - For each terminal_b in the list of terminal units: `For terminal_b in list_of_terminal_units_served_by_hvac_sys:`  
        - Create an object for the terminal unit: `terminal_b = terminal_b.id`  
        - Check if the cool source associated with the terminal unit equals CHILLED_WATER: `if terminal_b.cooling_source == "CHILLED_WATER": are_all_terminal_cool_sources_chilled_water = TRUE`
        - Else: `Else: are_all_terminal_cool_sources_chilled_water = FALSE`
        - Check if are_all_terminal_cool_sources_chilled_water equals False, if it does then leave the loop: `if are_all_terminal_cool_sources_chilled_water == FALSE:`
            - Leave the loop: `break`
        - Else: continue looping: `Else:`   
- Else: `Else: are_all_terminal_cool_sources_chilled_water = FALSE`  

**Returns** `return are_all_terminal_cool_sources_chilled_water`  

**[Back](../_toc.md)**