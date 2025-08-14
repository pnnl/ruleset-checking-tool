# is_hvac_sys_cooling_type_none_or_non_mechanical  

**Description:** Returns TRUE if the HVAC system cooling type is None or Null or non_mechanical. Returns FALSE if the HVAC system has anything other than None or Null or or non_mechanical for the cooling type.   

**Inputs:**  
- **B-RMR**: To evaluate if the hvac system is modeled with None or null or or non_mechanical for cooling.   
- **hvac_b.id**: The id of the hvac system to evaluate.  

**Returns:**  
- **is_hvac_sys_cooling_type_none_or_non_mechanical**: Returns TRUE if the HVAC system cooling type is None or Null or or non_mechanical. Returns FALSE if the HVAC system has anything other than None or Null or or non_mechanical for the cooling type.  


## Logic:   
- Create an object associate with the cooling_system associated with hvac_b: `cooling_system_b = hvac_b.cooling_system`
- Check if the system is None or equal to Null or equal to or non_mechanical, if yes then is_hvac_sys_cooling_type_none_or_non_mechanical equals TRUE  : `if cooling_system_b.cooling_system_type == "None" OR cooling_system_b.cooling_system_type == Null or OR cooling_system_b.cooling_system_type == "NON_MECHANICAL": is_hvac_sys_cooling_type_none_or_non_mechanical = TRUE` 
- Else, is_hvac_sys_cooling_type_none_or_non_mechanical = FALSE: `ELse: is_hvac_sys_cooling_type_none_or_non_mechanical = FALSE`  

**Returns** `return is_hvac_sys_cooling_type_none_or_non_mechanical`  

**[Back](../../../_toc.md)**