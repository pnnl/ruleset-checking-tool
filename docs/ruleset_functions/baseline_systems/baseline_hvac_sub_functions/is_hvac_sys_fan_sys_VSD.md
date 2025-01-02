# is_hvac_sys_fan_sys_VSD  

**Description:** Returns TRUE if the HVAC system fan system is variable speed drive controlled. Returns FALSE if the HVAC system fan system is anything other than variable speed drive controlled.   

**Inputs:**  
- **B-RMR**: To evaluate if the hvac system is modeled as variable speed drive controlled.   
- **hvac_b.id**: The id of the hvac system to evaluate.  

**Returns:**  
- **is_hvac_sys_fan_sys_VSD**: Returns TRUE if the HVAC system fan system his variable speed drive control. Returns FALSE if the HVAC system has a fan system that is anything other than variable speed drive controlled.   
 
**Function Call:** None  

## Logic:   
- Set is_hvac_sys_fan_sys_VSD = FALSE: `is_hvac_sys_fan_sys_VSD = FALSE`  
- Create an object associate with the fan_system associated with hvac_b: `fan_system_b = hvac_b.fan_system`
- Check if the system control is variable speed drive control, if yes then is_hvac_sys_fan_sys_VSD equals TRUE  : `if fan_system_b.fan_control == "VARIABLE_SPEED_DRIVE":is_hvac_sys_fan_sys_VSD = TRUE` 

**Returns** `return is_hvac_sys_fan_sys_VSD`  



**[Back](../../../_toc.md)**
