# are_all_terminal_fans_null   

**Description:** Returns TRUE if the fan data element associated with all terminal units input to this function are equal to Null. It returns FALSE if any terminal unit has a fan data element not equal to Null.   
   

**Inputs:**  
- **B-RMR**: To evaluate if the fan data element associated with all terminal units is equal to Null.   
- **terminal_unit_id_list**: List of terminal units to assess.

**Returns:**  
- **are_all_terminal_fans_null**: The function returns TRUE if the fan data element associated with all terminal units input to this function are equal to Null. It returns FALSE if any terminal unit has a fan data element not equal to Null.     
 
**Function Call:**  None  

## Logic: 
- Set are_all_terminal_fans_null = TRUE: `are_all_terminal_fans_null = TRUE`  
- For each terminal_b in the list of terminal units: `For terminal_b in terminal_unit_id_list:`  
    - Create an object for the terminal unit: `terminal_b = terminal_b.id`  
    - Check if the list of fans associated with the terminal unit does not equal Null: `if terminal_b.fan != Null:`
        - Set are_all_terminal_fans_null = FALSE: `are_all_terminal_fans_null = FALSE`  
        - Leave the loop: `break`  

**Returns** `return are_all_terminal_fans_null`  

**[Back](../../../_toc.md)**
