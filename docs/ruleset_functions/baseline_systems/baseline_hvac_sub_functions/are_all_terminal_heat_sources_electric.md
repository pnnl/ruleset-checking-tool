# are_all_terminal_heat_sources_electric   

**Description:** Returns TRUE if the heat source associated with all terminal units input to this function are electric. It returns FALSE if any terminal unit has a heat source other than electric.   

**Inputs:**  
- **B-RMR**: To evaluate if the heat source associated with all terminal units associated with the hvac system is electric.   
- **terminal_unit_id_list**: List of terminal units to assess.

**Returns:**  
- **are_all_terminal_heat_sources_electric**: The function returns TRUE if the heat source associated with all terminal units input to this function are electric. It returns FALSE if any terminal unit has a heat source other than electric.  
 
**Function Call:**  None       

## Logic: 
- Set are_all_terminal_heat_sources_electric = TRUE: `are_all_terminal_heat_sources_electric = TRUE`  
- For each terminal_b in the list of terminal units: `For terminal_b in terminal_unit_id_list:`  
    - Create an object for the terminal unit: `terminal_b = terminal_b.id`  
    - Check if the heat source associated with the terminal unit does not equal electric: `if terminal_b.heating_source != "ELECTRIC":`  
        - Set are_all_terminal_heat_sources_electric = FALSE: `are_all_terminal_heat_sources_electric = FALSE`
        - Leave the loop: `break`  

**Returns** `return are_all_terminal_heat_sources_electric`  

**[Back](../../../_toc.md)**
