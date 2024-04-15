# is_hvac_sys_fluid_loop_purchased_CHW  

**Description:** Returns TRUE if the fluid loop associated with the cooling system associated with the HVAC system is attached to an external purchased chilled water loop. Returns FALSE if this is not the case.   

**Inputs:**  
- **B-RMR**: To evaluate if the fluid loop associated with the cooling system associated with the HVAC system is attached to an external purchased chilled water loop.   
- **hvac_b.id**: The id of the hvac system to evaluate.  

**Returns:**  
- **is_hvac_sys_fluid_loop_purchased_CHW**: Returns TRUE if the fluid loop associated with the cooling system associated with the HVAC system is attached to an external purchased cooling loop. Returns FALSE if this is not the case.   
 
**Function Call:** None  

## Logic:   
- Set is_hvac_sys_fluid_loop_purchased_CHW equal to FALSE: `is_hvac_sys_fluid_loop_purchased_CHW = FALSE`  
- Check if RMR is modeled with external fluid source: `if RMR.RuleModelInstance.external_fluid_source != Null:`  
    - For each external fluid source in RMR: `for external_fluid_source.id in RMR.RuleModelInstance.external_fluid_source:`  
        - Check if external fluid source is chilled water: `if external_fluid_source.id.type == "CHILLED_WATER"`    
            - Add the associated loop id to the purchased_chilled_water_loop_list_b list: `purchased_chilled_water_loop_list_b.append (external_fluid_source.id.loop.id)`  
    - Create an object associate with the cooling_system fluid loop associated with hvac_b: `fluid_loop_b = hvac_b.cooling_system.chilled_water_loop`  
    - Check if the fluid loop id is in the list created above, if yes then is_hvac_sys_fluid_loop_purchased_CHW equals TRUE  : `if fluid_loop_b.id in purchased_chilled_water_loop_list_b: is_hvac_sys_fluid_loop_purchased_CHW = TRUE`  

**Returns** `is_hvac_sys_fluid_loop_purchased_CHW`  



**[Back](../../../_toc.md)**