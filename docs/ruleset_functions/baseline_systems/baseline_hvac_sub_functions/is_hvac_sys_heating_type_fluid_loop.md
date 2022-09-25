# is_hvac_sys_heating_type_fluid_loop 

**Description:** Returns TRUE if the HVAC system heating system heating type is fluid loop. Returns FALSE if the HVAC system heating system has anything other than fluid loop or if it has more than 1 heating system.   

**Inputs:**  
- **B-RMR**: To evaluate if the hvac system is modeled with heating type fluid loop.   
- **hvac_b.id**: The id of the hvac system to evaluate.  

**Returns:**  
- **is_hvac_sys_heating_type_fluid_loop**: Returns TRUE if the HVAC system heating system has fluid loop as the heating type AND only one heating system is associated with the HVAC system. Returns FALSE if the HVAC system has a heating system type other than fluid loop or if it has more than one heating system.   
 
**Function Call:**  
1. is_there_only_one_heating_system()

## Logic:   
- Set is_hvac_sys_heating_type_fluid_loop = FALSE: `is_hvac_sys_heating_type_fluid_loop = FALSE`  
- Check that there is only one heating system associated with the HVAC system: `if hvac_b.heating_system == TRUE:`  
    - Create an object associate with the heating_system associated with hvac_b: `heating_system_b = hvac_b.heating_system`
    - Check if the system type is FLUID_LOOP AND that hot_water_loop does not equal Null , if yes then is_hvac_sys_heating_type_fluid_loop equals TRUE: `if heating_system_b.heating_system_type == "FLUID_LOOP" AND heating_system_b.hot_water_loop != Null: is_hvac_sys_heating_type_fluid_loop = TRUE` 

**Returns** `return is_hvac_sys_heating_type_fluid_loop`  

**[Back](../../../_toc.md)**