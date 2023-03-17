
## get_heat_rejection_loops_connected_to_baseline_systems

Description: Get a list of all heat rejection loops in an RMI that are connected to a baseline HVAC System (Type-7, 8, 11.1, 11.2, 12, 13, 7b, 8b, 11.1b, 12b)

Inputs:  
- **RMI**: RMI that needs to get the list of primary and secondary loops (usually baseline RMI).

Returns: 
- **heat_rejection_loop_list**: A list that saves the ids of heat rejection loops in the model that serve baseline system types, e.g. [heat_rejection_loop1.id, heat_rejection_loop2.id]. If RMI does not have any qualifying heat rejection loops, it will return an empty list ([]).

Logic:  

- Get RMI system types: `baseline_hvac_system_dict = get_baseline_system_types(RMI)`

- For each chiller in RMI, save its cooling loop to CHW chiller loop array to get all loops connected to chiller(s): `for chiller in RMI.RulesetModelInstance.chillers: chiller_loop_array.append(chiller.cooling_loop)`

- For each building segment in RMI: `for building_segment in RMI...building_segments:`

  - For each HVAC system in building segment: `for hvac in building_segment.heating_ventilating_air_conditioning_systems`

    - Check if HVAC system is baseline system Type-7, 8, 11.1, 11.2, 12, 13, 7b, 8b, 11.1b, 12b: `if any(hvac.id in baseline_hvac_system_dict[sys_type] for sys_type in ["SYS-7", "SYS-8", "SYS-11.1", "SYS-11.2", "SYS-12", "SYS-13", "SYS-7B", "SYS-8B", "SYS-11B", "SYS-12B", "SYS-13B"]):`

      - Save chilled water loop that serves cooling systems to non-process CHW coil loop array (array for all loops connected to cooling coils): `non_process_chw_coil_loop_array.append(hvac.cooling_system.chilled_water_loop)`

- For each fluid loop in RMI: `for fluid_loop in RMI.RulesetModelInstance.fluid_loops:`

  - Check if loop type is cooling: `if fluid_loop.type == "COOLING":`

    - Check if loop is connected to chillers, but not cooling coils: `if ( fluid_loop.id in chiller_loop_array ) AND ( !fluid_loop in non_process_chw_coil_loop_array ):
`
      - Check if all child loops of loop serve baseline system Type-7, 8, 11.1, 11.2, 12, 13, 7b, 8b, 11.1b, 12b only (to exclude CHW loop served by process chiller(s)): `if all(child_loop_id in non_process_chw_coil_loop_array for child_loop_id in fluid_loop.child_loops):`

        - Save loop to primary loop array: `primary_loop_array.append(fluid_loop.id)`  
  
  - For each chiller in the model, check if the cooling loop is in either the primary_loop_array or in the non_process_chw_coil_loop_array: `if (chiller.cooling_loop.id in primary_loop_array) OR (chiller.cooling_loop.id in non_process_chw_coil_loop_array):`

    - append the chiller condensing loop id to the heat_rejection_loop_list if the chiller.condensing_loop exists: `heat_rejection_loop_list.append(chiller.condesing_loop.id) if chiller.condensing_loop != null`

**Returns** `return primary_secondary_loop_dictionary`

**Notes:**

1. Provides heat rejection loop even if the CHW system is not correctly modeled with primary / secondary configuration
2. 
**[Back](../_toc.md)**
