# is_hvac_sys_fan_sys_CV  

**Description:** Returns TRUE if the HVAC system fan system is constant volume. Returns FALSE if the HVAC system fan system is anything other than constant volume.   

**Inputs:**  
- **B-RMR**: To evaluate if the hvac system is modeled as constant volume.   
- **hvac_b.id**: The id of the hvac system to evaluate.  

**Returns:**  
- **is_hvac_sys_fan_sys_CV**: Returns TRUE if the HVAC system fan system his constant volume. Returns FALSE if the HVAC system has a fan system that is anything other than constant volume.   
 
**Function Call:** None  

## Logic:   

- Create an object associate with the fan_system associated with hvac_b: `fan_system_b = hvac_b.fan_system`
- Check if the system control is constant volume, if yes then is_hvac_sys_fan_sys_CV equals TRUE  : `if fan_system_b.fan_control == "CONSTANT":is_hvac_sys_fan_sys_CV = TRUE` 
- Else, is_hvac_sys_fan_sys_CV = FALSE: `ELse: is_hvac_sys_fan_sys_CV = FALSE`  

**Returns** `return is_hvac_sys_fan_sys_CV`  



**[Back](../../../_toc.md)**
