# is_terminal_fan_null   

**Description:** Returns TRUE if the list of fans associated with the terminal unit is Null. It returns FALSE if the list of fans associated with the terminal unit is anything other than Null.   

**Inputs:**  
- **B-RMR**: To evaluate if the list of fans associated with the terminal unit is Null.   
- **terminal_b.id**: The id of the terminal unit to evaluate.  

**Returns:**  
- **is_terminal_fan_null**: The function returns TRUE if the list of fans associated with the terminal unit is Null. It returns FALSE if the list of fans associated with the terminal unit is anything other than Null.    
 
**Function Call:** None  

## Logic: 
- Create an object for the terminal unit: `terminal_b = terminal_b.id`  
- Check if the list of fans associated with the terminal unit equals Null: `if terminal_b.fan == Null: is_terminal_fan_null = TRUE`
- Else: `Else: is_terminal_fan_null = FALSE`

**Returns** `return is_terminal_fan_null`  

**[Back](../_toc.md)**
