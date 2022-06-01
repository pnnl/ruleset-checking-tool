
## check_purchased_chw_hhw

Description: Check if RMR is modeled with purchased chilled water as space cooling source or purchased hot water/steam as space heating source. If any system in RMR uses purchased chilled water, function shall return True for purchased chilled water as space cooling source. Similarly, if any system in RMR uses purchased hot water or steam, function shall return True for purchased hot water/steam as space heating source.

Inputs:  
- **RMR**: The RMR that needs to be checked.

Returns: 
- **purchased_chw_hhw_status_dictionary**: A dictionary that saves whether RMR is modeled with purchased chilled water as space cooling source or purchased hot water/steam as space heating source, i.e. {"PURCHASED_COOLING": TRUE, "PURCHASED_HEATING": FALSE}.

Function Call:
- GET_COMPONENT_BY_ID()

Logic:  

- Check if RMR is not modeled with external fluid source: `if NOT RMR.ASHRAE229.external_fluid_source:`

  - Set purchased cooling and purchased heating flag as False: `purchased_chw_hhw_status_dict["PURCHASED_COOLING"] = FALSE, purchased_chw_hhw_status_dict["PURCHASED_HEATING"] = FALSE`

- Else, for each external fluid source in RMR: `for external_fluid_source in RMR.ASHRAE229.external_fluid_source:`

  - Check if external fluid source is cooling type: `if external_fluid_source.type == "COOLING"`

    - Get fluid loop served by external fluid source: `cooling_loop = GET_COMPONENT_BY_ID(external_fluid_source.loop)`

      - Save fluid loop and its child loops in purchased cooling loop array: `purchased_chw_loop_array.append(cooling_loop.id), purchased_chw_loop_array.append(loop.id for loop in cooling_loop.child_loops)`

    - For each building segment in RMR (logic loop #1): `for building_segment in RMR...building_segments:`

      - For each HVAC system in building segment: `for hvac_sys in building_segment.heating_ventilation_air_conditioning_systems:`

        - For each cooling system in HVAC system: `for cooling_system in hvac_sys.cooling_system:`

          - Check if cooling system is connected to any loop in purchased cooling loop array: `if cooling_system.chilled_water_loop in purchased_chw_loop_array`

            - Set purchased cooling flag as True and break logic loop #1: `purchased_chw_hhw_status_dict["PURCHASED_COOLING"] = TRUE, BREAK` (Note XC, under the assumption that there is no orphan hvac system not serving any zones.)

  - Else, external fluid source is heating type: `else:` (Note XC, under the assumption that the type field input is correct, i.e. only three inputs are valid, cooling, hot water or steam)

    - Get fluid loop served by external fluid source: `heating_loop = GET_COMPONENT_BY_ID(external_fluid_source.loop)`

      - Save fluid loop and its child loops in purchased heating loop array: `purchased_hhw_loop_array.append(heating_loop.id), purchased_hhw_loop_array.append(loop.id for loop in heating_loop.child_loops)`

    - For each building segment in RMR (logic loop #2): `for building_segment in RMR...building_segments:`

      - For each HVAC system in building segment: `for hvac_sys in building_segment.heating_ventilation_air_conditioning_systems:`

        - For each heating system in HVAC system: `for heating_system in hvac_sys.heating_system:`

          - Check if heating system is connected to any loop in purchased heating loop array: `if heating_system.hot_water_loop in purchased_hhw_loop_array`

            - Set purchased heating flag as True and break logic loop #2: `purchased_chw_hhw_status_dict["PURCHASED_HEATING"] = TRUE, BREAK`

        - For each preheat system in HVAC system: `for preheat_system in hvac_sys.preheat_system:`

          - Check if heating system is connected to any loop in purchased heating loop array: `if preheat_system.hot_water_loop in purchased_hhw_loop_array`

            - Set purchased heating flag as True and break logic loop #2: `purchased_chw_hhw_status_dict["PURCHASED_HEATING"] = TRUE, BREAK`

      - For each zone in building segment: `for zone in building_segment.zones:`

        - For each terminal in zone: `for terminal in zone.terminals:`

          - Check if zonal heating coil is connected to any loop in purchased heating loop array: `if terminal.heating_from_loop in purchased_hhw_loop_array`

            - Set purchased heating flag as True and break logic loop #2: `purchased_chw_hhw_status_dict["PURCHASED_HEATING"] = TRUE, BREAK`

          - Check if zonal cooling coil is connected to any loop in purchased cooling loop array: `if terminal.cooling_from_loop in purchased_chw_loop_array`

            - Set purchased cooling flag as True and break logic loop #2: `purchased_chw_hhw_status_dict["PURCHASED_COOLING"] = TRUE, BREAK`

**Returns** `return purchased_chw_hhw_status_dict`  

**Notes:**

1. For purchased heating, another option is to check if SHW uses purchased heating. If not and RMR has external fluid source, then assume purchased heating is used for space heating.

2. Pending question on baseboard, radiant system, whether these are terminal or an HVAC system.
