# is_hvac_sys_heating_type_heat_pump   

**Description:** Returns TRUE if the HVAC system has heat pump as the heating system type. Returns FALSE if the HVAC system has anything other than heat pump as the heating system type or if it has more than 1 heating system.   

**Inputs:**  
- **B-RMR**: To evaluate if the hvac system is modeled with heat pump as the heating system type.   
- **hvac_b.id**: The id of the hvac system to evaluate.  

**Returns:**  
- **is_hvac_sys_heating_type_heat_pump**: Returns TRUE if the HVAC system has heat pump as the heating system type. Returns FALSE if the HVAC system has a heating system type other than heat pump as the heating system type.   


## Logic:   
- Set is_hvac_sys_heating_type_heat_pump = FALSE: `is_hvac_sys_heating_type_heat_pump = FALSE`  
- Create an object associate with the heating_system associated with hvac_b: `heating_system_b = hvac_b.heating_system`
- Check if the system is HEAT_PUMP, if yes then is_hvac_sys_heating_type_heat_pump equals TRUE  : `if heating_system_b.heating_system_type == "HEAT_PUMP": is_hvac_sys_heating_type_heat_pump = TRUE`   

**Returns** `return is_hvac_sys_heating_type_heat_pump`  

**[Back](../../../_toc.md)**
