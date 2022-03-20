
## get_primary_secondary_loops

Description: Get the list of primary and secondary loops for HHW or CHW for a RMR.

Inputs:  
- **RMR**: The RMR that needs to get the list of primary and secondary loops.
- **loop_type**: "COOLING" (or "HEATING", if needed in future)

Returns: 
- **primary_secondary_loop_dictionary**: A dictionary that saves pairs of primary and secondary loops for the selected loop type, i.e. "HEATING" or "COOLING", e.g. {primary_loop_1.id: [secondary_loop_1.id, secondary_loop2.id], primary_loop_2.id: [secondary_loop3.id]]}. If RMR does not have primary-secondary loop configuration setup, return an empty dictionary.

Logic:  

- For each chiller in RMR, save its cooling loop to CHW chiller loop array to get all loops connected to chiller(s): `for chiller in RMR.RulesetModelInstance.chillers: component_loop_array.append(chiller.cooling_loop)`

- For each building segment in RMR: `for building_segment in RMR...building_segments:`

  - For each HVAC system in building segment: `for hvac in building_segment.heating_ventilation_air_conditioning_systems`

    - Check if HVAC system has chilled water coil: `if hvac.cooling_system.chilled_water_loop:`

      - Save chilled water loop that serves cooling systems to CHW coil loop array (array for all loops connected to cooling coils): `chw_coil_loop_array.append(hvac.cooling_system.chilled_water_loop)`

  - For each zone in building segment: `for zone in building_segment.zones:`

    - For each terminal in zone: `for terminal in zone.terminals:`

      - Check if cooling source is chilled water: `if terminal.cooling_source == "CHILLED_WATER":`

        - Save chilled water that serves terminal to CHW coil loop array (array for all loops connected to cooling coils): `chw_coil_loop_array.append(terminal.cooling_from_loop)`

- For each fluid loop in RMR: `for fluid_loop in RMR.RulesetModelInstance.fluid_loops:`

  - Check if loop type is the same as input loop_type: `if fluid_loop.type == loop_type:`

    - Check if loop is connected to chiller(s): `if fluid_loop.id in component_loop_array:`

      - Check if loop has child loop(s) and loop is not connected to any cooling coils: `if ( fluid_loop.child_loops != NULL ) AND ( NOT fluid_loop.id in chw_coil_loop_array ):`

        - Set pass primary check flag to True: `pass_primary_check_flag = TRUE`

        - Save loop to primary loop array: `primary_loop_array.append(fluid_loop.id)`

        - Save all child loops to child loop array: `child_loop_array.append(child_loop_id for child_loop_id in fluid_loop.child_loops)`

    - Check if loop to connected to cooling coil(s): `if fluid_loop in chw_coil_loop_array:`

      - Check if loop does not have any child loop and is not connected to any chiller(s): `if ( fluid_loop.child_loops == NULL ) AND ( NOT fluid_loop.id in component_loop_array ):`

        - Set pass secondary check flag to True: `pass_secondary_check_flag = TRUE`

        - Save loop to secondary loop array: `secondary_loop_array.append(fluid_loop.id)`

- Check if child loop array and secondary loop array is the same, set pass child loop check flag to True: `if child_loop_array.sort() == secondary_loop_array.sort(): pass_child_loop_check_flag = TRUE`

- If all three flags are true: `if pass_primary_check_flag AND pass_secondary_check_flag AND pass_child_loop_check_flag:`

  - For each primary loop: `for primary_loop in primary_loop_array:`
  
    - Save primary and secondary loop(s) pair to output dictionary: `primary_secondary_loop_dictionary[primary_loop_id].append(secondary_loop_id for secondary_loop_id in primary_loop.child_loops)`

**Returns** `return primary_secondary_loop_dictionary`

**Notes:**

1. Primary secondary configuration is correct if:
1). a cooling loop is either connected to chiller or cooling coil, but not both
2). if a cooling loop is connected to chiller, it shall have child loop(s)
3). if a cooling loop is connected to cooling coil, it shall not have any child loops
4). the collection of child loops of all of 2) shall be the same as all of 3)
