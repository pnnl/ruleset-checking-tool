
## get_hw_loop_zone_list_w_area

Description: Get the list of zones and their total floor area served by each HHW loop in a baseline ruleset model instance.  

Inputs:  
- **B-RMR**: The baseline ruleset model instance that needs to get the list of zones with their total floor area served by each HHW loop.

Returns: 
- **hw_loop_zone_list_w_area_dictionary**: A dictionary that saves the list of zones and the total floor area served by each HHW loop, i.e. {loop_1.id: {"ZONE_LIST": [zone_1.id, zone_2.id, zone_3.id], "TOTAL_AREA": 10000}, loop_2.id: {"ZONE_LIST": [zone_10.id], "TOTAL_AREA": 500}}

Function Calls:
- GET_COMPONENT_BY_ID()

Logic:  

- For each zone in baseline ruleset model instance: `for zone in B-RMR...zones:`

  - Check if zone is connected to any terminal: `if zone.terminals:`

    - Get zone total floor area: `zone_area = SUM(space.floor_area for space in zone.spaces)`

    - For each terminal serving zone: `for terminal in zone.terminals:`

      - Get HVAC system serving terminal: `hvac = GET_COMPONENT_BY_ID(terminal.served_by_heating_ventilation_air_conditioning_system)`

        - Check if HVAC system has preheat coil: `if hvac.preheat_system != NULL`

          - Get heating hot water loop serving preheat coil: `hhw_loop_id = GET_COMPONENT_BY_ID(hvac.preheat_system).hot_water_loop`

          - Save zone id and total floor area to loop dictionary: `hw_loop_zone_list_w_area_dict[hhw_loop_id]["ZONE_LIST"].append(zone.id), hw_loop_zone_list_w_area_dict[hhw_loop_id]["TOTAL_AREA"] += zone_area`

**Returns** `return hw_loop_zone_list_w_area_dict`  

**Notes:**

1. Prerequisite: baseline systems are model correctly with preheat coils.
