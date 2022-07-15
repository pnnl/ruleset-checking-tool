# are_all_terminal_supplies_ducted

**Description:** Returns TRUE if all of the terminal supplies are ducted (i.e., is_supply_ducted = TRUE) for the list of terminal units input to the function. It returns FALSE if any of the terminal supplies are not ducted (i.e., is_supply_ducted = FALSE).   

**Inputs:**  
- **B-RMR**: To evaluate if all the terminal supplies are ducted for the hvac system.    
- **terminal_unit_id_list**: List of terminal units to assess.

**Returns:**  
- **are_all_terminal_supplies_ducted**: The function returns TRUE if all of the terminal supplies are ducted (i.e., is_supply_ducted = TRUE) for the list of terminal units input to the function. It returns FALSE if any of the terminal supplies are not ducted (i.e., is_supply_ducted = FALSE).      
 
**Function Call:**   None       

## Logic:  
- For each terminal_b in the list of terminal units: `For terminal_b in terminal_unit_id_list:`  
    - Create an object for the terminal unit: `terminal_b = terminal_b.id`  
    - Check if the terminal supply is ducted: `if terminal_b.is_supply_ducted == TRUE: are_all_terminal_supplies_ducted = TRUE`
    - Else: `Else: are_all_terminal_supplies_ducted = FALSE`
         Check if are_all_terminal_supplies_ducted equals False, if it does then leave the loop: `if are_all_terminal_supplies_ducted == FALSE:`
        - Leave the loop: `break`
    - Else: continue looping: `Else:`   

**Returns** `return are_all_terminal_supplies_ducted`  

**[Back](../_toc.md)**