# is_terminal_cool_source_none   

**Description:** Returns TRUE if the cool source associated with the terminal unit is None or Null. It returns FALSE if the terminal unit has a cool source other than None or Null.   

**Inputs:**  
- **B-RMR**: To evaluate if the cool source associated with the terminal unit is None or Null.   
- **terminal_b.id**: The id of the terminal unit to evaluate.  

**Returns:**  
- **is_terminal_cool_source_none**: The function returns TRUE if the cool source associated with the terminal unit is None or Null. It returns FALSE if the terminal unit has a cool source other than None or Null.  
 
**Function Call:** None  

## Logic: 
- Create an object for the terminal unit: `terminal_b = terminal_b.id`  
- Check if the cool source associated with the terminal unit equals None or is Null: `if terminal_b.cooling_source == "None" or terminal_b.cooling_source == Null: is_terminal_cool_source_none = TRUE`
- Else: `Else: is_terminal_cool_source_none = FALSE`

**Returns** `return is_terminal_cool_source_none`  

**[Back](../_toc.md)**
