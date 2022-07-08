# is_heating_type_heat_pump   

**Description:** Returns TRUE if the HVAC system has DX heating. Returns FALSE if the HVAC system has anything other than DX heating or if it has more than 1 heating system.   

**Inputs:**  
- **B-RMR**: To evaluate if the hvac system is modeled with DX heating.   
- **hvac_b.id**: The id of the hvac system to evaluate.  

**Returns:**  
- **is_heating_type_DX**: Returns TRUE if the HVAC system has DX heating AND only one heating system . Returns FALSE if the HVAC system has a heating system type other than DX or if it has more than one heating system.   
 
**Function Call:** None  

## Logic:   
- Check that there is only one heating system associated with the HVAC system: `if Len(hvac_b.heating_system) != 1: is_heating_type_DX = FALSE`  
- Else, carry on: `Else: `
    - Create an object associate with the heating_system associated with hvac_b: `heating_system_b = hvac_b.heating_system[0]`
    - Check if the system is DIRECT_EXPANSION, if yes then is_heating_type_DX equals TRUE  : `if heating_system_b.heating_system_type == "DIRECT_EXPANSION": is_heating_type_DX = TRUE` 
    - Else, is_heating_type_DX = FALSE: `ELse: is_heating_type_DX = FALSE`  

**Returns** `return is_heating_type_DX`  

**[Back](../_toc.md)**
