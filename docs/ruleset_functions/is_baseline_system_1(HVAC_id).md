# is_baseline_system_1  

**Description:** Get a TRUE or FALSE output as to whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 1.  

**Inputs:**  
- **B-RMR**: To evaluate if the hvac system is modeled as system 1 in the B_RMR.   
- **hvac_b.id**: The id of the hvac system to evaluate.  

**Returns:**  
- **is_baseline_system_1**: The functions returns TRUE if the system is system 1 and FALSE if the system is not system 1.  
 
**Function Call:** 
1. get_hvac_zone_list_w_area()  
2. is_heating_type_fluid_loop()
3. is_cooling_type_DX()
4. serves_single_zone()

## Logic:  
- Set the is_baseline_system_1 boolean variable to true (if it does not meet the criteria below then it gets set to false): `is_baseline_system_1 = TRUE`  
- Create an object associated with the hvac system: `hvac_b = hvac_b.id`  
- Check that there is no preheat system: `if Len(hvac_b.preheat_system) != Null: is_baseline_system_1 = FALSE`  
- Check if is_baseline_system_1 = TRUE, if it does carry on: `if is_baseline_system_1 == TRUE:`   
    - Check if heatingsystem is a fluid_loop: `if is_heating_type_fluid_loop(B_RMR, hvac_b.id) == FALSE: is_baseline_system_1 = FALSE`   
    - Check if is_baseline_system_1 equals TRUE: `if is_baseline_system_1 == TRUE:`  
        - Check if coolingsystem is DX: `if is_cooling_type_DX(B_RMR, hvac_b.id) == FALSE: is_baseline_system_1 = FALSE`
        - Check if is_baseline_system_1 equals TRUE: `if is_baseline_system_1 == TRUE:`  
            - Check if fansystem is constant volume: `if is_cooling_type_DX(B_RMR, hvac_b.id) == FALSE: is_baseline_system_1 = FALSE`
            - Check if is_baseline_system_1 equals TRUE: `if is_baseline_system_1 == TRUE:`  
                - Get dictionary list of baseline zones and the associated HVAC systems: `hvac_zone_list_w_area_dict_b = get_hvac_zone_list_w_area (B_RMR)`  
                - Get list of zones that the HVAC system serves (should only be one): `zone_list_b = hvac_zone_list_w_area_dict_b[hvac_b.id]["ZONE_LIST"]`  
                - Check that there is a zone associated with the HVAC system and that there is only one zone in the zone list, if not then the function should return FALSE and no need to carry on with remaining logic: `if len(zone_list_b) == 0 OR zone_list_b == Null OR len(zone_list_b) > 1: is_baseline_system_1 = FALSE`  
                - Create an object for the zone associated with the HVAC system: `zone_b = zone_list_b[0]`
                - Check that there is a terminal unit associated with the zone and that there is only one terminal unit associated with the zone, if not then the function should return FALSE and no need to carry on with remaining logic: `if len(zone_b.terminals) != 1: is_baseline_system_1 = FALSE`  
                - Check if is_baseline_system_1 equals TRUE: `if is_baseline_system_1 == TRUE:`  
                    - Create an object for the terminal unit associated with the zone: `terminal_b = zone_b.terminals[0]`  
                    - Check that the data elements associated with the terminal unit align with system 1, if not then the function should return FALSE: `if terminal_b.heating_source != "None" or terminal_b.cooling_source != "None" or terminal_b.fan != Null or terminal_b.type != "CONSTANT_AIR_VOLUME": is_baseline_system_1 = FALSE`  

**Returns** `is_baseline_system_1`  

**Notes**
1. To limit redundant coding. I am thinking that we should also check to see if it is Sys-1, Sys-1a, Sys-1b, or Sys-1c in the same function and return strings of either Sys-1, Sys-1a, Sys-1b, Sys-1c, or Not_Sys_1.

**[Back](../_toc.md)**