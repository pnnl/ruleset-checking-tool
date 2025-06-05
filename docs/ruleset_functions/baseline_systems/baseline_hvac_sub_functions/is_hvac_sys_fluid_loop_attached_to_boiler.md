# is_hvac_sys_fluid_loop_attached_to_boiler  

**Description:** Returns TRUE if the fluid loop associated with the heating system associated with the HVAC system is attached to a boiler. Returns FALSE if this is not the case.   

**Inputs:**  
- **B-RMR**: To evaluate if the fluid loop associated with the heating system associated with the HVAC system is attached to a boiler.   
- **hvac_b.id**: The id of the hvac system to evaluate.  

**Returns:**  
- **is_hvac_sys_fluid_loop_attached_to_boiler**: Returns TRUE if the fluid loop associated with the heating system associated with the HVAC system is attached to a boiler. Returns FALSE if this is not the case.   
 
**Function Call:** None  

## Logic:   
- Set is_hvac_sys_fluid_loop_attached_to_boiler equal to FALSE: `is_hvac_sys_fluid_loop_attached_to_boiler = FALSE`  
- For each boiler in B_RMR, save boiler to loop boiler list: `for boiler_b in B_RMR.RulesetModelInstance.boilers: boiler_loop_ids.append(boiler_b.loop)`
- Create an object associate with the heating_system fluid loop associated with hvac_b: `fluid_loop_b = hvac_b.heating_system.hot_water_loop`
- Check if the fluid loop type is heating: `if fluid_loop_b.type = "HEATING":`
    - Check if the fluid loop id is in the list of keys created above, if yes then is_hvac_sys_fluid_loop_attached_to_boiler equals TRUE: `if fluid_loop_b.id in boiler_loop_ids: is_hvac_sys_fluid_loop_attached_to_boiler = TRUE` 

**Returns** `is_hvac_sys_fluid_loop_attached_to_boiler`  



**[Back](../../../_toc.md)**
