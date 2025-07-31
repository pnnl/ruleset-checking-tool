# are_all_terminal_types_VAV

**Description:** Returns TRUE if all of the terminal unit types input to this function are variable air volume (VAV) or are equal to null. It returns FALSE if any of the terminal units are of a type other than variable air volume (VAV) or null.   

**Inputs:**  
- **B-RMR**: To evaluate if the terminal unit types are variable air volume (VAV).    
- **terminal_unit_id_list**: List of terminal units to assess.  

**Returns:**  
- **are_all_terminal_types_VAV**: The function returns TRUE if all of the terminal unit types input to this function are variable air volume (VAV) or are equal to null. It returns FALSE if any of the terminal units are of a type other than variable air volume (VAV) or null.      
 
**Function Call:**  None        

## Logic:   
- Set are_all_terminal_types_VAV = TRUE: `are_all_terminal_types_VAV = TRUE`  
- For each terminal_b in the list of terminal units: `For terminal_b in terminal_unit_id_list:`  
    - Create an object for the terminal unit: `terminal_b = terminal_b.id`  
    - Check if the terminal unit type is not variable air volume (VAV) or Null: `if terminal_b.type != "VARIABLE_AIR_VOLUME" AND terminal_b.type != Null:`  
        - Set are_all_terminal_types_VAV = FALSE: `are_all_terminal_types_VAV = FALSE`
        - Leave the loop: `break`  

**Returns** `return are_all_terminal_types_VAV` 

**Notes:**  
1. This function is always called after "if is_hvac_sys_fan_sys_VSD(B_RMR, hvac_b.id) == TRUE", so we are not requiring that VAV is defined both on system and terminal level. 

**[Back](../_toc.md)**