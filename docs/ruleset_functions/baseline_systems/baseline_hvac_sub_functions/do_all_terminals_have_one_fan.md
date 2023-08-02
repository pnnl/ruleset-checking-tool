# do_all_terminals_have_one_fan   

**Description:** Returns TRUE if a fan data element associated with all terminal units input to this function. It returns FALSE if any terminal unit has no fan data element not equal to one.

**Inputs:**  
- **B-RMR**: To evaluate if the fan data element associated with all terminal units is equal to one (i.e., there is only one fan associated with the terminal unit).   
- **terminal_unit_id_list**: List of terminal units to assess.

**Returns:**  
- **do_all_terminals_have_one_fan**: The function returns TRUE if there is a fan data element associated with all terminal units input to this function. It returns FALSE if any terminal unit a no fan data.     

**Function Call:**  None  

## Logic:
- Set do_all_terminals_have_one_fan = TRUE: `do_all_terminals_have_one_fan = TRUE`  
- For each terminal_b in the list of terminal units: `For terminal_b in terminal_unit_id_list:`  
    - Create an object for the terminal unit: `terminal_b = terminal_b.id`  
    - Check if there is a fan associated with the terminal unit : `if terminal_b.fan == None:`
        - Set do_all_terminals_have_one_fan = FALSE: `do_all_terminals_have_one_fan = FALSE`  
        - Leave the loop: `break`  

**Returns** `return do_all_terminals_have_one_fan`  

**[Back](../../../_toc.md)**
