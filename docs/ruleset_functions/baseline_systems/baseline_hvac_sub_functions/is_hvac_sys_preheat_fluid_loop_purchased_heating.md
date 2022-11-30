# is_hvac_sys_preheat_fluid_loop_purchased_heating  

**Description:** Returns TRUE if the fluid loop associated with the preheating system associated with the HVAC system is attached to an external purchased heating loop. Returns FALSE if this is not the case.   

**Inputs:**  
- **B-RMR**: To evaluate if the fluid loop associated with the preheating system associated with the HVAC system is attached to an external purchased heating loop.   
- **hvac_b.id**: The id of the hvac system to evaluate.  

**Returns:**  
- **is_hvac_sys_preheat_fluid_loop_purchased_heating**: Returns TRUE if the fluid loop associated with the preheating system associated with the HVAC system is attached to an external purchased heating loop. Returns FALSE if this is not the case.   
 
**Function Call:** None  

## Logic:   
- Set is_hvac_sys_preheat_fluid_loop_purchased_heating equal to FALSE: `is_hvac_sys_preheat_fluid_loop_purchased_heating = FALSE`  
- Check if RMR is modeled with external fluid source: `if RMR.RuleModelInstance.external_fluid_source != Null:`  
    - For each external fluid source in RMR: `for external_fluid_source.id in RMR.RuleModelInstance.external_fluid_source:`  
        - Check if external fluid source is heating type: `if external_fluid_source.id.type == "HOT_WATER" OR external_fluid_source.id.type == "STEAM":`    
            - Add the associated loop to the purchased_heating_loop_list_b list: `purchased_heating_loop_list_b = purchased_heating_loop_list_b.append (external_fluid_source.id.loop.id)`   
    - Create an object associate with the preheat_system fluid loop associated with hvac_b: `fluid_loop_b = hvac_b.preheat_system.hot_water_loop`
    - Check if the fluid loop id is in the list created above, if yes then is_hvac_sys_preheat_fluid_loop_purchased_heating equals TRUE  : `if fluid_loop_b.id in purchased_heating_loop_list_b: is_hvac_sys_preheat_fluid_loop_purchased_heating = TRUE`  

**Returns** `is_hvac_sys_preheat_fluid_loop_purchased_heating`  


**[Back](../../../_toc.md)**

