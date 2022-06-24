# is_cooling_type_fluid_loop

**Description:** Returns TRUE if the HVAC system has fluid_loop cooling. Returns FALSE if the HVAC system has anything other than fluid_loop cooling or if it has more than 1 cooling system.   

**Inputs:**  
- **B-RMR**: To evaluate if the hvac system is modeled with fluid_loop cooling.   
- **hvac_b.id**: The id of the hvac system to evaluate.  

**Returns:**  
- **is_cooling_type_fluid_loop**: Returns TRUE if the HVAC system has fluid_loop cooling AND only one cooling system . Returns FALSE if the HVAC system has a cooling system type other than fluid_loop or if it has more than one cooling system.   
 
**Function Call:** None  

## Logic:   
- Check that there is only one cooling system associated with the HVAC system: `if Len(hvac_b.cooling_system) != 1: is_cooling_type_fluid_loop = FALSE`  
- Else, carry on: `Else: `
    - Create an object associate with the cooling_system associated with hvac_b: `cooling_system_b = hvac_b.cooling_system[0]`
    - Check if the system is FLUID_LOOP, if yes then is_cooling_type_fluid_loop equals TRUE  : `if cooling_system_b.cooling_system_type == "FLUID_LOOP": is_cooling_type_fluid_loop = TRUE` 
    - Else, is_cooling_type_fluid_loop = FALSE: `ELse: is_cooling_type_fluid_loop = FALSE`  

**Returns** `return is_cooling_type_fluid_loop`  

**[Back](../_toc.md)**
