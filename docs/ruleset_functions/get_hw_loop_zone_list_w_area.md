
## get_hw_loop_zone_list_w_area

**Schema Version:** 0.0.23

Description: Get the list of zones and their total floor area served by each HHW loop in a baseline ruleset model instance.  

Inputs:  
- **B-RMD**: The baseline ruleset model instance that needs to get the list of zones with their total floor area served by each HHW loop.

Returns: 
- **hw_loop_zone_list_w_area_dictionary**: A dictionary that saves the list of zones and the total floor area served by each HHW loop, i.e. {loop_1.id: {"ZONE_LIST": [zone_1.id, zone_2.id, zone_3.id], "TOTAL_AREA": 10000}, loop_2.id: {"ZONE_LIST": [zone_10.id], "TOTAL_AREA": 500}}

Functions:  
1. is_hvac_sys_preheating_type_fluid_loop() 
2. is_hvac_sys_heating_type_fluid_loop ()


**Logic:**   

- For each zone in baseline ruleset model instance: `for zone in B-RMD...Zone:`
  - Reset zone hot water loop found boolean variable: `zone_HHW_loop_found = FALSE`  
  - Check if zone is connected to any terminal: `if zone.terminals != Null or len(zone.terminals) != 0:`
    - Get zone total floor area: `zone_area = SUM(space.floor_area for space in zone.spaces)`
    - For each terminal serving the zone: `for terminal in zone.terminals:`
      - Check if the heat source is hot water: `if terminal.heating_source == "HOT_WATER":`  
        - Get the heating from loop ID: `hhw_loop_id = terminal.heating_from_loop`
          - Save zone id and total floor area to loop dictionary: `hw_loop_zone_list_w_area_dict[hhw_loop_id]["ZONE_LIST"].append(zone.id), hw_loop_zone_list_w_area_dict[hhw_loop_id]["TOTAL_AREA"] += zone_area`
          - Set zone_HHW_loop_found = TRUE: `zone_HHW_loop_found = TRUE`  
      - Check if the hot water loop serving the zone has been found, if it has not then carry on: `if zone_HHW_loop_found == FALSE:`
        - Get HVAC system serving terminal: `hvacID = terminal.served_by_heating_ventilating_air_conditioning_system`
        - Create HVAC system object from the ID (however the RCT team decides to do this): `hvac = HeatingVentilationAirConditioningSystem.hvacID`
          - Check that the preheat coil is a fluid_loop: `if is_hvac_sys_preheating_type_fluid_loop(B-RMI, hvac.id) == TRUE:`   
            - Get heating hot water loop serving preheat coil: `hhw_loop_id = hvac.preheat_system.hot_water_loop`
              - Save zone id and total floor area to loop dictionary: `hw_loop_zone_list_w_area_dict[hhw_loop_id]["ZONE_LIST"].append(zone.id), hw_loop_zone_list_w_area_dict[hhw_loop_id]["TOTAL_AREA"] += zone_area`
              - Set zone_HHW_loop_found = TRUE: `zone_HHW_loop_found = TRUE`  
            - Check if the hot water loop serving the zone has been found, if it has not then carry on: `if zone_HHW_loop_found == FALSE:`
            - Check that the heating coil is a fluid_loop: `if is_hvac_sys_heating_type_fluid_loop(B-RMI, hvac.id) == TRUE:`   
               - Get heating hot water loop serving the heating coil: `hhw_loop_id = hvac.heating_system[0].hot_water_loop`
                 - Save zone id and total floor area to loop dictionary: `hw_loop_zone_list_w_area_dict[hhw_loop_id]["ZONE_LIST"].append(zone.id), hw_loop_zone_list_w_area_dict[hhw_loop_id]["TOTAL_AREA"] += zone_area`

**Returns** `return hw_loop_zone_list_w_area_dict`  

**Notes:**

1. Prerequisite: baseline systems are model correctly with preheat coils - Xing.
2. Prerequisute is that baseline systems are modeled correctly with the same loops serving all relevant coils for each zone. 
