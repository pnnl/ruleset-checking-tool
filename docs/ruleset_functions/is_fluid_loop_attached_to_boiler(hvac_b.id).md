# is_fluid_loop_attached_to_boiler  

**Description:** Returns TRUE if the fluid loop associated with the heating system associated with the HVAC system is attached to a boiler. Returns FALSE if this is not the case.   

**Inputs:**  
- **B-RMR**: To evaluate if the fluid loop associated with the heating system associated with the HVAC system is attached to a boiler.   
- **hvac_b.id**: The id of the hvac system to evaluate.  

**Returns:**  
- **is_fluid_loop_attached_to_boiler**: Returns TRUE if the fluid loop associated with the heating system associated with the HVAC system is attached to a boiler. Returns FALSE if this is not the case.   
 
**Function Call:** None  

## Logic:   
- For each boiler in B_RMR, save boiler to loop boiler dictionary: `for boiler_b in B_RMR.RulesetModelInstance.boilers: loop_boiler_dict[boiler_b.loop].append(boiler_b)`
- Create an object associate with the heating_system fluid loop associated with hvac_b: `fluid_loop_b = hvac_b.heating_system[0].hot_water_loop`
- Check if the fluid loop id is in the list created above, if yes then is_fluid_loop_attached_to_boiler equals TRUE  : `if fluid_loop_b.id in hot_water_loop_list_b: is_fluid_loop_attached_to_boiler = TRUE` 
- Else, is_fluid_loop_attached_to_boiler = FALSE: `ELse: is_fluid_loop_attached_to_boiler = FALSE`  

**Returns** `is_fluid_loop_attached_to_boiler`  



**[Back](../_toc.md)**
