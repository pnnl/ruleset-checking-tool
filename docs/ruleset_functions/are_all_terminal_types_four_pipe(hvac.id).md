# are_all_terminal_types_four_pipe

**Description:** Returns TRUE if the terminal unit type associated with all terminal units input to this function are FOUR_PIPE_FAN_COIL_UNIT. It returns FALSE if any of the terminal units is of a type other than FOUR_PIPE_FAN_COIL_UNIT.   

**Inputs:**  
- **B-RMR**: To evaluate if the terminal unit type associated with all terminal units input to this function are FOUR_PIPE_FAN_COIL_UNIT.   
- **terminal_unit_id_list**: List of terminal units to assess.

**Returns:**  
- **are_all_terminal_types_four_pipe**: The function returns TRUE if the terminal unit type associated with all terminal units input to this function are FOUR_PIPE_FAN_COIL_UNIT. It returns FALSE if any of the terminal units is of a type other than FOUR_PIPE_FAN_COIL_UNIT.     
 
**Function Call:**  None    

## Logic: 
- Set are_all_terminal_types_four_pipe = TRUE: `are_all_terminal_types_four_pipe = TRUE`  
- For each terminal_b in the list of terminal units: `For terminal_b in terminal_unit_id_list:`  
    - Create an object for the terminal unit: `terminal_b = terminal_b.id`  
    - Check if the terminal unit type is Not FOUR_PIPE_FAN_COIL_UNIT: `if terminal_b.type != "FOUR_PIPE_FAN_COIL_UNIT":`  
        - Set are_all_terminal_types_four_pipe = FALSE: `are_all_terminal_types_four_pipe = FALSE`
        - Leave the loop: `break`  

**Returns** `return are_all_terminal_types_four_pipe`  

**[Back](../_toc.md)**