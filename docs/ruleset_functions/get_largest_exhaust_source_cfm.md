# get_largest_exhaust_source_cfm  

**Description:** Returns the largest exhaust source cfm in the RMI sent to this function. This is for evaluating G3.1.2.10 exception 6 which states "Where the largest exhaust source is less than 75% of the design outdoor airflow. This exception shall only be used if exhaust air energy recovery is not used in the proposed design. "

**Inputs:**  
- **U,P,or B-RMI**: The RMR in which the largest exhaust source CFM is to be returned.  

**Returns:**  
- **get_largest_exhaust_source_cfm**: Returns the largest exhaust source cfm in the RMI sent to this function. This is for evaluating G3.1.2.10 exception 6 which states "Where the largest exhaust source is less than 75% of the design outdoor airflow. This exception shall only be used if exhaust air energy recovery is not used in the proposed design. "  
 
**Function Call:** None  

## Logic:  
- Set largest exhaust source cfm equal to zero: `Get_largest_exhaust_source_cfm = 0`  
- For each hvac system in the P_RMI: `for hvac_p in P_RMI...HeatingVentilatingAirConditioningSystem`  
    - Create a fan system object: `fan_system_p = hvac_p.fan_system`  
    - Get list of relief fan fan objects: `fan_sys_relief_list = list(fan_system_p.relief_fans)`  
    - Get list of exhaust fan fan objects: `fan_sys_exhaust_list = list(fan_system_p.exhaust_fans)`  
    - Reset the total fan cfm variable: `total_fan_cfm = 0` 
    - Reset the fan cfm variable: `fan_cfm = 0` 
    - Cycle through the list of relief fans: `for fan_p in fan_sys_relief_list:`  
        - Get the fan cfm: `fan_cfm = fan_p.design_airflow`  
        - Total the fan cfm across the multiple fans: `total_fan_cfm = total_fan_cfm + fan_cfm`  
    - Check if the total fan cfm is greater than the current value of Get_largest_exhaust_source_cfm, if it is then set Get_largest_exhaust_source_cfm equal to the cfm: `if total_fan_cfm > Get_largest_exhaust_source_cfm: Get_largest_exhaust_source_cfm = total_fan_cfm`  
    - Reset the total fan cfm variable: `total_fan_cfm = 0`  
    - Reset the fan cfm variable: `fan_cfm = 0` 
    - Cycle through the list of exhaust fans: `for fan_p in fan_sys_exhaust_list:`  
        - Get the fan cfm: `fan_cfm = fan_p.design_airflow`  
        - Total the fan cfm across the multiple fans: `total_fan_cfm = total_fan_cfm + fan_cfm`  
        - Check if the total fan cfm is greater than the current value of Get_largest_exhaust_source_cfm, if it is then set Get_largest_exhaust_source_cfm equal to the cfm: `if total_fan_cfm > Get_largest_exhaust_source_cfm: Get_largest_exhaust_source_cfm = total_fan_cfm`  
- Reset the fan cfm variable: `fan_cfm = 0` 
- Cycle through each zone in the P_RMI: `for zone_p in P_RMI...Zone:`  
    - Check if there are any exhaust fan objects associated with the zone: `if zone_b_obj.zonal_exhaust_fan != Null:`  
        - Get the fan cfm: `fan_cfm = zone_b_obj.zonal_exhaust_fan.design_airflow`    
        - Check if the cfm is greater than the current value of Get_largest_exhaust_source_cfm, if it is then set Get_largest_exhaust_source_cfm equal to the cfm: `if fan_cfm > Get_largest_exhaust_source_cfm: Get_largest_exhaust_source_cfm = fan_cfm`  

**Returns** `return get_largest_exhaust_source_cfm`  

**[Back](../_toc.md)**
