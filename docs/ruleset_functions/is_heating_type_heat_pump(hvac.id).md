# is_heating_type_heat_pump   

**Description:** Returns TRUE if the HVAC system has heat pump as the heating system type. Returns FALSE if the HVAC system has anything other than heat pump as the heating system type or if it has more than 1 heating system.   

**Inputs:**  
- **B-RMR**: To evaluate if the hvac system is modeled with heat pump as the heating system type.   
- **hvac_b.id**: The id of the hvac system to evaluate.  

**Returns:**  
- **is_heating_type_heat_pump**: Returns TRUE if the HVAC system has heat pump as the heating system type AND only one heating system . Returns FALSE if the HVAC system has a heating system type other than heat pump as the heating system type or if it has more than one heating system.   
 
**Function Call:** None  

## Logic:   
- Check that there is only one heating system associated with the HVAC system: `if Len(hvac_b.heating_system) != 1: is_heating_type_heat_pump = FALSE`  
- Else, carry on: `Else: `
    - Create an object associate with the heating_system associated with hvac_b: `heating_system_b = hvac_b.heating_system[0]`
    - Check if the system is HEAT_PUMP, if yes then is_heating_type_heat_pump equals TRUE  : `if heating_system_b.heating_system_type == "HEAT_PUMP": is_heating_type_heat_pump = TRUE` 
    - Else, is_heating_type_heat_pump = FALSE: `ELse: is_heating_type_heat_pump = FALSE`  

**Returns** `return is_heating_type_heat_pump`  

**[Back](../_toc.md)**
