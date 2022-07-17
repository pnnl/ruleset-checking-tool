# are_all_terminal_heat_sources_HW   

**Description:** Returns TRUE if the heat source associated with all terminal units input to this function are hot water. It returns FALSE if any terminal unit has a heat source other than hot water.   

**Inputs:**  
- **B-RMR**: To evaluate if the heat source associated with all terminal units associated with the hvac system is hot water.   
- **terminal_unit_id_list**: List of terminal units to assess.

**Returns:**  
- **are_all_terminal_heat_sources_HW**: The function returns TRUE if the heat source associated with all terminal units input to this function are hot water. It returns FALSE if any terminal unit has a heat source other than hot water.  
 
**Function Call:**  None       

## Logic: 
- Set are_all_terminal_heat_sources_HW = TRUE: `are_all_terminal_heat_sources_HW = TRUE`  
- For each terminal_b in the list of terminal units: `For terminal_b in terminal_unit_id_list:`  
    - Create an object for the terminal unit: `terminal_b = terminal_b.id`  
    - Check if the heat source associated with the terminal unit does not equal hot water: `if terminal_b.heating_source != "HOT_WATER":`  
        - Set are_all_terminal_heat_sources_HW = FALSE: `are_all_terminal_heat_sources_HW = FALSE`
        - Leave the loop: `break`  

**Returns** `return are_all_terminal_heat_sources_HW`  

**[Back](../_toc.md)**
