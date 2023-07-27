# are_all_terminal_cool_sources_chilled_water   

**Description:** Returns TRUE if the cool source associated with all terminal units is CHILLED_WATER. It returns FALSE if any terminal unit has a cool source other than CHILLED_WATER.   

**Inputs:**  
- **B-RMR**: To evaluate if the cool source associated with all terminal units sent to this function is CHILLED_WATER.     
- **terminal_unit_id_list**: List of terminal units to assess.

**Returns:**  
- **are_all_terminal_cool_sources_chilled_water**: The function returns TRUE if the cool source associated with all terminal units sent to this function is CHILLED_WATER. It returns FALSE if any terminal unit has a cool source other than CHILLED_WATER.  
 
**Function Call:**  None     

## Logic:  
- Set are_all_terminal_cool_sources_chilled_water = TRUE: `are_all_terminal_cool_sources_chilled_water = TRUE`  
- For each terminal_b in the list of terminal units: `For terminal_b in terminal_unit_id_list:`  
    - Create an object for the terminal unit: `terminal_b = terminal_b.id`  
    - Check if the cool source associated with the terminal unit does not equal CHILLED_WATER: `if terminal_b.cooling_source != "CHILLED_WATER":`
        - Set are_all_terminal_cool_sources_chilled_water = FALSE: `are_all_terminal_cool_sources_chilled_water = FALSE`
        - Leave the loop: `break`

**Returns** `return are_all_terminal_cool_sources_chilled_water`  

**[Back](../../../_toc.md)**