# is_fan_CV  

**Description:** Returns TRUE if the HVAC system fan system is constant volume. Returns FALSE if the HVAC system fan system is anything other than constant volume.   

**Inputs:**  
- **B-RMR**: To evaluate if the hvac system is modeled as constant volume.   
- **hvac_b.id**: The id of the hvac system to evaluate.  

**Returns:**  
- **is_fan_CV**: Returns TRUE if the HVAC system fan system his constant volume. Returns FALSE if the HVAC system has a fan system that is anything other than constant volume.   
 
**Function Call:** None  

## Logic:   

- Create an object associate with the fan_system associated with hvac_b: `fan_system_b = hvac_b.fan_system[0]`
- Check if the system control is constant volume, if yes then is_fan_CV equals TRUE  : `if fan_system_b.fan_control == "CONSTANT":is_fan_CV = TRUE` 
- Else, is_fan_CV = FALSE: `ELse: is_fan_CV = FALSE`  

**Returns** `return is_fan_CV`  

**Notes**
1. Should we also check if associated terminal_b.type != "CONSTANT_AIR_VOLUME" as well for this function?


**[Back](../_toc.md)**
