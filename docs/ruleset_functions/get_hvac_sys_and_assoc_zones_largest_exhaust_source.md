# get_hvac_sys_and_assoc_zones_largest_exhaust_source  

**Description:** Returns a list with the largest exhaust source cfm associated with an hvac system and the zones it serves and the number of exhaust fans associated with the HVAC system [get_hvac_sys_and_assoc_zones_largest_exhaust_source,  num_hvac_exhaust_fans ]. This is for evaluating G3.1.2.10 exception 6 which states "Where the largest exhaust source is less than 75% of the design outdoor airflow. This exception shall only be used if exhaust air energy recovery is not used in the proposed design. "

**Inputs:**  
- **U,P,or B-RMI**: The RMI in which the largest exhaust source CFM is to be returned.  
- **hvac_sys**: The hvac system object for which the largest exhaust source is being determined.

**Returns:**  
- **get_hvac_sys_and_assoc_zones_largest_exhaust_source**: Returns a list with the largest exhaust source cfm associated with an hvac system and the zones it serves and the number of exhaust fans associated with the HVAC system [get_hvac_sys_and_assoc_zones_largest_exhaust_source,  num_hvac_exhaust_fans ].This is for evaluating G3.1.2.10 exception 6 which states "Where the largest exhaust source is less than 75% of the design outdoor airflow. This exception shall only be used if exhaust air energy recovery is not used in the proposed design. "  
 
**Function Call:**   
1. get_dict_of_zones_and_terminal_units_served_by_hvac_sys()   


## Logic:  
- Create dictionary of hvac systems, zones, and terminal units: `dict_of_zones_and_terminal_units_served_by_hvac_sys = get_dict_of_zones_and_terminal_units_served_by_hvac_sys(B_RMI)`  
- Get the list of zones associated with the hvac system: `zone_list = dict_of_zones_and_terminal_units_served_by_hvac_sys[hvac_sys.id]["ZONE_LIST"]`  
- Set largest exhaust source cfm equal to zero: `get_hvac_sys_and_assoc_zones_largest_exhaust_source = 0`  
- Create a fan system object: `fan_system_p = sys.fan_system`   
- Get list of exhaust fan fan objects: `fan_sys_exhaust_list = list(fan_system_p.exhaust_fans)`  
- Get the number of exhaust fans associated with the hvac system: `num_hvac_exhaust_fans = len(fan_sys_exhaust_list)`  
- Reset the total fan cfm variable: `total_fan_cfm = 0` 
- Reset the fan cfm variable: `fan_cfm = 0` 
- Check if the num_hvac_exhaust_fans is greater than 0: `if num_hvac_exhaust_fans >0:`  
    - Cycle through the list of exhaust fans: `for fan_p in fan_sys_exhaust_list:`  
        - Get the fan cfm: `fan_cfm = fan_p.design_airflow`  
        - Total the fan cfm across the multiple fans: `total_fan_cfm = total_fan_cfm + fan_cfm`  
- Set the largest exhaust source (this considers the sum of hvac system exhaust fan cfm to be one source of exhaust): `get_hvac_sys_and_assoc_zones_largest_exhaust_source = total_fan_cfm`  
- Reset the fan cfm variable: `fan_cfm = 0` 
- Cycle through each zone associated with the HVAC system in the B_RMI: `for zone_b in zone_list:`  
- Check if there are any exhaust fan objects associated with the zone: `if zone_b_obj.zonal_exhaust_fan != Null:`  
    - Get the fan cfm: `fan_cfm = zone_b_obj.zonal_exhaust_fan.design_airflow`    
    - Check if the cfm is greater than the current value of get_hvac_sys_and_assoc_zones_largest_exhaust_source, if it is then set get_hvac_sys_and_assoc_zones_largest_exhaust_source equal to the cfm: `if fan_cfm > get_hvac_sys_and_assoc_zones_largest_exhaust_source: get_hvac_sys_and_assoc_zones_largest_exhaust_source = fan_cfm`  

**Returns** `return [get_hvac_sys_and_assoc_zones_largest_exhaust_source, num_hvac_exhaust_fans]`  

**[Back](../_toc.md)**