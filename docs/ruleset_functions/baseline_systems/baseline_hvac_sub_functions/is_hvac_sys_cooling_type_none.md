# is_hvac_sys_cooling_type_none  

**Description:** Returns TRUE if the HVAC system cooling type is None or Null. Returns FALSE if the HVAC system has anything other than None or Null for the cooling type or if it has more than 1 or no cooling system.   

**Inputs:**  
- **B-RMR**: To evaluate if the hvac system is modeled with None or null for cooling.   
- **hvac_b.id**: The id of the hvac system to evaluate.  

**Returns:**  
- **is_hvac_sys_cooling_type_none**: Returns TRUE if the HVAC system cooling type is None or Null. Returns FALSE if the HVAC system has anything other than None or Null for the cooling type or if it has more than 1 or no cooling system.  
 
**Function Call:** 
1. is_there_only_one_cooling_system()  

## Logic:   
- Check that there is only one cooling system associated with the HVAC system: `if is_there_only_one_cooling_system(B_RMR,hvac_b.id) == FALSE: is_hvac_sys_cooling_type_none = FALSE`  
- Else, carry on: `Else: `
    - Create an object associate with the cooling_system associated with hvac_b: `cooling_system_b = hvac_b.cooling_system[0]`
    - Check if the system is None or equal to Null, if yes then is_hvac_sys_cooling_type_none equals TRUE  : `if cooling_system_b.cooling_system_type == "None" OR cooling_system_b.cooling_system_type == Null: is_hvac_sys_cooling_type_none = TRUE` 
    - Else, is_hvac_sys_cooling_type_none = FALSE: `ELse: is_hvac_sys_cooling_type_none = FALSE`  

**Returns** `return is_hvac_sys_cooling_type_none`  

**[Back](../../../_toc.md)**

