
## get_primary_secondary_loops (TBD, change name to get_baseline_chw_primary_secondary_loops)

Description: Get the list of primary and secondary loops for CHW for a B-RMR.

Inputs:  
- **B-RMR**: B-RMR that needs to get the list of primary and secondary loops.

Returns: 
- **primary_secondary_loop_dictionary**: A dictionary that saves pairs of primary and secondary loops for baseline chilled water system, e.g. {primary_loop_1.id: [secondary_loop_1.id, secondary_loop2.id], primary_loop_2.id: [secondary_loop3.id]]}. If B-RMR does not have primary-secondary loop configuration setup, return an empty dictionary.

Logic:  

- Get B-RMR system types: `baseline_hvac_system_dict = get_baseline_system_types(B-RMR)`

- For each chiller in B-RMR, save its cooling loop to CHW chiller loop array to get all loops connected to chiller(s): `for chiller in B-RMR.RulesetModelInstance.chillers: chiller_loop_array.append(chiller.cooling_loop)`

- For each building segment in B-RMR: `for building_segment in B-RMR...building_segments:`

  - For each HVAC system in building segment: `for hvac in building_segment.heating_ventilating_air_conditioning_systems`

    - Check if HVAC system is baseline system Type-7, 8, 11.1, 11.2, 12, 13, 7b, 8b, 11.1b, 12b: `if any(hvac.id in baseline_hvac_system_dict[sys_type] for sys_type in ["SYS-7", "SYS-8", "SYS-11.1", "SYS-11.2", "SYS-12", "SYS-13", "SYS-7B", "SYS-8B", "SYS-11B", "SYS-12B", "SYS-13B"]):`

      - Save chilled water loop that serves cooling systems to non-process CHW coil loop array (array for all loops connected to cooling coils): `non_process_chw_coil_loop_array.append(hvac.cooling_system.chilled_water_loop)`

- For each fluid loop in B-RMR: `for fluid_loop in B-RMR.RulesetModelInstance.fluid_loops:`

  - Check if loop type is cooling: `if fluid_loop.type == "COOLING":`

    - Check if loop is connected to both chiller(s) and non-process cooling coil(s), break logic and return an empty dictionary (this would be if the system was not modeled as primary-seconday, a fluid_loop will never be connected to a cooling_system.chilled_water_loop): `if ( fluid_loop.id in chiller_loop_array ) AND ( fluid_loop in non_process_chw_coil_loop_array ): BREAK and return primary_secondary_loop_dictionary = {}`

    - Else if loop is connected to chiller(s) only: `else if fluid_loop.id in chiller_loop_array:`

      - Check if all child loops of loop serve baseline system Type-7, 8, 11.1, 11.2, 12, 13, 7b, 8b, 11.1b, 12b only (to exclude CHW loop served by process chiller(s)): `if all(child_loop_id in non_process_chw_coil_loop_array for child_loop_id in fluid_loop.child_loops):`

        - Save loop to primary loop array: `primary_loop_array.append(fluid_loop.id)`  
  
  - For each primary loop: `for primary_loop_id in primary_loop_array:`
  
    - Save primary and secondary loop(s) pair to output dictionary: `primary_secondary_loop_dictionary[primary_loop_id].append(secondary_loop_id for secondary_loop_id in primary_loop.child_loops)`

**Returns** `return primary_secondary_loop_dictionary`

**Notes:**

1. Primary secondary configuration is correct if:
1). a cooling loop is either connected to chiller or cooling coil, but not both
2). if a cooling loop is connected to chiller, it shall have child loop(s)
3). if a cooling loop is connected to cooling coil, it shall not have any child loops (AND will not be in the fluid_loop array)

2. B-RMR might have process chiller(s). Process chiller(s) and its associated loop(s) should be excluded from the primary-secondary loop check. Hence the logic only returns primary loops that serves standard baseline systems with chilled water coils.

3. Zonal cooling coils are not considered as this function will be used for baseline systems only.

**[Back](../_toc.md)**