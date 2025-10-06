# does_hvac_system_serve_single_zone  

**Description:** Returns TRUE if the HVAC system serves a single zone. Returns FALSE if the HVAC system serves multiple zones.   

**Inputs:**  
- **B-RMR**: To evaluate if the hvac system is modeled as a single zone system.   
- **zone_id_list**: list of zone IDs associated with the HVAC system to be evaluated. These are sent to this function from the mater get_baseline_system_types function.

**Returns:**  
- **serves_single_zone_boolean**: Returns TRUE if the HVAC system serves a single zone. Returns FALSE if the HVAC system serves multiple zones.   
 
**Function Call:** None  

## Logic:    
- Set serves_single_zone_boolean = TRUE: `serves_single_zone_boolean = TRUE`  
- Check if the number of zones associated with the HVAC system does not equal 1: `if len(zone_ID_list) != 1: serves_single_zone_boolean = FALSE`  

**Returns** `return serves_single_zone_boolean`  

**[Back](../../../_toc.md)**
