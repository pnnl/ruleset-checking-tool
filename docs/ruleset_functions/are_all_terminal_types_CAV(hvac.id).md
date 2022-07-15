# are_all_terminal_types_CAV

**Description:** Returns TRUE if all of the terminal unit types associated with the hvac system are constant air volume (CAV). It returns FALSE if any of the terminal units are of a type other than constant air volume (CAV).   

**Inputs:**  
- **B-RMR**: To evaluate if the terminal unit types are constant air volume (CAV).    
- **hvac_b.id**: The id of the hvac system to evaluate. 

**Returns:**  
- **are_all_terminal_types_CAV**: The function returns TRUE if all of the terminal unit types associated with the hvac system are constant air volume (CAV). It returns FALSE if any of the terminal units are of a type other than constant air volume (CAV).      
 
**Function Call:**  
1. get_list_of_terminal_units_served_by_hvac_sys()      

## Logic: 
- Get list of the terminal units associated with the hvac system: list_of_terminal_units_served_by_hvac_sys = get_list_of_terminal_units_served_by_hvac_sys(B_RMR, hvac_b.id)
- Check if there is at least one terminal unit in the list: `if len(list_of_terminal_units_served_by_hvac_sys) >= 1:`
    - For each terminal_b in the list of terminal units: `For terminal_b in list_of_terminal_units_served_by_hvac_sys:`  
        - Create an object for the terminal unit: `terminal_b = terminal_b.id`  
        - Check if the terminal unit type is constant air volume (CAV): `if terminal_b.type == "CONSTANT_AIR_VOLUME": are_all_terminal_types_CAV = TRUE`  
        - Else: `Else: are_all_terminal_types_CAV = FALSE`
        - Check if are_all_terminal_types_CAV equals False, if it does then leave the loop: `if are_all_terminal_types_CAV == FALSE:`
            - Leave the loop: `break`
        - Else: continue looping: `Else:`   
- Else: `Else: are_all_terminal_types_CAV = FALSE`

**Returns** `return are_all_terminal_types_CAV`   

**[Back](../_toc.md)**