# are_all_terminal_heat_sources_none_or_null   

**Description:** Returns TRUE if the heat source associated with all terminal units input to this function are None or Null. It returns FALSE if any terminal unit has a heat source other than None or Null.   

**Inputs:**  
- **B-RMR**: To evaluate if the heat source associated with all terminal units associated with the hvac system is None or Null.   
- **terminal_unit_id_list**: List of terminal units IDs.

**Returns:**  
- **are_all_terminal_heat_sources_none_or_null**: The function returns TRUE if the heat source associated with all terminal units input to this function are None or Null. It returns FALSE if any terminal unit has a heat source other than None or Null.  
 
**Function Call:**  None       

## Logic: 
- Set are_all_terminal_heat_sources_none_or_null = TRUE: `are_all_terminal_heat_sources_none_or_null = TRUE`  
- For each terminal_b in the list of terminal units: `For terminal_b in terminal_unit_id_list:`  
    - Create an object for the terminal unit: `terminal_b = terminal_b.id`  
    - Check if the heat source associated with the terminal unit does not equal None and Null: `if terminal_b.heating_source != "None" AND terminal_b.heating_source != Null:`  
        - Set are_all_terminal_heat_sources_none_or_null = FALSE: `are_all_terminal_heat_sources_none_or_null = FALSE`
        - Leave the loop: `break`  

**Returns** `return are_all_terminal_heat_sources_none_or_null`  

**[Back](../../../_toc.md)**
