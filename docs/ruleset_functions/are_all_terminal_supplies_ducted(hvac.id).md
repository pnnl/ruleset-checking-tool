# are_all_terminal_supplies_ducted

**Description:** Returns TRUE if all of the terminal supplies are ducted (i.e., is_supply_ducted = TRUE) for the hvac system input to the function. It returns FALSE if any of the terminal supplies are not ducted (i.e., is_supply_ducted = FALSE).   

**Inputs:**  
- **B-RMR**: To evaluate if all the terminal supplies are ducted for the hvac system.    
- **hvac_b.id**: The id of the hvac system to evaluate. 

**Returns:**  
- **are_all_terminal_supplies_ducted**: The function returns TRUE if all of the terminal supplies are ducted (i.e., is_supply_ducted = TRUE) for the hvac system input to the function. It returns FALSE if any of the terminal supplies are not ducted (i.e., is_supply_ducted = FALSE).      
 
**Function Call:**  
1. get_list_of_terminal_units_served_by_hvac_sys()      

## Logic: 
- Get list of the terminal units associated with the hvac system: `list_of_terminal_units_served_by_hvac_sys = get_list_of_terminal_units_served_by_hvac_sys(B_RMR, hvac_b.id)`  
- Check if there is at least one terminal unit in the list: `if len(list_of_terminal_units_served_by_hvac_sys) >= 1:`
    - For each terminal_b in the list of terminal units: `For terminal_b in list_of_terminal_units_served_by_hvac_sys:`  
        - Create an object for the terminal unit: `terminal_b = terminal_b.id`  
        - Check if the terminal supply is ducted: `if terminal_b.is_supply_ducted == TRUE: are_all_terminal_supplies_ducted = TRUE`
        - Else: `Else: are_all_terminal_supplies_ducted = FALSE`
        - Check if are_all_terminal_supplies_ducted equals False, if it does then leave the loop: `if are_all_terminal_supplies_ducted == FALSE:`
            - Leave the loop: `break`
        - Else: continue looping: `Else:`   
- Else: `Else: are_all_terminal_supplies_ducted = FALSE`

**Returns** `return are_all_terminal_supplies_ducted`  

**[Back](../_toc.md)**