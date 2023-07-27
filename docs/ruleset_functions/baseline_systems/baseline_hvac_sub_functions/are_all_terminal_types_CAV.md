# are_all_terminal_types_CAV

**Description:** Returns TRUE if all of the terminal unit types input to this function are constant air volume (CAV) or if this data element is undefined. It returns FALSE if any of the terminal units are of a type other than constant air volume (CAV).   

**Inputs:**  
- **B-RMR**: To evaluate if the terminal unit types are constant air volume (CAV).    
- **terminal_unit_id_list**: List of terminal units to assess.  

**Returns:**  
- **are_all_terminal_types_CAV**: The function returns TRUE if all of the terminal unit types input to this function are constant air volume (CAV). It returns FALSE if any of the terminal units are of a type other than constant air volume (CAV).      
 
**Function Call:**  None        

## Logic:   
- Set are_all_terminal_types_CAV = TRUE: `are_all_terminal_types_CAV = TRUE`  
- For each terminal_b in the list of terminal units: `For terminal_b in terminal_unit_id_list:`  
    - Create an object for the terminal unit (however the RCT accomplishes this): `terminal_b = terminal_b.id`  
    - Check if the terminal unit type is not constant air volume (CAV) and also not equal to Null: `if terminal_b.type != "CONSTANT_AIR_VOLUME" or terminal_b.type != Null:`  
        - Set are_all_terminal_types_CAV = FALSE: `are_all_terminal_types_CAV = FALSE`
        - Leave the loop: `break`  

**Returns** `return are_all_terminal_types_CAV`   

**[Back](../../../_toc.md)**