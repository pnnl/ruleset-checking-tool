# is_economizer_modeled_in_proposed  

**Description:** Returns true or false. The function returns true if at least one zone served by the baseline HVAC system sent to the function is served by an hvac system with an economizer in the proposed design. The function returns false otherwise. 

**Inputs:**  
- **B_RMI**: The B_RMI in which the baseline hvac system object is defined. 
- **P_RMI**: The P_RMI that is being checked for a modeled economizer. 
- **hvac**: The baseline hvac system object.

**Returns:**  
- **is_economizer_modeled_in_proposed**: Returns true or false. Returns true or false. The function returns true if at least one zone served by the baseline HVAC system sent to the function is served by an hvac system with an economizer in the proposed design. The function returns false otherwise.      
 
**Function Call:**  
1. Get_list_hvac_systems_associated_with_zone()   
2. get_hvac_zone_list_w_area()   
3. match_data_element()   

## Logic:  
- Create dictionary with hvac iD and zone id list: `hvac_zone_list_w_area_dict = get_hvac_zone_list_w_area(B_RMI)`  
- Reset is_economizer_modeled_in_proposed boolean variable to FALSE: `is_economizer_modeled_in_proposed =  FALSE`  
- Get zone ids associated with the HVAC system: `zone_list_b = hvac_zone_list_w_area_dict[hvac.id]["ZONE_LIST"]`  
- Check if any of the zones are served by an economizer in the proposed design model, start by cycling through each zone served by the baseline HVAC system: `for zone_b in zone_list_b:`  
    - Get analogous zone ID in the P_RMI: `zone_p = match_data_element(P_RMI,Zone,zone_b)`  
    - Get list of HVAC system IDs associated with the zone in the proposed: `hvac_sys_list_p = Get_list_hvac_systems_associated_with_zone(P_RMI, zone_p)`  
    - Loop through each HVAC system and check if it is equipped with an economizer, if it is then set is_economizer_modeled_in_proposed equal to TRUE : `for hvac_p in hvac_sys_list_p:`  
        - Convert hvac_p (which is an ID) to an HVAC object (however the RCT team does this, if this is even needed): `hvac_p_obj = hvac_p`  
        - Check if the HVAC system is equipped with an economizer: `if hvac_p_obj.fan_system.AirEconomizer != Null AND hvac_p_obj.fan_system.AirEconomizer.type != "FIXED_FRACTION": is_economizer_modeled_in_proposed = TRUE`       

**Returns** `return is_economizer_modeled_in_proposed`  

**Comments/Questions**  None   


**[Back](../_toc.md)**
