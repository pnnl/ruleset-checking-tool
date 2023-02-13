# is_hvac_sys_cooling_type_none  

**Description:** Returns TRUE if the HVAC system cooling type is None or Null. Returns FALSE if the HVAC system has anything other than None or Null for the cooling type.   

**Inputs:**  
- **B-RMR**: To evaluate if the hvac system is modeled with None or null for cooling.   
- **hvac_b.id**: The id of the hvac system to evaluate.  

**Returns:**  
- **is_hvac_sys_cooling_type_none**: Returns TRUE if the HVAC system cooling type is None or Null. Returns FALSE if the HVAC system has anything other than None or Null for the cooling type.  


## Logic:   
- Create an object associate with the cooling_system associated with hvac_b: `cooling_system_b = hvac_b.cooling_system`
- Check if the system is None or equal to Null, if yes then is_hvac_sys_cooling_type_none equals TRUE  : `if cooling_system_b.cooling_system_type == "None" OR cooling_system_b.cooling_system_type == Null: is_hvac_sys_cooling_type_none = TRUE` 
- Else, is_hvac_sys_cooling_type_none = FALSE: `ELse: is_hvac_sys_cooling_type_none = FALSE`  

**Returns** `return is_hvac_sys_cooling_type_none`  

**[Back](../../../_toc.md)**
