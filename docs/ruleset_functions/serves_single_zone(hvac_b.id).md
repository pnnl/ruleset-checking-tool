# serves_single_zone  

**Description:** Returns TRUE if the HVAC system serves a single zone. Returns FALSE if the HVAC system serves multiple zones.   

**Inputs:**  
- **B-RMR**: To evaluate if the hvac system is modeled as a single zone system.   
- **hvac_b.id**: The id of the hvac system to evaluate.  

**Returns:**  
- **serves_single_zone_boolean**: Returns TRUE if the HVAC system serves a single zone. Returns FALSE if the HVAC system serves multiple zones.   
 
**Function Call:** None  
1. get_hvac_zone_list_w_area()  

## Logic:   
- Get dictionary list of baseline zones and the associated HVAC systems: `hvac_zone_list_w_area_dict_b = get_hvac_zone_list_w_area (B_RMR)`  
- Get list of zones that the baseline HVAC system serves: `zone_list_b = hvac_zone_list_w_area_dict_b[hvac_b.id]["ZONE_LIST"]`  
- Check if the number of zones associated with the HVAC system does not equal 1: `if len(zone_list_b) != 1: serves_single_zone_boolean = FALSE`
- Else, serves_single_zone_boolean equals TRUE (HVAC system serves a single zone): `Else: serves_single_zone_boolean = TRUE`

**Returns** `return serves_single_zone_boolean`  

**[Back](../_toc.md)**
