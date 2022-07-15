# is_there_only_one_heating_system  

**Description:** Returns TRUE if the HVAC system has only one heating system associated with it. Returns FALSE if the HVAC system has anything other than 1 heating system associated with it.   

**Inputs:**  
- **B-RMR**: To evaluate if the HVAC system has only one heating system associated with it.   
- **hvac_b.id**: The id of the hvac system to evaluate.  

**Returns:**  
- **is_there_only_one_heating_system**: Returns TRUE if the HVAC system has only one heating system associated with it. Returns FALSE if the HVAC system has anything other than 1 heating system associated with it.      
 
**Function Call:** None  

## Logic:   
- Check if there is only one heating system associated with the HVAC system: `if Len(hvac_b.heating_system) != 1: is_there_only_one_heating_system = FALSE`  
- Else: `Else: is_there_only_one_heating_system =  TRUE `

**Returns** `return is_there_only_one_heating_system`  

**[Back](../_toc.md)**
