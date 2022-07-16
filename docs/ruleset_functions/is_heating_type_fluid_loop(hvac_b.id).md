# is_heating_type_fluid_loop 

**Description:** Returns TRUE if the HVAC system heating system heating type is fluid loop. Returns FALSE if the HVAC system heating system has anything other than fluid loop or if it has more than 1 heating system.   

**Inputs:**  
- **B-RMR**: To evaluate if the hvac system is modeled with heating type fluid loop.   
- **hvac_b.id**: The id of the hvac system to evaluate.  

**Returns:**  
- **is_heating_type_fluid_loop**: Returns TRUE if the HVAC system heating system has fluid loop as the heating type AND only one heating system is associated with the HVAC system. Returns FALSE if the HVAC system has a heating system type other than fluid loop or if it has more than one heating system.   
 
**Function Call:** None  

## Logic:   
- Set is_heating_type_fluid_loop = FALSE: `is_heating_type_fluid_loop = FALSE`  
- Check that there is only one heating system associated with the HVAC system: `if is_there_only_one_heating_system(B_RMR,hvac_b.id) == TRUE:`  
    - Create an object associate with the heating_system associated with hvac_b: `heating_system_b = hvac_b.heating_system[0]`
    - Check if the system type is FLUID_LOOP, if yes then is_heating_type_fluid_loop equals TRUE  : `if heating_system_b.heating_system_type == "FLUID_LOOP": is_heating_type_fluid_loop = TRUE` 

**Returns** `return is_heating_type_fluid_loop`  

**[Back](../_toc.md)**