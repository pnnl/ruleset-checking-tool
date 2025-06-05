
## get_heat_rejection_loops_connected_to_baseline_systems

Description: Get a list of all heat rejection loops in an RMI that are connected to a baseline HVAC System (Type-7, 8, 11.1, 11.2, 12, 13, 7b, 8b, 11.1b, 12b)

Inputs:  
- **RMI**: RMI that needs to get the list of primary and secondary loops (usually baseline RMI).

Returns: 
- **heat_rejection_loop_set**: A set that saves the ids of heat rejection loops in the model that serve baseline system types, e.g. [heat_rejection_loop1.id, heat_rejection_loop2.id]. If RMI does not have any qualifying heat rejection loops, it will return an empty list ([]).

**Function Call:** 
1. get_primary_secondary_loops()   

Logic:  

- get the dictionary of primary and secondary loops using get_primary_secondary_loops(): `primary_secondary_loops_dict = get_primary_secondary_loops(RMI)` 
  
- For each chiller in the model, check if the cooling loop is one of the keys in primary_secondary_loops_dict (this means it is a primary loop): `if (chiller.cooling_loop.id in primary_secondary_loops_dict):`

  - add the chiller condensing loop id to the heat_rejection_loop_set if the chiller.condensing_loop exists: `heat_rejection_loop_set.add(chiller.condesing_loop.id) if chiller.condensing_loop != null`

**Returns** `return heat_rejection_loop_set`

**Notes:**


**[Back](../_toc.md)**
