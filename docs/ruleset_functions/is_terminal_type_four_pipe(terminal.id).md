# is_terminal_type_four_pipe

**Description:** Returns TRUE if the terminal unit type is FOUR_PIPE_FAN_COIL_UNIT. It returns FALSE if the terminal unit is a type other than FOUR_PIPE_FAN_COIL_UNIT.   

**Inputs:**  
- **B-RMR**: To evaluate if the terminal unit type is FOUR_PIPE_FAN_COIL_UNIT.    
- **terminal_b.id**: The id of the terminal unit to evaluate.  

**Returns:**  
- **is_terminal_type_four_pipe**: The function returns TRUE if the terminal unit type is FOUR_PIPE_FAN_COIL_UNIT. It returns FALSE if the terminal unit is a type other than FOUR_PIPE_FAN_COIL_UNIT.    
 
**Function Call:** None  

## Logic: 
- Create an object for the terminal unit: `terminal_b = terminal_b.id`  
- Check if the terminal unit type is FOUR_PIPE_FAN_COIL_UNIT: `if terminal_b.type == "FOUR_PIPE_FAN_COIL_UNIT": is_terminal_type_four_pipe = TRUE`
- Else: `Else: is_terminal_type_four_pipe = FALSE`

**Returns** `return is_terminal_type_four_pipe`  

**[Back](../_toc.md)**