## get_zones_hvac_system_humid_p

**Description:** Get the list of P_RMR zones and corresponding HVAC system IDs where humidification is applicable.

**Inputs:**
- **P-RMR**: To determine if any zones and corresponding HVAC systems have humidification in the proposed.

**Returns:**
- **applicable_zones_hvac_sys_humid_dict_p**: A dictionary that saves all zones IDs as keys and a list of associated HVAC sys IDs as values that have humidification on the P_RMR.
 
**Function Call:** None


**Logic:**
- For each zone in P_RMR: `zone_p in P_RMR..Zone:`
- Reset applicability flag: `rule_applicability_check = FALSE`  
    - For each terminal unit associated with each zone: `terminal_p in zone_p:`
        - Get the served_by_heating_ventilation_air_conditioning_systems for each terminal: `heating_ventilation_air_conditioning_systems_p = terminal_p.served_by_heating_ventilation_air_conditioning_systems`
            - Create list of heating_ventilation_air_conditioning_systems_p add to as the code loops through the terminal units: `heating_ventilation_air_conditioning_systems_list_p = heating_ventilation_air_conditioning_systems_list_p.append(heating_ventilation_air_conditioning_systems_p)`                    
    - Convert the list of heating_ventilation_air_conditioning_systems_list_p associated with the zone to a set and the back to a list to eliminate duplicates: `heating_ventilation_air_conditioning_systems_list_p = list(set(heating_ventilation_air_conditioning_systems_list_p))`
     - For each hvac_p in heating_ventilation_air_conditioning_systems_list_p: `for hvac_p in heating_ventilation_air_conditioning_systems_list_p:`    
        - Reset applicability flag_hvac: `rule_applicability_check_hvac = FALSE`  
        - For each heating_system in hvac_p.heating_system: `for heating_system_p in hvac_p.heating_system:`
            - Get humidification type: `humidification_type_p = heating_systems_p.humidification_type`
            - Check if humidification type is adiabatic or other (if null or NONE then no humidification): `if humidification_type_p in ["ADIABATIC", "OTHER"]:`
                - Set zone applicability flag: `rule_applicability_check = TRUE`
                - Set hvac applicablity flag: `rule_applicability_check_hvac = TRUE` 
        - For each preheat_system in hvac_p.preheat_system: `for preheat_systems_p in hvac_p.preheat_system:`
            - Get humidification type: `humidification_type_p = preheat_systems_p.humidification_type`
            - Check if humidification type is adiabatic or other (if null or NONE then no humidification): `if humidification_type_p in ["ADIABATIC", "OTHER"]:`
                - Set zone applicability flag: `rule_applicability_check = TRUE`
                - Set hvac applicablity flag: `rule_applicability_check_hvac = TRUE`
        - Check if hvac applicability flag is true: `if rule_applicability_check_hvac == TRUE:`
            - Add to list of applicable hvac_systems for the zone: `applicable_hvac_sys_list_p = applicable_hvac_sys_list_p.append(hvac_p)`
    - Check if the applicability flag equals TRUE for the zone, if true then add to dict with zone as key and list of applicable hvac systems as values: `if rule_applicability_check == TRUE:`
        - Add to dict with zone as key and list of applicable hvac systems as values, start with empty list: `applicable_zones_hvac_sys_humid_dict_p[zone_p.id] = list()`
        - Add to dict with zone as key and list of applicable hvac systems as values: `applicable_zones_hvac_sys_humid_dict_p[zone_b.id].extend(applicable_hvac_sys_list_p)`

**Returns** `return applicable_zones_hvac_sys_humid_dict_p`   

**[Back](../_toc.md)**