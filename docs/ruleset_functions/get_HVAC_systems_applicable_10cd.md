## get_HVAC_systems_applicable_10cd

**Description:** Get the list of HeatingVentilationAirAconditioningSystem in which Appendix G Table G3.1 #10 c and d are applicable.

**Inputs:**
- **U-RMR**: The U-RMR to determine if an HVAC system has been designed or modeled as existing for each zone.
- **P-RMR**: To determine if the same zone has been analyzed with a HVAC system in P-RMR.

**Returns:**
- **applicable_hvac_systems_10cd_list_p**: A list that saves all the HVAC systems in which Appendix G Table G3.1 #10 c and d are applicable.
 
**Function Call:** 

1. match_data_element()

**Logic:**
- # Determine if a HVAC system has been designed or modeled as existing in U-RMR for each zone**
- For each zone in U_RMR: `for zone_u in U_RMR...zones:`
    - Reset heating system exists boolean variable equal to false each time it loops to a different zone: `heating_system_exists_is-designed_u = FALSE`
    - Reset cooling system exists boolean variable equal to false each time it loops to a different zone: `cooling_system_exists_is-designed_u = FALSE`
    - Reset heating system exists boolean variable equal to false each time it loops to a different zone: `heating_system_modeled_p = FALSE`
    - Reset cooling system exists boolean variable equal to false each time it loops to a different zone: `cooling_system_modeled_p = FALSE`
    - Check if there are terminal units associated with the zone, if not skip to proposed: `if len(zone_u.terminals) != 0:`
        - For each terminal unit associated with each zone: `for terminal_u in zone_u:`
            - if reheat_source is not null then set heating exists/is designed boolean variable equal to true: `if terminal_u.reheat_source != "None":`
                - Set heating system exists/is designed boolean variable equal to true: `heating_system_exists_is-designed_u = TRUE`
            - if terminal heat_capacity is not zero then set heating exists/is designed boolean variable equal to true: `if terminal_u.heat_capacity != 0:`
                - Set heating system exists/is designed boolean variable equal to true: `heating_system_exists_is-designed_u = TRUE`    
            - Get the served_by_heating_ventilation_air_conditioning_systems for each terminal: `heating_ventilation_air_conditioning_systems_u = terminal_u.served_by_heating_ventilation_air_conditioning_systems`
            - Add to list of heating_ventilation_air_conditioning_systems_list_u as the code loops through the terminal units: `heating_ventilation_air_conditioning_systems_list_u = heating_ventilation_air_conditioning_systems_list_u.append(heating_ventilation_air_conditioning_systems_u)`                    
        - After looping through all terminal units convert the list of heating_ventilation_air_conditioning_systems_list_u associated with the zone to a set and the back to a list to eliminate duplicates: `heating_ventilation_air_conditioning_systems_list_u = list(set(heating_ventilation_air_conditioning_systems_list_u))`
        - For each hvac_u in heating_ventilation_air_conditioning_systems_list_u: `for hvac_u in heating_ventilation_air_conditioning_systems_list_u:`
            - For each heating system in hvac_u: `for heating_system_u in hvac_u.heating_system:`
                - if heating_system_type is not "None": `if heating_system_u.heating_system_type != "None":`
                    - Set heating system exists/is designed boolean variable equal to true: `heating_system_exists_is-designed_u = TRUE`
            - For each cooling system in hvac_u: `for cooling_system_u in hvac_u.cooling_system:`
                - if cooling_system_type is not "None": `if cooling_system_u.cooling_system_type != "None":`
                    - Set cooling system exists/is designed boolean variable equal to true: `cooling_system_exists_is-designed_u = TRUE`
            - For each preheat system in hvac_u: `for preheat_system_u in hvac_u.preheat_system:`
                - if preheat_system_type is not "None": `if preheat_system_u.heating_system_type != "None":`
                    - Set heating system exists/is designed boolean variable equal to true: `heating_system_exists_is-designed_u = TRUE`

    - # Determine if the same zone has been analyzed with a HVAC system in P-RMR
    - Get the analogous Zone ID in the P_RMR: `zone_p = match_data_element(P_RMR,Zones,zone_u.id)` 
        - Check if there are terminal units associated with the zone, if not skip to if statements based on if there are heating and cooling systems: `if len(zone_p.terminals) != 0:`
            - For each terminal unit associated with each zone: `for terminal_p in zone_p:`
                - if reheat_source is not null then set heating modeled boolean variable equal to true: `if terminal_p.reheat_source != "None":`
                    - Set heating system modeled boolean variable equal to true: `heating_system_modeled_p = TRUE`
                - if terminal heat_capacity is not zero then set heating modeled boolean variable equal to true: `if terminal_p.heat_capacity != 0:`
                    - Set heating system modeled boolean variable equal to true: `heating_system_modeled_p = TRUE`    
                - Get the served_by_heating_ventilation_air_conditioning_systems for each terminal: `heating_ventilation_air_conditioning_systems_p = terminal_p.served_by_heating_ventilation_air_conditioning_systems`
                - Add to the list of heating_ventilation_air_conditioning_systems_p as the code loops through the terminal units: `heating_ventilation_air_conditioning_systems_list_p = heating_ventilation_air_conditioning_systems_list_p.append(heating_ventilation_air_conditioning_systems_p)`                    
            - After looping through all terminal units convert the list of heating_ventilation_air_conditioning_systems_list_p associated with the zone to a set and the back to a list to eliminate duplicates: `heating_ventilation_air_conditioning_systems_list_p = list(set(heating_ventilation_air_conditioning_systems_list_p))`
                - For each hvac_p in heating_ventilation_air_conditioning_systems_list_p: `for hvac_p in heating_ventilation_air_conditioning_systems_list_p:`
                    - For each heating system in hvac_p: `for heating_system_p in hvac_p.heating_system:`
                        - if heating_system_type is not "None": `if heating_system_p.heating_system_type != "None":`
                            - Set heating system modeled boolean variable equal to true: `heating_system_modeled_p = TRUE`
                    - For each cooling system in hvac_p: `for cooling_system_p in hvac_p.cooling_system:`
                        - if cooling_system_type is not "None": `if cooling_system_p.cooling_system_type != "None":`
                            - Set cooling system modeled boolean variable equal to true: `cooling_system_modeled_p = TRUE`
                    - For each preheat system in hvac_p: `for preheat_system_p in hvac_p.preheat_system:`
                        - if preheat_system_type is not "None": `if preheat_system_p.heating_system_type != "None":`
                            - Set heating system modeled boolean variable equal to true: `heating_system_modeled_p = TRUE`  
        
    
    - if zone has heating and cooling in the U_RMR: `if heating_system_exists_is-designed_u == TRUE AND cooling_system_exists_is-designed_u == TRUE:`
        - Set applicability flag: `function_applicability_check = FALSE`
    - else if the zone has heating but no cooling in the U_RMR and P_RMR: `else if heating_system_exists_is-designed_u == TRUE AND cooling_system_exists_is-designed_u == FALSE AND heating_system_modeled_p == TRUE AND cooling_system_modeled_p == FALSE:`
        - Set applicability flag: `function_applicability_check = FALSE`                
    - else, set applicability flag to true and add the proposed HVAC system(s) to the list: `else:`
        - Set applicability flag:`function_applicability_check == TRUE`
        - For each hvac_u in heating_ventilation_air_conditioning_systems_list_u: `for hvac_u in heating_ventilation_air_conditioning_systems_list_u:`
            - Get the analogous HVAC ID in the P_RMR: `hvac_p = match_data_element(P_RMR,heating_ventilation_air_conditioning_systems,hvac_u.id)`
            - Add to list of HVAC system that are applicable to this check: `applicable_hvac_systems_10cd_list_p = applicable_hvac_systems_10cd_list_p.append(hvac_p)`

 - Convert the list of applicable_hvac_systems_list_p to a set and the back to a list to eliminate duplicates after looping through all zones:
 `applicable_hvac_systems_10cd_list_p = list(set(applicable_hvac_systems_10cd_list_p))` 

 **Returns** `return applicable_hvac_systems_10cd_list_p`  

                                 
**[Back](../_toc.md)**