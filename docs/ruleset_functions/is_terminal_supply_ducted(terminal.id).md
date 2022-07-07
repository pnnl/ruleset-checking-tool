# is_terminal_supply_ducted

**Description:** Returns TRUE if the terminal supply is ducted. It returns FALSE if the terminal is supply ducted data element equals FALSE.   

**Inputs:**  
- **B-RMR**: To evaluate if the terminal supply is ducted.    
- **terminal_b.id**: The id of the terminal unit to evaluate.  

**Returns:**  
- **is_terminal_supply_ducted**: The function returns TRUE if the terminal supply is ducted. It returns FALSE if the terminal is supply ducted data element equals FALSE.      
 
**Function Call:** None  

## Logic: 
- Create an object for the terminal unit: `terminal_b = terminal_b.id`  
- Check if the terminal supply is ducted: `if terminal_b.is_supply_ducted == TRUE: is_terminal_supply_ducted = TRUE`
- Else: `Else: is_terminal_supply_ducted = FALSE`

**Returns** `return is_terminal_supply_ducted`  

**[Back](../_toc.md)**