
## check_purchased_chw_hhw_status_dict

Description: Check if RMI is modeled with purchased chilled water as space cooling source or purchased hot water/steam as space heating source. If any system in RMI uses purchased chilled water, function shall return True for purchased chilled water as space cooling source. Similarly, if any system in RMI uses purchased hot water or steam, function shall return True for purchased hot water/steam as space heating source.

Inputs:  
- **RMI**: The RMI that needs to be checked.

Returns:
- **purchased_chw_hhw_status_dictionary**: A dictionary that saves whether RMI is modeled with purchased chilled water as space cooling source or purchased hot water/steam as space heating source, i.e. {"PURCHASED_COOLING": TRUE, "PURCHASED_HEATING": FALSE}.

Function Call:
- GET_COMPONENT_BY_ID()

Logic:  

- Check if RMI is not modeled with external fluid source: `if NOT RMI.ASHRAE229.external_fluid_source:`

  - Set purchased cooling and purchased heating flag as False: `purchased_chw_hhw_status_dict["PURCHASED_COOLING"] = FALSE, purchased_chw_hhw_status_dict["PURCHASED_HEATING"] = FALSE`

- Else, for each external fluid source in RMI: `for external_fluid_source in RMI.ASHRAE229.external_fluid_source:`

  - Check if external fluid source is chilled water type: `if external_fluid_source.type == "CHILLED_WATER"`

    - Get fluid loop served by external fluid source: `cooling_loop = GET_COMPONENT_BY_ID(external_fluid_source.loop)`

      - Save fluid loop and its child loops in purchased cooling loop array: `purchased_chw_loop_array.append(cooling_loop.id), purchased_chw_loop_array.append(loop.id for loop in cooling_loop.child_loops)`

    - For each building segment in RMI (logic loop #1): `for building_segment in RMI...building_segments:`

      - For each HVAC system in building segment: `for hvac_sys in building_segment.heating_ventilating_air_conditioning_systems:`

          - Check if cooling system is connected to any loop in purchased cooling loop array: `if cooling_system.chilled_water_loop.chilled_water_loop in purchased_chw_loop_array`

            - Set purchased cooling flag as True and break logic loop #1: `purchased_chw_hhw_status_dict["PURCHASED_COOLING"] = TRUE, BREAK` (Note XC, under the assumption that there is no orphan hvac system not serving any zones.)
      
      - For each zone in building segment: `for zone in building_segment.zones:`

        - For each terminal in zone: `for terminal in zone.terminals:`

          - Check if zonal cooling coil is connected to any loop in purchased cooling loop array: `if terminal.cooling_from_loop in purchased_chw_loop_array`

            - Set purchased cooling flag as True and break logic loop #2: `purchased_chw_hhw_status_dict["PURCHASED_COOLING"] = TRUE, BREAK`

  - Else, external fluid source is heating type: `else:` (Note XC, under the assumption that the type field input is correct, i.e. only three inputs are valid, cooling, hot water or steam)

    - Get fluid loop served by external fluid source: `heating_loop = GET_COMPONENT_BY_ID(external_fluid_source.loop)`

      - Save fluid loop and its child loops in purchased heating loop array: `purchased_hhw_loop_array.append(heating_loop.id), purchased_hhw_loop_array.append(loop.id for loop in heating_loop.child_loops)`

    - For each building segment in RMI (logic loop #2): `for building_segment in RMI...building_segments:`

      - For each HVAC system in building segment: `for hvac_sys in building_segment.heating_ventilating_air_conditioning_systems:`

          - Check if heating system is connected to any loop in purchased heating loop array: `if hvac_sys.heating_system.hot_water_loop in purchased_hhw_loop_array`

            - Set purchased heating flag as True and break logic loop #2: `purchased_chw_hhw_status_dict["PURCHASED_HEATING"] = TRUE, BREAK`

          - Check if heating system is connected to any loop in purchased heating loop array: `if preheat_system.hot_water_loop in purchased_hhw_loop_array`

            - Set purchased heating flag as True and break logic loop #2: `purchased_chw_hhw_status_dict["PURCHASED_HEATING"] = TRUE, BREAK`

      - For each zone in building segment: `for zone in building_segment.zones:`

        - For each terminal in zone: `for terminal in zone.terminals:`

          - Check if zonal heating coil is connected to any loop in purchased heating loop array: `if terminal.heating_from_loop in purchased_hhw_loop_array`

            - Set purchased heating flag as True and break logic loop #2: `purchased_chw_hhw_status_dict["PURCHASED_HEATING"] = TRUE, BREAK`
**Returns** `return purchased_chw_hhw_status_dict`  

**Notes:**

1. For purchased heating, another option is to check if SHW uses purchased heating. If not and RMI has external fluid source, then assume purchased heating is used for space heating.

2. Pending question on baseboard, radiant system, whether these are terminal or an HVAC system.
