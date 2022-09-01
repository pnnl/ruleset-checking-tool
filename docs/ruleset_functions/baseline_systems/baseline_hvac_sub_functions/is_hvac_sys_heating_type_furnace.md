# is_hvac_sys_heating_type_furnace 

**Description:** Returns TRUE if the HVAC system heating system heating type is furnace. Returns FALSE if the HVAC system heating system has anything other than furnace or if it has more than 1 heating system.   

**Inputs:**  
- **B-RMR**: To evaluate if the hvac system is modeled with heating type furnace.   
- **hvac_b.id**: The id of the hvac system to evaluate.  

**Returns:**  
- **is_hvac_sys_heating_type_furnace**: Returns TRUE if the HVAC system heating system has furnace as the heating type AND only one heating system is associated with the HVAC system. Returns FALSE if the HVAC system has a heating system type other than furnace or if it has more than one heating system.   
 
**Function Call:**  
1. is_there_only_one_heating_system()

## Logic:   
- Set is_hvac_sys_heating_type_furnace = FALSE: `is_hvac_sys_heating_type_furnace = FALSE`  
- Check that there is only one heating system associated with the HVAC system: `if is_there_only_one_heating_system(B_RMR,hvac_b.id) == TRUE:`  
    - Create an object associate with the heating_system associated with hvac_b: `heating_system_b = hvac_b.heating_system[0]`
    - Check if the system type is FURNACE, if yes then is_hvac_sys_heating_type_furnace equals TRUE: `if heating_system_b.heating_system_type == "FURNACE": is_hvac_sys_heating_type_furnace = TRUE` 

**Returns** `return is_hvac_sys_heating_type_furnace`  

**[Back](../../../_toc.md)**