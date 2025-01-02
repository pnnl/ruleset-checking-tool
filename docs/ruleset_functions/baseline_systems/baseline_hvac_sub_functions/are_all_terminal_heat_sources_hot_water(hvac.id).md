# are_all_terminal_heat_sources_hot_water   

**Description:** Returns TRUE if the heat source associated with all terminal units input to this function is HOT_WATER. It returns FALSE if any terminal unit has a heat source other than HOT_WATER.   

**Inputs:**  
- **B-RMR**: To evaluate if the heat source associated with all terminal units is HOT_WATER.   
- **terminal_unit_id_list**: List of terminal units to assess.

**Returns:**  
- **are_all_terminal_heat_sources_hot_water**: The function returns TRUE if the heat source associated with all terminal units input to this function is HOT_WATER. It returns FALSE if any terminal unit has a heat source other than HOT_WATER.  
 
**Function Call:**  None   

## Logic:  
- Set are_all_terminal_heat_sources_hot_water = TRUE: `are_all_terminal_heat_sources_hot_water = TRUE`  
- For each terminal_b in the list of terminal units: `For terminal_b in terminal_unit_id_list:`  
    - Create an object for the terminal unit: `terminal_b = terminal_b.id`  
    - Check if the heat source associated with the terminal unit does not equal HOT_WATER: `if terminal_b.heating_source != "HOT_WATER":`  
        - Set are_all_terminal_heat_sources_hot_water = FALSE: `are_all_terminal_heat_sources_hot_water = FALSE`  
        - Leave the loop: `break`  

**Returns** `return are_all_terminal_heat_sources_hot_water`  

**[Back](../../../_toc.md)**
