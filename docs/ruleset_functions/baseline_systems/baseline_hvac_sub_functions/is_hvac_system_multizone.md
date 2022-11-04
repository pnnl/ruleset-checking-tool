# is_hvac_system_multizone  

**Description:** Returns TRUE if the HVAC system serves multiple zones. Returns FALSE if the HVAC system serves a single or no zones.   

**Inputs:**  
- **B-RMR**: To evaluate if the hvac system is modeled as a multizone system.   
- **zone_id_list**: list of zone IDs associated with the HVAC system to be evaluated. These are sent to this function from the master get_baseline_system_types function.

**Returns:**  
- **is_hvac_system_multizone**: Returns TRUE if the HVAC system serves a multiple zones. Returns FALSE if the HVAC system serves zero or one zone.   
 
**Function Call:** None  

## Logic:    
- Set is_hvac_system_multizone = FALSE: `is_hvac_system_multizone = FALSE`  
- Check if the number of zones associated with the HVAC is greater than 1: `if len(zone_ID_list) > 1: is_hvac_system_multizone = TRUE`  

**Returns** `return is_hvac_system_multizone`  

**[Back](../../../_toc.md)**
