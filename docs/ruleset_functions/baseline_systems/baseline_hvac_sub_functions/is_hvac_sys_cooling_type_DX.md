# is_hvac_sys_cooling_type_DX  

**Description:** Returns TRUE if the HVAC system has DX cooling. Returns FALSE if the HVAC system has anything other than DX cooling.   

**Inputs:**  
- **B-RMR**: To evaluate if the hvac system is modeled with DX cooling.   
- **hvac_b.id**: The id of the hvac system to evaluate.  

**Returns:**  
- **is_hvac_sys_cooling_type_DX**: Returns TRUE if the HVAC system has DX cooling. Returns FALSE if the HVAC system has a cooling system type other than DX.   
 
**Function Call:** 
1. is_there_only_one_cooling_system()  

## Logic:   
- Check that there is only one cooling system associated with the HVAC system: `if is_there_only_one_cooling_system(B_RMR,hvac_b.id) == FALSE: is_hvac_sys_cooling_type_DX = FALSE`  
- Else, carry on: `Else: `
    - Create an object associate with the cooling_system associated with hvac_b: `cooling_system_b = hvac_b.cooling_system[0]`
    - Check if the system is DIRECT_EXPANSION, if yes then is_hvac_sys_cooling_type_DX equals TRUE  : `if cooling_system_b.cooling_system_type == "DIRECT_EXPANSION": is_hvac_sys_cooling_type_DX = TRUE` 
    - Else, is_hvac_sys_cooling_type_DX = FALSE: `ELse: is_hvac_sys_cooling_type_DX = FALSE`  

**Returns** `return is_hvac_sys_cooling_type_DX`  

**[Back](../../../_toc.md)**
