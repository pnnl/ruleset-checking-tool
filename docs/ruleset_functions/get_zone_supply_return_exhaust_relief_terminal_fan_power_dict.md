# get_zone_supply_return_exhaust_relief_terminal_fan_power_dict

**Description:** Get the supply, return, exhaust, relief, and terminal total fan power for each zone. The function returns a dictionary that saves each zone's supply, return, exhaust, relief  and terminal unit fan power as a list {zone.id: [supply fan power kW, return fan power kW, exhaust fan power kW, relief fan power kW, terminal fan power]}. Values will be equal to zero where not defined for a fan system. Zonal exhaust and non-mechanical cooling is not included.
This function first identifies if a HVAC system is serving more than one zone, in which case the fan power is apportioned to the zone based on the fraction of airflow to that zone. For single zone systems, the fan power associated with the hvac system is added to the zone fan power. For systems defined at the terminal, such as FPFCU, it sums up the fan power specified at the terminal and assigns it to the zone.

**Inputs:**  
- **B-RMD,P-RMD**: To calculate the supply, return, exhaust, relief, and terminal unit total fan power for each zone in the ruleset model instance.   

**Returns:**  
- **get_zone_supply_return_exhaust_relief_terminal_fan_power_dict**: The function returns a dictionary that saves each zone's supply, return, exhaust, relief and terminal fan power as a list {zone.id: {supply_fans_power: value, return_fans_power: value, exhaust_fans_power: value, relief_fans_power: value, terminal_fans_power: value}}. Values will be equal to zero where not defined for a fan system. Zonal exhaust and non-mechanical cooling is not included.

**Function Call:**  
1. get_dict_of_zones_and_terminal_units_served_by_hvac_sys()   
2. get_list_hvac_systems_associated_with_zone()   
3. get_fan_object_electric_power()  
4. get_fan_system_object_supply_return_exhaust_relief_total_kW_CFM()  


## Logic:    
- Create dictionary of hvac systems and associated zones and terminal units: `dict_of_zones_and_terminal_units_served_by_hvac_sys_x = get_dict_of_zones_and_terminal_units_served_by_hvac_sys(RMD)`  
- For each Zone in the RMD (whichever is sent to this function): `for zone in RMD...Zone:`  
    - Reset the zone total supply fan power variable: `zone_total_supply_fan_power = 0`
    - Reset the zone total return fan power variable: `zone_total_return_fan_power = 0`  
    - Reset the zone total exhaust fan power variable: `zone_total_exhaust_fan_power = 0`  
    - Reset the zone total relief fan power variable: `zone_total_relief_fan_power = 0`
    - Reset the zone total terminal fan power variable: `zone_total_terminal_fan_power = 0`  
    
    - Add zonal exhaust fan power to zone_total_exhaust_fan_power: `if zone.zone_exhaust_fans ? zone_total_exhaust_fan_power = get_fan_object_electric_power(P_RMI,zone.zonal_exhaust_fan)`
    - Get a list of HVAC systems serving the zone: `hvac_sys_list_serving_zone_x =  get_list_hvac_systems_associated_with_zone(RMD,zone.id)`  
    - For each hvac system serving the zone: `for hvac in hvac_sys_list_serving_zone_x:`  
        - Reset total_terminal_air_flow variable to 0 (total across all zones served): `total_terminal_air_flow = 0`  
        - Reset the zone_primary_air_flow variable to 0: `zone_primary_air_flow = 0`  
        - Check if there is a fan system associated with the hvac system (if not then assume the fan is defined at the terminal unit like it is for a four pipe fan coil units and go to Else): `if hvac.fan_system != Null:`  
            - Get list of zones served by the hvac system: `zone_list_hvac_sys_x = dict_of_zones_and_terminal_units_served_by_hvac_sys_x[hvac.id]["ZONE_LIST"]`  
            - Check if the hvac system serves more than one zone, if it does then carry on, if not then go to Else: `if len(zone_list_hvac_sys_x) >1:`  
                - Get list of terminal units served by the hvac system: `terminal_list_hvac_sys_x = dict_of_zones_and_terminal_units_served_by_hvac_sys_x[hvac.id]["Terminal_Unit_List"]`  
                - For each terminal unit served by the HVAC system: `for terminal in terminal_list_hvac_sys_x:`  
                    - Get the primary air flow: `primary_air_flow_terminal = terminal.primary_airflow`  
                    - Add to the total cfm across all terminals served by the HVAC system: `total_terminal_air_flow = total_terminal_air_flow + primary_air_flow_terminal`  
                    - Get the terminal unit fan power: `terminal_fan_power = get_fan_object_electric_power(RMD,terminal.fan)`  
                    - Check if the terminal unit is associated with this zone: `if terminal in zone.terminals:`   
                        - Add to the primary flow for the zone for this hvac system:  `zone_primary_air_flow = zone_primary_air_flow + primary_air_flow_terminal`  
                        - Add to the terminal fan power for the zone for this hvac system:  `zone_total_terminal_fan_power = zone_total_terminal_fan_power + terminal_fan_power`  
                - Get dictionary of the hvac system's fan system's supply, return, exhaust and relief fan powers in kW: `fan_sys_powers =(get_fan_system_object_supply_return_exhaust_relief_total_kW_CFM(RMD,hvac.fan_system)`  
                - Get the hvac system total supply fan kW, need to get the first element in the list of fan powers:`hvac_sys_total_supply_fan_power = fan_sys_powers['supply_fan_power]` 
                - Get the hvac system total return fan kW, need to get the second element in the list of fan powers:`hvac_sys_total_return_fan_power = fan_sys_powers['return_fan_power']` 
                - Get the hvac system total exhaust fan kW, need to get the third element in the list of fan powers:`hvac_sys_total_exhaust_fan_power = fan_sys_powers['exhaust_fan_power'']` 
                - Get the hvac system total relief fan kW, need to get the fourth element in the list of fan powers:`hvac_sys_total_relief_fan_power = fan_sys_powers['relief_fan_power']`     

                - Apportion the supply kW to this zone based on the terminal unit primary flow for the zone and the total primary terminal unit flow across all zones that this HVAC system serves: `zone_total_supply_fan_power = zone_total_supply_fan_power + (hvac_sys_total_supply_fan_power * (zone_primary_air_flow/total_terminal_air_flow))`    
                - Apportion the return kW to this zone based on the terminal unit primary flow for the zone and the total primary terminal unit flow across all zones that this HVAC system serves: `zone_total_return_fan_power = zone_total_return_fan_power + (hvac_sys_total_return_fan_power * (zone_primary_air_flow/total_terminal_air_flow))`  
                - Apportion the exhaust kW to this zone based on the terminal unit primary flow for the zone and the total primary terminal unit flow across all zones that this HVAC system serves: `zone_total_exhaust_fan_power = zone_total_exhaust_fan_power + (hvac_sys_total_exhaust_fan_power * (zone_primary_air_flow/total_terminal_air_flow))`  
                - Apportion the relief kW to this zone based on the terminal unit primary flow for the zone and the total primary terminal unit flow across all zones that this HVAC system serves: `zone_total_relief_fan_power = zone_total_relief_fan_power + (hvac_sys_total_relief_fan_power * (zone_primary_air_flow/total_terminal_air_flow))`  

            - Else, the HVAC system serves a single zone: `Else:`  
                - Get dictionary of the hvac system's fan system's supply, return, exhaust and relief fan powers in kW: `fan_sys_powers =(get_fan_system_object_supply_return_exhaust_relief_total_kW_CFM(RMD,hvac.fan_system)`  
                - Get the hvac system total supply fan kW, need to get the first element in the list of fan powers:`hvac_sys_total_supply_fan_power = fan_sys_powers['supply_fan_power]` 
                - Get the hvac system total return fan kW, need to get the second element in the list of fan powers:`hvac_sys_total_return_fan_power = fan_sys_powers['return_fan_power']` 
                - Get the hvac system total exhaust fan kW, need to get the third element in the list of fan powers:`hvac_sys_total_exhaust_fan_power = fan_sys_powers['exhaust_fan_power'']` 
                - Get the hvac system total relief fan kW, need to get the fourth element in the list of fan powers:`hvac_sys_total_relief_fan_power = fan_sys_powers['relief_fan_power']`     

                - Add the supply kW to this zone: `zone_total_supply_fan_power = zone_total_supply_fan_power + hvac_sys_total_supply_fan_power`    
                - Add the return kW to this zone: `zone_total_return_fan_power = zone_total_return_fan_power + hvac_sys_total_return_fan_power` 
                - Add the exhaust kW to this zone: `zone_total_exhaust_fan_power = zone_total_exhaust_fan_power + hvac_sys_total_exhaust_fan_power`  
                - Add the relief kW to this zone: `zone_total_relief_fan_power = zone_total_relief_fan_power + hvac_sys_total_relief_fan_power` 

                - Get list of terminal units served by the hvac system: `terminal_list_hvac_sys_x = dict_of_zones_and_terminal_units_served_by_hvac_sys_x[hvac.id]["ZONE_LIST"]["Terminal_Unit_List"]`  
                - For each terminal unit served by the HVAC system: `for terminal in terminal_list_hvac_sys_x:`  
                - Get the terminal unit fan power: `terminal_fan_power = get_fan_object_electric_power(RMD,terminal.fan)`  
                - Add to the total terminal kW associated with the zone: `zone_total_terminal_fan_power = zone_total_terminal_fan_power + terminal_fan_power`  

        - Else, the hvac fan system equals Null meaning that the fan is defined at the terminal unit level like it is for a four pipe fan coil unit: `Else:`  
            - Get list of zones served by the hvac system: `zone_list_hvac_sys_x = dict_of_zones_and_terminal_units_served_by_hvac_sys_x[hvac.id]["ZONE_LIST"]`  
            - Get list of terminal units served by the hvac system: `terminal_list_hvac_sys_x = dict_of_zones_and_terminal_units_served_by_hvac_sys_x[hvac.id]["Terminal_Unit_List"]`  
            - For each terminal unit served by the HVAC system: `for terminal in terminal_list_hvac_sys_x:`  
                - Check if the terminal unit is associated with this zone, if so then add the fan power associated with the terminal unit to the zone total supply fan power: `if terminal in zone.terminals: `  
                    - Get the terminal unit fan power: `terminal_fan_power = get_fan_object_electric_power(RMD,terminal.fan)`  
                    - Add to the total terminal kW for this zone: `zone_total_terminal_fan_power = zone_total_terminal_fan_power + terminal_fan_power`
                    - Add to the zone total supply fan power since it is a supply fan defined at the terminal: `zone_total_supply_fan_power = zone_total_supply_fan_power + terminal_fan_power`  

  - Add the zone as a key and the supply, return, exhaust, relief, terminal fan powers as a list of values to a dictionary: `zone_supply_return_exhaust_relief_terminal_fan_power_dict[zone.id] = [zone_total_supply_fan_power,zone_total_return_fan_power,zone_total_exhaust_fan_power,zone_total_relief_fan_power,zone_total_terminal_fan_power]`

**Returns** `get_zone_supply_return_exhaust_relief_terminal_fan_power_dict`  

**Questions:**  None  

**[Back](../_toc.md)**
