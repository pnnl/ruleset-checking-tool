# is_fluid_loop_attached_to_chiller  

**Description:** Returns TRUE if the fluid loop associated with the cooling system associated with the HVAC system is attached to a chiller. Returns FALSE if this is not the case.   

**Inputs:**  
- **B-RMR**: To evaluate if the fluid loop associated with the cooling system associated with the HVAC system is attached to a chiller.   
- **hvac_b.id**: The id of the hvac system to evaluate.  

**Returns:**  
- **is_fluid_loop_attached_to_chiller**: Returns TRUE if the fluid loop associated with the cooling system associated with the HVAC system is attached to a chiller. Returns FALSE if this is not the case.   
 
**Function Call:** None  

## Logic:   
- Set is_fluid_loop_attached_to_chiller equal to FALSE: `is_fluid_loop_attached_to_chiller = FALSE`  
- For each chiller in B_RMR, save the list of the associated primary and secondary loops: `for chiller_b in B_RMR.RulesetModelInstance.chillers:`   
    - Add the secondary loops associated with the chiller system primary loop to a list of loops: `loop_list.extend(list(chiller_b.cooling_loop.child_loops))`  
    - Add the primary loop associated with the chiller system to the list: `loop_list.append(chiller_b.cooling_loop)`  
- Create an object associate with the cooling_system fluid loop associated with hvac_b: `fluid_loop_b = hvac_b.cooling_system.chilled_water_loop`
- Check if the fluid loop type is cooling: `if fluid_loop_b.type = "COOLING":`
    - Check if the fluid loop is in the list created above, if yes then is_fluid_loop_attached_to_chiller equals TRUE: `if fluid_loop_b in loop_list: is_fluid_loop_attached_to_chiller = TRUE` 

**Returns** `is_fluid_loop_attached_to_chiller`  


**[Back](../../../_toc.md)**
