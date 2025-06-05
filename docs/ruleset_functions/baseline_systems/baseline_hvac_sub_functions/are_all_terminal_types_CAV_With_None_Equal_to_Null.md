# are_all_terminal_types_CAV_With_None_Equal_to_Null

**Description:** Returns TRUE if all of the terminal unit types input to this function are constant air volume (CAV). It returns FALSE if any of the terminal units are of a type other than constant air volume (CAV).   

**Inputs:**  
- **B-RMR**: To evaluate if the terminal unit types are constant air volume (CAV).    
- **terminal_unit_id_list**: List of terminal units to assess.  

**Returns:**  
- **aare_all_terminal_types_CAV_With_None_Equal_to_Null**: The function returns TRUE if all of the terminal unit types input to this function are constant air volume (CAV). It returns FALSE if any of the terminal units are of a type other than constant air volume (CAV).      
 
**Function Call:**  None        

## Logic:   
- Set are_all_terminal_types_CAV_With_None_Equal_to_Null = TRUE: `are_all_terminal_types_CAV_With_None_Equal_to_Null = TRUE`  
- For each terminal_b in the list of terminal units: `For terminal_b in terminal_unit_id_list:`  
    - Create an object for the terminal unit (however the RCT accomplishes this): `terminal_b = terminal_b.id`  
    - Check if the terminal unit type is not constant air volume (CAV): `if terminal_b.type != "CONSTANT_AIR_VOLUME":`  
        - Set are_all_terminal_types_CAV_With_None_Equal_to_Null = FALSE: `are_all_terminal_types_CAV_With_None_Equal_to_Null = FALSE`
        - Leave the loop: `break`  

**Returns** `return are_all_terminal_types_CAV_With_None_Equal_to_Null`   

**[Back](../../../_toc.md)**