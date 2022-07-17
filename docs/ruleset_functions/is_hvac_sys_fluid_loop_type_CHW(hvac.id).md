# is_hvac_sys_fluid_loop_type_CHW  

**Description:** Returns TRUE if the fluid loop type associated with the cooling system associated with the HVAC system is chilled water and NOT an external source. Returns FALSE if this is not the case.   

**Inputs:**  
- **B-RMR**: To evaluate if the fluid loop associated with the cooling system associated with the HVAC system is is chilled water and not an external source.   
- **hvac_b.id**: The id of the hvac system to evaluate.  

**Returns:**  
- **is_hvac_sys_fluid_loop_type_CHW**: Returns TRUE if the fluid loop type associated with the cooling system associated with the HVAC system is chilled water and NOT an external source. Returns FALSE if this is not the case.   
 
**Function Call:** None  

## Logic:   
- Set is_hvac_sys_fluid_loop_type_CHW equal to FALSE: `is_hvac_sys_fluid_loop_type_CHW = FALSE`  
- For each external fluid source in RMR: `For external_fluid_source.id in RMR.RuleModelInstance.external_fluid_source:`  
    - Check if external fluid source is chilled water: `if external_fluid_source.id.type == "CHILLED_WATER"`    
        - Add the associated loop to the purchased_chilled_water_loop_list_b list: `purchased_chilled_water_loop_list_b = purchased_chilled_water_loop_list_b.append (external_fluid_source.id)`  
- Create an object associate with the cooling_system fluid loop associated with hvac_b: `fluid_loop_b = hvac_b.cooling_system[0].chilled_water_loop`  
- Check if the fluid loop id is in the list created above, if it is NOT then is_hvac_sys_fluid_loop_type_CHW equals TRUE  : `if fluid_loop_b.id Not in purchased_chilled_water_loop_list_b: is_hvac_sys_fluid_loop_type_CHW = TRUE`  

**Returns** `is_hvac_sys_fluid_loop_type_CHW`  



**[Back](../_toc.md)**