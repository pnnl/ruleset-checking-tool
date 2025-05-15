# does_zone_meet_G3_1_1d  

**Schema Version:** 0.0.28

**Description:** determines whether a given zone meets the G3_1_1d exception "For laboratory spaces in a building having a total laboratory exhaust rate greater than 15,000 cfm, use a single system of type 5 or 7 serving only those spaces."

This function gets the system-wide exhaust airflow rate following the same logic as the function **get_zone_supply_return_exhaust_relief_terminal_fan_power_dict**

**Inputs:** 
- **P_RMI**
- **zone**
- **zones_and_systems** - this is a dict of the existing expected system types from the function `get_zone_target_baseline_system`

**Returns:**  
- **result**: boolean true if meet, false otherwise.
 
**Function Call:**
- **get_baseline_system_types**
- **get_list_hvac_systems_associated_with_zone**
- **get_dict_of_zones_and_terminal_units_served_by_hvac_sys**   
- **get_list_hvac_systems_associated_with_zone**
- **get_building_total_lab_exhaust_from_zone_exhaust_fans**
- **get_building_lab_zones**

## Logic:
- set the result variable to "No" - only a positive test can give it a different value: `result = NO`
- use the function get_building_lab_zones to get a list of laboratory zones in the P_RMI: `laboratory_zones_list = get_building_lab_zones(P_RMI)`
- check if the given zone is in the laboratory_zones_list, continue checking logic: `if zone.id in? laboratory_zones_list:`
    - now check whether building lab exhaust airflow is greater than 15,000 cfm - create a variable for the building total lab exhaust and set it equal to the result of the function get_building_total_lab_exhaust_from_zone_exhaust_fans(): `building_total_lab_exhaust = get_building_total_lab_exhaust_from_zone_exhaust_fans(P_RMI)`
    - check if the building_total_lab_exhaust is greater than 15,000cfm.  If it is, then the zone meets G3.1.1d.  If not, check the HVAC systems serving lab zones and add the exhaust to the building_total_lab_exhaust: `if building_total_lab_exhaust > 15,000:`
     - set result to YES: `result = YES`
    - otherwise, find the system exhaust rate allocated to labs: `else:`
     - Now find the laboratory exhaust for each zone in the laboratory_zones list.  Loop through each zone: `for z_id in laboratory_zones_list:`
        - Get a list of HVAC systems serving the zone: `hvac_sys_list_serving_zone_x =  get_list_hvac_systems_associated_with_zone(RMI,z_id)`  
        - For each hvac system serving the zone: `for hvac in hvac_sys_list_serving_zone_x:`  
            - Check if there is a fan system associated with the hvac system (if not, then there is no central HVAC system exhaust fan (terminal units don't have exhaust fans)): `if hvac.fan_system != Null:`  
                - Get list of zones served by the hvac system: `zone_list_hvac_sys_x = dict_of_zones_and_terminal_units_served_by_hvac_sys_x[hvac.id]["ZONE_LIST"]`  
                - create a variable to hold the total exhaust airflow rate of the HVAC system: `hvac_system_total_exhaust_airflow = 0`
                - Look at each fan in the fan_system.exhaust_fans: `for exhaust_fan in fan_system.exhaust_fans:`
                    - add the exhaust fan airflow to the hvac exhaust airflow total: `hvac_system_total_exhaust_airflow += exhaust_fan.design_airflow`
                - Check if the hvac system serves more than one zone, if it does then carry on, if not then go to Else: `if len(zone_list_hvac_sys_x) >1:`  
                    - Get list of terminal units served by the hvac system: `terminal_list_hvac_sys_x = dict_of_zones_and_terminal_units_served_by_hvac_sys_x[hvac.id]["Terminal_Unit_List"]`  
                    - create a variable for the total terminal air flow for the hvac system - this total terminal airflow is used to divide exhaust proportionally across zones: `total_terminal_air_flow = 0`
                    - create a variable to hold the terminal airflow for this zone: `zone_primary_air_flow = 0`
                    - For each terminal unit served by the HVAC system: `for terminal in terminal_list_hvac_sys_x:`  
                        - Get the primary air flow: `primary_air_flow_terminal = terminal.primary_airflow`  
                        - Add to the total cfm across all terminals served by the HVAC system: `total_terminal_air_flow = total_terminal_air_flow + primary_air_flow_terminal`  
                        - Check if the terminal unit is associated with this zone: `if terminal in z.terminals:`   
                            - Add to the primary flow for the zone for this hvac system:  `zone_primary_air_flow = zone_primary_air_flow + primary_air_flow_terminal`  
                    - Get the HVAC system's FanSystem: `fan_system = hvac.fan_system`
                    - Apportion the exhaust airflow to the zone based on the terminal unit primary flow for the zone if hvac_system_total_exhaust_airflow > 0 and zone_primary_air_flow > 0: `if( zone_primary_air_flow > 0 && hvac_system_total_exhaust_airflow > 0 ): zone_total_exhaust += hvac_system_total_exhaust_airflow * (zone_primary_air_flow/total_terminal_air_flow)`
                - Else, the HVAC system serves a single zone: `Else:`  
                    - Add the hvac system exhaust flow to zone_total_exhaust: `zone_total_exhaust += hvac_system_total_exhaust_airflow`  
        - add the zone_total_exhaust to building_total_lab_exhaust: `building_total_lab_exhaust = building_total_lab_exhaust + zone_total_exhaust`
      - now check whether the building wide total lab exhaust is greater than 15,000 cfm: `if building_total_lab_exhaust > 15000:`
        - set the result to YES: `result = YES`



**Returns** `result`

**Notes**
1.  This function determines whether the zone is a lab zone, and whether the building has total lab exhaust greater than 15,000 cfm.  We can determine with precision when there is less than 15,000cfm of lab exhaust, but not necessarily all air that is exhausted from a lab zone is classified as lab exhaust.  Therefore, when we do rule evaluation, we can only give a 100% positive identification of a lab zone when the lab zones have a total of more than 15,000 cfm of zone exhaust.
2.  when a lab zone is served by HVAC system with exhaust fans serving both lab and non-lab zones, we assume that exhaust flow rate is allocated to the lab zones in proportion to the primary air flow delivered to these zones comared to the total primary air flow delivered to all zones by this system.


**[Back](../_toc.md)**

