# is_hvac_sys_fluid_loop_attached_to_chiller  

**Description:** Returns TRUE if the fluid loop associated with the cooling system associated with the HVAC system is attached to a chiller. Returns FALSE if this is not the case.   

**Inputs:**  
- **B-RMR**: To evaluate if the fluid loop associated with the cooling system associated with the HVAC system is attached to a chiller.   
- **hvac_b.id**: The id of the hvac system to evaluate.  

**Returns:**  
- **is_fluid_loop_attached_to_chiller**: Returns TRUE if the fluid loop associated with the cooling system associated with the HVAC system is attached to a chiller. Returns FALSE if this is not the case.   
 
**Function Call:** None  

## Logic:   
- Set is_hvac_sys_fluid_loop_attached_to_chiller equal to FALSE: `is_hvac_sys_fluid_loop_attached_to_chiller = FALSE`  
- For each chiller in B_RMR, save chiller ids to cooling loop id list: `for chiller_b in B_RMR.RulesetModelInstance.chillers: cooling_loop_id.append(chiller_b.id)`
- Create an object associate with the cooling_system fluid loop associated with hvac_b: `fluid_loop_b = hvac_b.cooling_system.chilled_water_loop`
- Check if the fluid loop type is cooling: `if fluid_loop_b.type = "COOLING":`
    - Check if the fluid loop id is in the list of keys created above, if yes then is_fluid_loop_attached_to_chiller equals TRUE: `if fluid_loop_b.id in cooling_loop_id: is_fluid_loop_attached_to_chiller = TRUE` 

**Returns** `is_fluid_loop_attached_to_chiller`  


**[Back](../../../_toc.md)**
