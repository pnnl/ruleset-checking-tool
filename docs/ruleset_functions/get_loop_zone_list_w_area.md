
## get_loop_zone_list_w_area

Description: Get the list of zones and their total floor area served by each CHW or HHW loop in a RMR.

Inputs:  
- **RMR**: The RMR that needs to get the list of zones with their total floor area served by each CHW or HHW loop.

Returns: 
- **loop_zone_list_w_area_dictionary**: A dictionary that saves the list of zones and the total floor area served by each CHW or HHW loop, i.e. {loop_1.id: {"ZONE_LIST": [zone_1.id, zone_2.id, zone_3.id], "TOTAL_AREA": 10000}, loop_2.id: {"ZONE_LIST": [zone_10.id], "TOTAL_AREA": 500}}

Logic:  

- For each zone in RMR: `for zone in RMR...zones:`

  - Check if zone is connected to any terminal: `if zone.terminals:`

    - Get zone total floor area: `zone_area = SUM(space.floor_area for space in zone.spaces)`

    - For each terminal serving zone: `for terminal in zone.terminals:`

      - Check if terminal is connected to heating hot water loop: `if terminal.reheat_from_loop:`

        - Check if zone is not already saved in loop dictionary: `if NOT zone.id in loop_dict[terminal.reheat_from_loop]["ZONE_LIST"]:`

          - Save zone id and total floor area to loop dictionary: `loop_dict[terminal.reheat_from_loop]["ZONE_LIST"].append(zone.id), loop_dict[terminal.reheat_from_loop]["TOTAL_AREA"] += zone_area`

      - Get HVAC system connected to terminal: `hvac_sys = terminal.served_by_heating_ventilation_air_conditioning_systems`

        - For each heating system in HVAC system: `for heating_system in hvac_sys.heating_system:`

          - Check if heating system is connected to any fluid loop, get fluid loop for heating: `if heating_system.hot_water_loop: heating_loop_id = heating_system.hot_water_loop`

            - Check if zone is not already saved in loop dictionary: `if NOT zone.id in loop_dict[heating_loop_id]["ZONE_LIST"]:`

              - Add zone id and total floor area to loop dictionary: `loop_dict[heating_loop_id]["ZONE_LIST"].append(zone.id), loop_dict[heating_loop_id]["TOTAL_AREA"] += zone_area`

        - For each cooling system in HVAC system: `for cooling_system in hvac_sys.cooling_system:`

          - Check if cooling system is connected to any fluid loop, get fluid loop for cooling: `if cooling_system.chilled_water_loop: cooling_loop_id = cooling_system.chilled_water_loop`

            - Check if zone is not already saved in loop dictionary: `if NOT zone.id in loop_dict[cooling_loop_id]["ZONE_LIST"]:`

              - Add zone id and total floor area to loop dictionary: `loop_dict[cooling_loop_id]["ZONE_LIST"].append(zone.id), loop_dict[cooling_loop_id]["TOTAL_AREA"] += zone_area`

**Returns** `return loop_zone_list_w_area_dict`  

**Notes:**

1. Assuming baseboard and radiant systems are HVAC system and also have terminals.
2. If a zone is served by multiple hvac/terminal connected to different loops, the area and zone are reported under all loops.
