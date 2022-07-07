# is_terminal_type_CAV

**Description:** Returns TRUE if the terminal unit type is constant air volume (CAV). It returns FALSE if the terminal unit is a type other than constant air volume (CAV).   

**Inputs:**  
- **B-RMR**: To evaluate if the terminal unit type is constant air volume (CAV).    
- **terminal_b.id**: The id of the terminal unit to evaluate.  

**Returns:**  
- **is_terminal_type_CAV**: The function returns TRUE if the terminal unit type is constant air volume (CAV). It returns FALSE if the terminal unit is a type other than constant air volume (CAV).    
 
**Function Call:** None  

## Logic: 
- Create an object for the terminal unit: `terminal_b = terminal_b.id`  
- Check if the terminal unit type is constant air volume (CAV): `if terminal_b.type == "CONSTANT_AIR_VOLUME": is_terminal_type_CAV = TRUE`
- Else: `Else: is_terminal_type_CAV = FALSE`

**Returns** `return is_terminal_type_CAV`  

**[Back](../_toc.md)**