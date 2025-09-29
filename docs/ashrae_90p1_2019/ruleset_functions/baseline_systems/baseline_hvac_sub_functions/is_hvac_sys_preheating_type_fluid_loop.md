# is_hvac_sys_preheating_type_fluid_loop 

**Description:** Returns TRUE if the HVAC system preheating system heating type is fluid loop. Returns FALSE if the HVAC system preheating system has anything other than fluid loop.   

**Inputs:**  
- **B-RMR**: To evaluate if the hvac system is modeled with preheating type fluid loop.   
- **hvac_b.id**: The id of the hvac system to evaluate.  

**Returns:**  
- **is_hvac_sys_preheating_type_fluid_loop**: Returns TRUE if the HVAC system preheating system has fluid loop as the heating type. Returns FALSE if the HVAC system has a preheating system type other than fluid loop.   
 
**Function Call:**  None  

## Logic:   
- Set is_hvac_sys_preheating_type_fluid_loop = FALSE: `is_hvac_sys_preheating_type_fluid_loop = FALSE`  
- Create an object associate with the preheating_system associated with hvac_b: `preheating_system_b = hvac_b.preheat_system`
- Check if the system type is FLUID_LOOP AND that hot_water_loop does not equal Null , if yes then is_hvac_sys_preheating_type_fluid_loop equals TRUE: `if preheating_system_b.heating_system_type == "FLUID_LOOP" AND preheating_system_b.hot_water_loop != Null: is_hvac_sys_preheating_type_fluid_loop = TRUE` 

**Returns** `return is_hvac_sys_preheating_type_fluid_loop`  


**[Back](../../../_toc.md)**

