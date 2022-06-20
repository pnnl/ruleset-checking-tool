# is_baseline_system_1  

**Description:** Get a TRUE or FALSE output as to whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 1.  

**Inputs:**  
- **B-RMR**: To evaluate if the hvac system is modeled as system 1 in the B_RMR.   
- **hvac_b.id**: The id of the hvac system to evaluate.  

**Returns:**  
- **is_baseline_system_1**: The functions returns TRUE if the system is system 1 and FALSE if the system is not system 1.  
 
**Function Call:** 
1. get_hvac_zone_list_w_area()   

## Logic:  
- Set the is_baseline_system_1 boolean variable to true (if it does not meet the criteria below then it gets set to false): `is_baseline_system_1 = TRUE`  
- Create an object associated with the hvac system: `hvac_b = hvac_b.id`  
- Check that there is only one heating system, one cooling system, that a fan system is defined, and that there is no preheat system associated with the HVAC system. If any of these criteria are not met then the function should return FALSE and no need to carry on with remaining logic: `if Len(hvac_b.heating_system) != 1 OR Len(hvac_b.cooling_system) != 1 AND Len(hvac_b.fan_system) != 1 AND Len(hvac_b.preheat_system) != Null: is_baseline_system_1 = FALSE`  
- Create an object associate with the heating_system associated with hvac_b: `heating_system_b = hvac_b.heating_system[0]`
- Check that the data elements associated with the heating_system align with system 1, if not then the function should return FALSE and no need to carry on with remaining logic: `if heating_system_b.heating_system_type != "FLUID_LOOP": is_baseline_system_1 = FALSE`
- Check if is_baseline_system_1 equals TRUE: `if is_baseline_system_1 == TRUE:`  
    - Create an object associate with the cooling_system associated with hvac_b: `cooling_system_b = hvac_b.cooling_system[0]`
    - Check that the data elements associated with the cooling_system align with system 1, if not then the function should return FALSE and no need to carry on with remaining logic: `if cooling_system_b.cooling_system_type != "DIRECT_EXPANSION": is_baseline_system_1 = FALSE` 
    - Check if is_baseline_system_1 equals TRUE: `if is_baseline_system_1 == TRUE:`  
        - Create an object associate with the fan_system associated with hvac_b: `fan_system_b = hvac_b.fan_system[0]`
        - Check that the data elements associated with the fan_system align with system 1, if not then the function should return FALSE and no need to carry on with remaining logic (QUESTION: SHOULD I BE CHECKING ANYTHING ELSE FOR THE FAN_SYSTEM LIKE # OF FANS OR ANYTHING OR ARE THESE CHECKED ELSEWHERE? ALSO, I KNOW APP G SAYS "The calculated system fan power shall be distributed to supply, return, exhaust, andrelief fans in the same proportion as the proposed design." but PTACS only have a supply fan so should these units only have one supply fan and no other fan types? This has always been an area of confusion for me ): `if fan_system_b.fan_control != "CONSTANT": is_baseline_system_1 = FALSE` 
        - Check if is_baseline_system_1 equals TRUE: `if is_baseline_system_1 == TRUE:`  
            - Get dictionary list of baseline zones and the associated HVAC systems: `hvac_zone_list_w_area_dict_b = get_hvac_zone_list_w_area (B_RMR)`  
            - Get list of zones that the HVAC system serves (should only be one): `zone_list_b = hvac_zone_list_w_area_dict_b[hvac_b.id]["ZONE_LIST"]`  
            - Check that there is a zone associated with the HVAC system and that there is only one zone in the zone list, if not then the function should return FALSE and no need to carry on with remaining logic: `if len(zone_list_b) == 0 OR zone_list_b == Null OR len(zone_list_b) > 1: is_baseline_system_1 = FALSE`  
            - Create an object for the zone associated with the HVAC system: `zone_b = zone_list_b[0]`
            - Check that there is a terminal unit associated with the zone and that there is only one terminal unit associated with the zone, if not then the function should return FALSE and no need to carry on with remaining logic: `if len(zone_b.terminals) != 1: is_baseline_system_1 = FALSE`  
            - Create an object for the terminal unit associated with the zone: `terminal_b = zone_b.terminals[0]`  
            - Check that the data elements associated with the terminal unit align with system 1, if not then the function should return FALSE and no need to carry on with remaining logic: `if terminal_b.heating_source != "None" or terminal_b.cooling_source != "None" or terminal_b.fan != Null or terminal_b.type != "CONSTANT_AIR_VOLUME" or terminal_b.is_supply_ducted != FALSE: is_baseline_system_1 = FALSE`  

**Returns** `is_baseline_system_1`  

**[Back](../_toc.md)**