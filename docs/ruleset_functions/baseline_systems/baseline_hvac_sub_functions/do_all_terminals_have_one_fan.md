# do_all_terminals_have_one_fan   

**Description:** Returns TRUE if the fan data element associated with all terminal units input to this function are equal to one (i.e., there is only one fan associated with the terminal unit). It returns FALSE if any terminal unit has a fan data element not equal to one (i.e., there is NOT only one fan associated with the terminal unit).   
   

**Inputs:**  
- **B-RMR**: To evaluate if the fan data element associated with all terminal units is equal to one (i.e., there is only one fan associated with the terminal unit).   
- **terminal_unit_id_list**: List of terminal units to assess.

**Returns:**  
- **do_all_terminals_have_one_fan**: The function returns TRUE if the fan data element associated with all terminal units input to this function are equal to one (i.e., there is only one fan associated with the terminal unit). It returns FALSE if any terminal unit has a fan data element not equal to one (i.e., there is NOT only one fan associated with the terminal unit).     
 
**Function Call:**  None  

## Logic: 
- Set do_all_terminals_have_one_fan = TRUE: `do_all_terminals_have_one_fan = TRUE`  
- For each terminal_b in the list of terminal units: `For terminal_b in terminal_unit_id_list:`  
    - Create an object for the terminal unit: `terminal_b = terminal_b.id`  
    - Check if the length of the list of fans associated with the terminal unit does not equal one: `if len(terminal_b.fan) != 1:`
        - Set do_all_terminals_have_one_fan = FALSE: `do_all_terminals_have_one_fan = FALSE`  
        - Leave the loop: `break`  

**Returns** `return do_all_terminals_have_one_fan`  

**[Back](../../../_toc.md)**

