# get_hvac_sys_and_assoc_zones_largest_exhaust_source  

**Description:** Returns a list with the sum of the hvac fan system exhaust fan flow values, the maximum zone level exhaust source across the zones associated with the HVAC system, the number of exhaust fans associated with the hvac fan system, and the maximum flow of all of the exhaust fans associated with the hvac system fan system [hvac_sys_exhaust_flow_sum, maximum_zone_exhaust, num_hvac_exhaust_fans, maximum_hvac_exhaust]. This is for evaluating G3.1.2.10 exception 6 which states "Where the largest exhaust source is less than 75% of the design outdoor airflow. This exception shall only be used if exhaust air energy recovery is not used in the proposed design. "

**Inputs:**  
- **U,P,or B-RMD**: The RMD in which the largest exhaust source flow is to be returned.  
- **hvac_sys**: The hvac system object for which the largest exhaust source is being determined.

**Returns:**  
- **get_hvac_sys_and_assoc_zones_largest_exhaust_source**: Returns a dict with the following form: { "hvac_sys_exhaust_flow_sum": the sum of the hvac fan system exhaust fan flow rates, "maximum_zone_exhaust_flow": the maximum zone level exhaust source across the zones associated with the HVAC system, "num_hvac_exhaust_fans": the number of exhaust fans associated with the hvac fan system, "maximum_hvac_exhaust_flow": the maximum flow rate of all of the exhaust fans associated with the hvac system fan system }
 
**Function Call:**   
1. get_dict_of_zones_and_terminal_units_served_by_hvac_sys()   


## Logic:  
- Create dictionary of hvac systems, zones, and terminal units: `dict_of_zones_and_terminal_units_served_by_hvac_sys = get_dict_of_zones_and_terminal_units_served_by_hvac_sys(B_RMI)`  
- Get the list of zones associated with the hvac system: `zone_list = dict_of_zones_and_terminal_units_served_by_hvac_sys[hvac_sys.id]["ZONE_LIST"]`  
- Set largest zone exhaust source flow equal to zero: `maximum_zone_exhaust = 0`  
- Set largest hvac exhaust flow equal to zero: `maximum_hvac_exhaust = 0`  
- Create a fan system object: `fan_system_b = sys.fan_system`   
- Get list of exhaust fan fan objects: `fan_sys_exhaust_list = list(fan_system_b.exhaust_fans)`  
- Get the number of exhaust fans associated with the hvac system: `num_hvac_exhaust_fans = len(fan_sys_exhaust_list)`  
- Reset the total fan flow variable: `total_fan_flow = 0` 
- Reset the fan flow variable: `fan_flow = 0` 
- Check if the num_hvac_exhaust_fans is greater than 0: `if num_hvac_exhaust_fans > 0:`  
    - Cycle through the list of exhaust fans: `for fan_b in fan_sys_exhaust_list:`  
        - Get the fan flow: `fan_flow = fan_b.design_airflow`  
        - Total the fan flow across the multiple fans: `total_fan_flow = total_fan_flow + fan_flow`  
        - Check if the fan flow is greater than maximum_hvac_exhaust, if it is then set the maximum_hvac_exhaust equal to the fan flow: `if fan_flow > maximum_hvac_exhaust: maximum_hvac_exhaust = fan_flow`  
- Set hvac_sys_exhaust_flow_sum equal to the sum of hvac system exhaust fan flow (this assumes the hvac system exhaust fans are collectively considered one source and sums them as if they were in paraellel): `hvac_fan_sys_exhaust_sum = total_fan_flow`  
- Reset the fan flow variable: `fan_flow = 0` 
- Cycle through each zone associated with the HVAC system in the B_RMI: `for zone_b in zone_list:`  
    - Check if there are any exhaust fan objects associated with the zone: `if zone_b_obj.zonal_exhaust_fan != Null:`  
        - Get the fan flow: `fan_flow = zone_b_obj.zonal_exhaust_fan.design_airflow`    
        - Check if the flow is greater than the current value of maximum_zone_exhaust, if it is then set maximum_zone_exhaust equal to the flow: `if fan_flow > maximum_zone_exhaust: maximum_zone_exhaust = fan_flow`  
- Create dictionary to be returned by function: `get_hvac_sys_and_assoc_zones_largest_exhaust_source_dict  = {"hvac_sys_exhaust_flow_sum": hvac_fan_sys_exhaust_sum, "maximum_zone_exhaust_flow": maximum_zone_exhaust, "num_hvac_exhaust_fans": num_hvac_exhaust_fans, "maximum_hvac_exhaust_flow": maximum_hvac_exhaust}`  

**Returns** `return get_hvac_sys_and_assoc_zones_largest_exhaust_source`  

**[Back](../_toc.md)**