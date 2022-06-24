# is_fluid_loop_purchased_heating  

**Description:** Returns TRUE if the fluid loop associated with the heating system associated with the HVAC system is attached to an external purchased heating loop. Returns FALSE if this is not the case.   

**Inputs:**  
- **B-RMR**: To evaluate if the fluid loop associated with the heating system associated with the HVAC system is attached to an external purchased heating loop.   
- **hvac_b.id**: The id of the hvac system to evaluate.  

**Returns:**  
- **is_fluid_loop_purchased_heating**: Returns TRUE if the fluid loop associated with the heating system associated with the HVAC system is attached to an external purchased heating loop. Returns FALSE if this is not the case.   
 
**Function Call:** None  

## Logic:   
- Check if RMR is not modeled with external fluid source: `if NOT RMR.ASHRAE229.external_fluid_source: is_fluid_loop_purchased_heating = FALSE`
- Else, continue on: `Else:`  
    - for each external fluid source in RMR: `for external_fluid_source.id in RMR.ASHRAE229.external_fluid_source:`
        - Check if external fluid source is heating type: `if external_fluid_source.id.type == "HOT_WATER"` QUESTION: SHOULD IT IT BE OR STEAM?  
            - Add the associated loop to the purchased_hot_water_loop_list_b list: `purchased_hot_water_loop_list_b = purchased_hot_water_loop_list_b.append (external_fluid_source.id.type)` 
    - Create an object associate with the heating_system fluid loop associated with hvac_b: `fluid_loop_b = hvac_b.heating_system[0].hot_water_loop`
    - Check if the fluid loop id is in the list created above, if yes then is_fluid_loop_purchased_heating equals TRUE  : `if fluid_loop_b.id in purchased_hot_water_loop_list_b: is_fluid_loop_purchased_heating = TRUE` 
    - Else, is_fluid_loop_purchased_heating = FALSE: `ELse: is_fluid_loop_purchased_heating = FALSE`  

**Returns** `is_fluid_loop_purchased_heating`  



**[Back](../_toc.md)**