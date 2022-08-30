
## get_hw_loop_zone_list_w_area

Description: Get the list of zones and their total floor area served by each HHW loop in a baseline ruleset model instance.  

Inputs:  
- **B-RMR**: The baseline ruleset model instance that needs to get the list of zones with their total floor area served by each HHW loop.

Returns: 
- **hw_loop_zone_list_w_area_dictionary**: A dictionary that saves the list of zones and the total floor area served by each HHW loop, i.e. {loop_1.id: {"ZONE_LIST": [zone_1.id, zone_2.id, zone_3.id], "TOTAL_AREA": 10000}, loop_2.id: {"ZONE_LIST": [zone_10.id], "TOTAL_AREA": 500}}

Functions:  
1. is_hvac_sys_preheating_type_fluid_loop() 


Logic:  

- For each zone in baseline ruleset model instance: `for zone in B-RMR...Zone:`
  - Check if zone is connected to any terminal: `if len(zone.terminals) != Null or len(zone.terminals) != 0:`
    - Get zone total floor area: `zone_area = SUM(space.floor_area for space in zone.spaces)`
    - For each terminal serving zone: `for terminal in zone.terminals:`
      - Get HVAC system serving terminal: `hvacID = terminal.served_by_heating_ventilation_air_conditioning_system`
      - Create HVAC system object from the ID (however the RCT team decides to do this): `hvac = HeatingVentilationAirConditioningSystem.hvacID`
        - Check if HVAC system has preheat coil: `if hvac.preheat_system != NULL AND hvac.preheat_system[0].heating_system_type != "None":`
          - Check that the preheat coil is a fluid_loop: `if is_hvac_sys_preheating_type_fluid_loop(B-RMR, hvac.id) == TRUE:`   
            - Get heating hot water loop serving preheat coil: `hhw_loop_id = hvac.preheat_system[0].hot_water_loop`
            - Check if zone is not already saved in heating hot water loop dictionary: `if NOT zone.id in hvac_zone_list_w_area_dict[hhw_loop_id]["ZONE_LIST"]:`  
              - Save zone id and total floor area to loop dictionary: `hw_loop_zone_list_w_area_dict[hhw_loop_id]["ZONE_LIST"].append(zone.id), hw_loop_zone_list_w_area_dict[hhw_loop_id]["TOTAL_AREA"] += zone_area`

**Returns** `return hw_loop_zone_list_w_area_dict`  

**Notes:**

1. Prerequisite: baseline systems are model correctly with preheat coils - Xing.
2. Not sure where this function is to be used so I am not clear why it only checks the preheat coil. 
For example, 
Systems 1, 1a, 1b, 3b, 3c, 11.2, 11.2a, 11b, 11c, and 12, 12a, 12b, 12c will have HW coils as heating coils. 
Systems 5, 5a, 5b, 6b, 7, 7a, 7b, 7c, 8b, 8c, 9b and 1c will have HW coils at the terminal units.
