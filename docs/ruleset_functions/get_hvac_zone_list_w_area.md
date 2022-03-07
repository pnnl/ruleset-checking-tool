
## get_hvac_zone_list_w_area

Description: Get the list of zones and their total floor area served by each HVAC system in a RMR.

Inputs:  
- **RMR**: The RMR that needs to get the list of zones served by each HVAC system.

Returns: 
- **hvac_zone_list_w_area_dictionary**: A dictionary that saves the list of zones and the total floor area served by each HVAC system, i.e. {hvac_system_1.id: {"ZONE_LIST": [zone_1.id, zone_2.id, zone_3.id], "TOTAL_AREA": 10000}, hvac_system_2.id: {"ZONE_LIST": [zone_10.id], "TOTAL_AREA": 500}}

Logic:  

- For each zone in RMR: `for zone in RMR...zones:`

  - Check if zone is connected to any terminal: `if zone.terminals:`

    - Get zone total floor area: `zone_area = SUM(space.floor_area for space in zone.spaces)`

    - For each terminal serving zone: `for terminal in zone.terminals:`

      - Get HVAC system connected to terminal: `hvac_sys_id = terminal.served_by_heating_ventilation_air_conditioning_systems` (Note XC, will there be more than one HVAC system connecting to a terminal?)

        - Check if zone is not already saved in HVAC system dictionary: `if NOT zone.id in hvac_zone_list_w_area_dict[hvac_sys_id]["ZONE_LIST"]:`

          - Add zone id and total floor area to HVAC system dictionary: `hvac_zone_list_w_area_dict[hvac_sys_id]["ZONE_LIST"].append(zone.id), hvac_zone_list_w_area_dict[hvac_sys_id]["TOTAL_AREA"] += zone_area`

**Returns** `return hvac_zone_list_w_area_dict`  

**Notes:**

1. If a zone is served by multiple terminals connected to different hvac system, the area and zone are reported under all systems.
