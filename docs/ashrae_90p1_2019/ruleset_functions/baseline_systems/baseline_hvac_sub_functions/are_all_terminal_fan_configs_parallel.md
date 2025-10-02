# are_all_terminal_fan_configs_parallel   

**Description:** Returns TRUE if the fan configuration associated with all terminal units input to this function are parallel. It returns FALSE if any terminal unit has a fan configuration other than parallel.   

**Inputs:**  
- **B-RMR**: To evaluate if the fan configuration associated with all terminal units associated with the hvac system is parallel.   
- **terminal_unit_id_list**: List of terminal units to assess.

**Returns:**  
- **are_all_terminal_fan_configs_parallel**: The function returns TRUE if the fan configuration associated with all terminal units input to this function are parallel. It returns FALSE if any terminal unit has a fan configuration other than parallel.  
 
**Function Call:**  None       

## Logic: 
- Set are_all_terminal_fan_configs_parallel = TRUE: `are_all_terminal_fan_configs_parallel = TRUE`  
- For each terminal_b in the list of terminal units: `For terminal_b in terminal_unit_id_list:`  
    - Create an object for the terminal unit: `terminal_b = terminal_b.id`  
    - Check if the fan configuration associated with the terminal unit does not equal parallel: `if terminal_b.fan_configuration != "PARALLEL":`  
        - Set are_all_terminal_fan_configs_parallel = FALSE: `are_all_terminal_fan_configs_parallel = FALSE`
        - Leave the loop: `break`  

**Returns** `return are_all_terminal_fan_configs_parallel`  

**[Back](../../../_toc.md)**
