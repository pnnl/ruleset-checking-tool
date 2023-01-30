# is_hvac_sys_cooling_type_fluid_loop

**Description:** Returns TRUE if the HVAC system has fluid_loop cooling. Returns FALSE if the HVAC system has anything other than fluid_loop cooling or if it has more than 1 cooling system.   

**Inputs:**  
- **B-RMR**: To evaluate if the hvac system is modeled with fluid_loop cooling.   
- **hvac_b.id**: The id of the hvac system to evaluate.  

**Returns:**  
- **is_hvac_sys_cooling_type_fluid_loop**: Returns TRUE if the HVAC system has fluid_loop cooling AND only one cooling system . Returns FALSE if the HVAC system has a cooling system type other than fluid_loop or if it has more than one cooling system.   
 
**Function Call:**  
1. is_there_only_one_cooling_system()    

## Logic:   
- Set is_hvac_sys_cooling_type_fluid_loop = FALSE: `is_hvac_sys_cooling_type_fluid_loop = FALSE`  
- Check that there is a cooling system associated with the HVAC system: `if hvac_b.cooling_system == TRUE:`  
    - Create an object associate with the cooling_system associated with hvac_b: `cooling_system_b = hvac_b.cooling_system`
    - Check if the system is FLUID_LOOP and the chilled water loop does not equal null, if yes then is_hvac_sys_cooling_type_fluid_loop equals TRUE  : `if cooling_system_b.cooling_system_type == "FLUID_LOOP" AND cooling_system_b.chilled_water_loop != Null: is_hvac_sys_cooling_type_fluid_loop = TRUE` 

**Returns** `return is_hvac_sys_cooling_type_fluid_loop`  

**[Back](../../../_toc.md)**
