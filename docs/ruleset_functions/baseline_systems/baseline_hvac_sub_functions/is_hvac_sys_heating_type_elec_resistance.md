# is_hvac_sys_heating_type_elec_resistance 

**Description:** Returns TRUE if the HVAC system heating system heating type is ELECTRIC_RESISTANCE. Returns FALSE if the HVAC system heating system has anything other than ELECTRIC_RESISTANCE.   

**Inputs:**  
- **B-RMR**: To evaluate if the hvac system is modeled with a heating type of ELECTRIC_RESISTANCE.   
- **hvac_b.id**: The id of the hvac system to evaluate.  

**Returns:**  
- **is_hvac_sys_heating_type_elec_resistance**: Returns TRUE if the HVAC system heating system has ELECTRIC_RESISTANCE as the heating type. Returns FALSE if the HVAC system has a heating system type other than ELECTRIC_RESISTANCE.   
 
**Function Call:**  None  

## Logic:   
- Set is_hvac_sys_heating_type_elec_resistance = FALSE: `is_hvac_sys_heating_type_elec_resistance = FALSE`  
- Create an object associate with the heating_system associated with hvac_b: `heating_system_b = hvac_b.heating_system`
- Check if the system type is ELECTRIC_RESISTANCE, if yes then is_hvac_sys_heating_type_elec_resistance equals TRUE: `if heating_system_b.heating_system_type == "ELECTRIC_RESISTANCE": is_hvac_sys_heating_type_elec_resistance = TRUE`  

**Returns** `return is_hvac_sys_heating_type_elec_resistance`  

**[Back](../../../_toc.md)**

