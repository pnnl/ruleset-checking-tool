# get_list_of_terminal_units_served_by_hvac_sys  

**Description:** Returns a list of terminal unit IDs associated with the HVAC system input to the function.   

**Inputs:**  
- **RMR**: The RMR to evalute (B-RMR or P-RMR or U-RMR).   
- **hvac_x.id**: The id of the hvac system to evaluate.  

**Returns:**  
- **list_of_terminal_units_served_by_hvac_sys**: Returns a list of terminal unit IDs associated with the HVAC system input to the function.      
 
**Function Call:**  None

## Logic:   
- For each terminal unit in the RMR: `For terminal_x in RMR...Terminal:`
    - Check if the served_by_heating_ventilation_air_conditioning_system equals to the hvac id input to the function: `if terminal_x.served_by_heating_ventilation_air_conditioning_system = hvac_x.id:`  
        - Add it to the list of terminal units associated with the HVAC system: `list_of_terminal_units_served_by_hvac_sys = list_of_terminal_units_served_by_hvac_sys.append(terminal_x.id)`  
    - Else, do nothing: `Else:`

**[Back](../_toc.md)**














