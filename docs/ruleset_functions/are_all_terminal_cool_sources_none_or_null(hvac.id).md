# are_all_terminal_cool_sources_none_or_null   

**Description:** Returns TRUE if the cool source associated with all terminal units input to this function are None or Null. It returns FALSE if any terminal unit has a cool source other than None or Null.   

**Inputs:**  
- **B-RMR**: To evaluate if the cool source associated with all terminal units input to this function are None or Null.   
- **terminal_unit_id_list**: List of terminal units to assess.   

**Returns:**  
- **are_all_terminal_cool_sources_none_or_null**: The function returns TRUE if the cool source associated with all terminal units input to this function are None or Null. It returns FALSE if any terminal unit has a cool source other than None or Null.  
 
**Function Call:**  None    

## Logic: 
- For each terminal_b in the list of terminal units: `For terminal_b in terminal_unit_id_list:`  
    - Create an object for the terminal unit: `terminal_b = terminal_b.id`  
    - Check if the cool source associated with the terminal unit equals None or is Null: `if terminal_b.cooling_source == "None" or terminal_b.cooling_source == Null: are_all_terminal_cool_sources_none_or_null = TRUE`
    - Else: `Else: are_all_terminal_cool_sources_none_or_null = FALSE`
    - Check if are_all_terminal_cool_sources_none_or_null equals False, if it does then leave the loop: `if are_all_terminal_cool_sources_none_or_null == FALSE:`
        - Leave the loop: `break`
    - Else: continue looping: `Else:`    

**Returns** `return are_all_terminal_cool_sources_none_or_null`  

**[Back](../_toc.md)**
