# are_all_terminal_types_four_pipe

**Description:** Returns TRUE if the terminal unit type associated with all terminal units associated with the hvac system is FOUR_PIPE_FAN_COIL_UNIT. It returns FALSE if any of the terminal units is of a type other than FOUR_PIPE_FAN_COIL_UNIT.   

**Inputs:**  
- **B-RMR**: To evaluate if the terminal unit type associated with all terminal units associated with the hvac system is FOUR_PIPE_FAN_COIL_UNIT.   
- **hvac_b.id**: The id of the hvac system to evaluate.  

**Returns:**  
- **are_all_terminal_types_four_pipe**: The function returns TRUE if the terminal unit type associated with all terminal units associated with the hvac system is FOUR_PIPE_FAN_COIL_UNIT. It returns FALSE if any of the terminal units is of a type other than FOUR_PIPE_FAN_COIL_UNIT.     
 
**Function Call:**  
1. get_list_of_terminal_units_served_by_hvac_sys()      

## Logic: 
- Get list of the terminal units associated with the hvac system: `list_of_terminal_units_served_by_hvac_sys = get_list_of_terminal_units_served_by_hvac_sys(B_RMR, hvac_b.id)`  
- Check if there is at least one terminal unit in the list: `if len(list_of_terminal_units_served_by_hvac_sys) >= 1:`
    - For each terminal_b in the list of terminal units: `For terminal_b in list_of_terminal_units_served_by_hvac_sys:`  
        - Create an object for the terminal unit: `terminal_b = terminal_b.id`  
        - Check if the terminal unit type is FOUR_PIPE_FAN_COIL_UNIT: `if terminal_b.type == "FOUR_PIPE_FAN_COIL_UNIT": are_all_terminal_types_four_pipe = TRUE`
        - Else: `Else: are_all_terminal_types_four_pipe = FALSE`
        - Check if are_all_terminal_types_four_pipe equals False, if it does then leave the loop: `if are_all_terminal_types_four_pipe == FALSE:`
            - Leave the loop: `break`
        - Else: continue looping: `Else:`  
- Else: `Else: are_all_terminal_types_four_pipe = FALSE`

**Returns** `return are_all_terminal_types_four_pipe`  

**[Back](../_toc.md)**