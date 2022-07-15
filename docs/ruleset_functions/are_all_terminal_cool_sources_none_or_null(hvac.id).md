# are_all_terminal_cool_sources_none_or_null   

**Description:** Returns TRUE if the cool source associated with all terminal units associated with the hvac system is None or Null. It returns FALSE if any terminal unit has a cool source other than None or Null.   

**Inputs:**  
- **B-RMR**: To evaluate if the cool source associated with all terminal units associated with the hvac system is None or Null.   
- **hvac_b.id**: The id of the hvac system to evaluate.  

**Returns:**  
- **are_all_terminal_cool_sources_none_or_null**: The function returns TRUE if the cool source associated with all terminal units associated with the hvac system is None or Null. It returns FALSE if any terminal unit has a cool source other than None or Null.  
 
**Function Call:**  
1. get_list_of_terminal_units_served_by_hvac_sys()      

## Logic: 
- Get list of the terminal units associated with the hvac system: `list_of_terminal_units_served_by_hvac_sys = get_list_of_terminal_units_served_by_hvac_sys(B_RMR, hvac_b.id)`  
- Check if there is at least one terminal unit in the list: `if len(list_of_terminal_units_served_by_hvac_sys) >= 1:`
    - For each terminal_b in the list of terminal units: `For terminal_b in list_of_terminal_units_served_by_hvac_sys:`  
        - Create an object for the terminal unit: `terminal_b = terminal_b.id`  
        - Check if the cool source associated with the terminal unit equals None or is Null: `if terminal_b.cooling_source == "None" or terminal_b.cooling_source == Null: are_all_terminal_cool_sources_none_or_null = TRUE`
        - Else: `Else: are_all_terminal_cool_sources_none_or_null = FALSE`
        - Check if are_all_terminal_cool_sources_none_or_null equals False, if it does then leave the loop: `if are_all_terminal_cool_sources_none_or_null == FALSE:`
            - Leave the loop: `break`
        - Else: continue looping: `Else:`   
- Else: `Else: are_all_terminal_cool_sources_none_or_null = FALSE`  

**Returns** `return are_all_terminal_cool_sources_none_or_null`  

**[Back](../_toc.md)**
