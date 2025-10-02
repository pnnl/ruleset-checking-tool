## compare_swh_dist_systems_and_components

Description: This function compares all sub-components of a given SWH Distribution System ID between two models.  The function also accepts   

Inputs:
- **RMD1**
- **RMD2**
- **compare_context_str**
- **swh_distribution_id**

Returns:
- **errors**: An array of errors encountered in this function and in compare_context_pair.  If errors is an empty array, then all elements that were expected to match do match

Function Call:

- **compare_context_pair** - there is no RDS for this function, but it is a function developed for Rule 1-6 that compares two elements  
- **get_component_by_id**

Data Lookup: None

Logic:
  - create the list errors: `errors = []`
  - use the function get_swh_components_associated_with_each_swh_distribution_system to get a dictionary of SWH equipment associated with each Distribution System for model 1 (pumps, tanks, SWH use, distribution system, etc): `RMD1_swh_system_and_equip_dict = get_swh_components_associated_with_each_swh_distribution_system(RMD1)`
  - use the function get_swh_components_associated_with_each_swh_distribution_system to get a dictionary of SWH equipment associated with each Distribution System for model 2 (pumps, tanks, SWH use, distribution system, etc): `RMD2_swh_system_and_equip_dict = get_swh_components_associated_with_each_swh_distribution_system(RMD2)`

  - check if this distribution ID is in model 1: `if RMD1_swh_system_and_equip_dict[swh_distribution_id]:`
    - get the dictionary of all SWH equipment (pumps, tanks, SWH use, dist system, etc) for the given swh_distribution_id for RMD1: `RMD1_swh_equipment_dict = RMD1_swh_system_and_equip_dict[swh_distribution_id]`
    - get the actual distribution equipment associated with this ID from model 1: `RMD1_swh_distribution = get_component_by_id(RMD1, swh_distribution_id)`
  - otherwise, add an error to the list: `else: errors.append("SWH Distribution System " + swh_distribution_id + " not found in one of the two RMDs")`

  - check if this distribution ID is in model 2: `if RMD2_swh_system_and_equip_dict[swh_distribution_id]:`
    - get the dictionary of all SWH equipment (pumps, tanks, SWH use, dist system, etc) for the given swh_distribution_id for RMD2: `RMD2_swh_equipment_dict = RMD2_swh_system_and_equip_dict[swh_distribution_id]`
    - get the actual distribution equipment associated with this ID from model 2: `RMD2_swh_distribution = get_component_by_id(RMD2, swh_distribution_id)`
  - otherwise...: `else:`
    -  add an error an error to the list: `errors.append("SWH Distribution System " + swh_distribution_id + " not found in one of the two RMDs")`


  - the following two lines set the longer of the two swh_distribution lists to the index_content_list and the shorter to the compare_context_list
  - `if len(RMD1_swh_distribution) > len(RMD2_swh_distribution): index_content_list = RMD1_swh_distribution, compare_context_list = RMD2_swh_distribution`
  -  `else: index_content_list = RMD2_swh_distribution, compare_context_list = RMD1_swh_distribution`
  - Compare the distribution in the two models using the function compare_context_pair.  compare_context_pair is recursive, so by sending the function the distribution systems, it is also checking the tanks and piping that are child objects of the distribution systems.  If the comparison fails, we add an error to the errors list indicating the id of the swh distribution system that failed comparison : `compare_context_pair(index_context=index_content_list, compare_context=compare_context_list, extra_schema='extra_schema_for_SWH_comparison.json', error_msg_list=errors, search_key = compare_context_str)`
  - In addition to the equipment connected to the distribution system, there's also equipment that's part of the service water heating distribution system that are not direct child objects of the distribution system.  We need to check these objects.
  - first, check ServiceWaterHeatingEquipment - when we execute compare_context_pair, this will also check any child objects that exist (SolarThermal and SWH validation point).  Start by checking if there are the same number of objects in models 1 and 2.  We need to do the length check here because it's not checked implicitly as part of compare_context_pair.  For example, if there are more pieces of equipment in the model 1 than model 2, comparing each item found in model 2 could return a false positive: `if len(RMD1_swh_equipment_dict["SWHHeatingEq"]) == len(RMD2_swh_equipment_dict["SWHHeatingEq"]):`
    - look at each SWHEquipment in the model 1: `for swh_eq_id in RMD1_swh_equipment_dict["SWHHeatingEq"]:`
      - get the SWH equipment for models 1 and 2: `swh_eq_1 = get_component_by_id(RMD1, swh_eq_id), swh_eq_2 = get_component_by_id(RMD2, swh_eq_id)`
      - the following two lines set the longer of the two equipment lists to the index_content_list and the shorter to the compare_context_list
      - `if len(swh_eq_1) > len(swh_eq_2): index_content_list = swh_eq_1, compare_context_list = swh_eq_2`
      -  `else: index_content_list = swh_eq_2, compare_context_list = swh_eq_1`
      - compare the two SWH equipment using compare_context_pair.  By passing in the same errors list, any new errors get appended to the list.  If the comparison fails, we add an error to the errors list indicating the id of the swh equipment that failed comparison: `compare_context_pair(index_context=index_content_list, compare_context=compare_context_list, extra_schema='extra_schema_for_SWH_comparison.json', error_msg_list=errors, search_key = compare_context_str): errors.append("Comparison of SWH Equipment: " + swh_eq_id + " failed.")`
  - otherwise there is an unequal number of equipment entries.  Add our own error to the errors list: `else: errors.append("Unequal numbers of SWH Equipment between the two models for " + swh_distribution_id(`
  - next, check Pumps - this will also recursively check PumpOutputValidationPointPumpOutputValidationPoint: `if len(RMD1_swh_equipment_dict["Pumps"]) == len(RMD2_swh_equipment_dict["Pumps"]):`
    - look at each SWHEquipment in the proposed model: `for pump_id in RMD1_swh_equipment_dict["Pumps"]:`
      - get the pumps for models 1 and 2: `pump_1 = get_component_by_id(RMD1, pump_id), pump_2 = get_component_by_id(RMD2, pump_id)`
      - the following two lines set the longer of the two pump lists to the index_content_list and the shorter to the compare_context_list
      - `if len(pump_1) > len(pump_2): index_content_list = pump_1, compare_context_list = pump_2`
      -  `else: index_content_list = pump_2, compare_context_list = pump_1`
      - compare the two pumps using compare_context_pair.  If the comparison fails, we add an error to the errors list indicating the id of the swh pump that failed comparison: `compare_context_pair(index_context=index_content_list, compare_context=compare_context_list, extra_schema='extra_schema_for_SWH_comparison.json', error_msg_list=errors, search_key = compare_context_str)`
  - otherwise, there are an an unequal number of pump entries: `else: errors.append("Unequal number of pumps in the two models for SWH Distribution System " + swh_distribution_id)`

**Returns** errors

**[Back](../_toc.md)**

**Notes:**
