# Rule Definition Development Strategy

### Introduction
The following documentation provides a technical description of ASHRAE 90.1-2019 Appendix G rules as defined in the ASHRAE 229P Test Case Descriptions (TCD) based on the construct of the Ruleset Checking Tool (RCT) Rule Definitions.  This document serves as a bridge between the ASHRAE 229 TCDs, which are in the form of the ruleset, and the RCT Rule Definitions, which are in the form of Python classes.  Each Rule Definition Development Strategy document seeks to describe a TCD Rule in pseudocode that can be understood by ASHRAE 90.1 professionals and Python developers alike.  The documents are organized based on 90.1 section and TCD Rule.  Front matter is included that describes any standard conventions, nomenclature or use of pseudocode functions.  The purpose of this document is not to provide direct Python code, rather to convey the logic necessary to develop code that meets the intent of the 229 TCDs.

### Notes on Evaluating Rules Separately for Buildings
Most rules documented in the RDS apply to data groups that are located within the *buildings* array.  It is typical that an RMD will only include a single *building* object.  In the case where multiple *building* objects exists in an RMD, each rule will be evaluated independently for each *building* object.  The following is a list of sections that will be evaluated for each *building* object in the RMD per the previous description: 
 - 5  
 - 6  
 - 12  
 - 16  
 - 17  

The *transformers* data group is handled differently, since the data group exists at the top level of the RMD schema.  For any rules related to distribution transformers, the rule is evaluated only the *transformers* list and *buildings* are ignored in the rule evaluation.  This is only applicable to the following section:
- 15  

These conventions are used in all RDS below, and the logic of evaluating rules for each *building* or *transformer* are not described in the individual RDS document.

## Reference Material
  * [Rule Template](_rule_template.md): Template file for creating a new Rule Definition Development Strategy document
  * [Functions](_functions.md): A list of functions used within the Rule Definition Development Strategy documents

## Ruleset Functions

### General ruleset functions
  * [get_lighting_status_type](ruleset_functions/get_lighting_status_type.md): This function would determine whether the space lighting status type is 1). not-yet designed or match Table 9_5_1, 2). as-designed or as-existing.  
  * [get_opaque_surface_type](ruleset_functions/get_opaque_surface_type.md): This function would determine whether it is a wall, ceiling or floor.  
  * [get_surface_conditioning_category](ruleset_functions/get_surface_conditioning_category.md): This function would cycle through each surface in  a zone and categorize it as exterior res, exterior non res, exterior mixed, semi-exterior or unregulated.  
  * [get_wwr](ruleset_functions/get_wwr.md): This function would determine window wall ratio for a building segment.  
  * [get_zone_conditioning_category.md](ruleset_functions/get_zone_conditioning_category.md): Determine the Zone Conditioning Category for each zone. This function would cycle through each zone in an RMD and categorize it as ‘conditioned’, 'semi-heated’, 'unenclosed' or ‘unconditioned’.  If ‘conditioned’ it will also categorize the space as ‘residential’ or ‘non-residential’.  
  * [normalize_interior_lighting_schedules](ruleset_functions/normalize_interior_lighting_schedules.md):This function would determine a normalized schedule for a data element in space.
  * [compare_schedules](ruleset_functions/compare_schedules.md): This function would compare two schedules and determine if they match with or without a comparison factor when applicable.  
  * [get_fuels_modeled_in_RMD](ruleset_functions/get_fuels_modeled_in_RMD.md): Get a list of the fuels used in the RMD.  Includes fuels used by HVAC systems including terminal units, chillers, boilers, ExternalFluidSources, and SWHs.
  * [get_primary_secondary_loops_dict](ruleset_functions/get_primary_secondary_loops_dict.md): Get the list of primary and secondary loops for CHW for a B-RMD.
  * [get_hvac_systems_5_6_serving_multiple_floors_b](ruleset_functions/get_hvac_systems_5_6_serving_multiple_floors_b.md): Get a dictionary of the system 5, 5a, 5b, 6, 6a, 6b hvac system IDs that are modeled as serving more than one floor in the baseline design model.  The dictionary consists of the hvac system ids as the key and the number of floors served as the value associated with the key.
  * [get_zones_computer_rooms](ruleset_functions/get_zones_computer_rooms.md): Returns a dictionary with the zones that have at least one computer room space associated with them in the RMD as the keys. The values associated with each key are in a list form. The list associated with each key contains the computer room floor area as the first item in the list and the total zone floor area as the second item in the list.
  * [get_HVAC_systems_primarily_serving_comp_rooms](ruleset_functions/get_HVAC_systems_primarily_serving_comp_rooms.md): Returns a list of HVAC systems in which greater than 50% of the area served by the HVAC system is computer room space.
  * [get_dict_of_zones_and_terminal_units_served_by_hvac_sys](ruleset_functions/get_dict_of_zones_and_terminal_units_served_by_hvac_sys.md): Returns a dictionary of zones and terminal unit IDs associated with each HVAC system in the RMD.
  * [get_baseline_system_type](ruleset_functions/get_baseline_system_types.md): Identify all the baseline system types modeled in a B-RMD.
  * [get_hvac_zone_list_w_area](ruleset_functions/get_hvac_zone_list_w_area.md): Get the list of zones and their total floor area served by each HVAC system in a RMD.
  * [check_purchased_chw_hhw_status_dict](ruleset_functions/check_purchased_chw_hhw_status_dict.md): Check if RMI is modeled with purchased chilled water as space cooling source or purchased hot water/steam as space heating source. If any system in RMI uses purchased chilled water, function shall return True for purchased chilled water as space cooling source. Similarly, if any system in RMI uses purchased hot water or steam, function shall return True for purchased hot water/steam as space heating source.
  * [get_proposed_hvac_modeled_with_virtual_heating](ruleset_functions/get_proposed_hvac_modeled_with_virtual_heating.md): Get the list of HeatingVentilationAirAconditioningSystem in which Appendix G Table G3.1 #10 c is applicable (i.e. space heating is modeled in the P_RMR but not the U_RMR).  Table G3.1 #10 c states that "where no heating system exists or no heating system has been submitted with design documents, the system type shall be the same system as modeled in the baseline building design and shall comply with but not exceed the requirements of Section 6."
  * [get_fan_object_electric_power](ruleset_functions/get_fan_object_electric_power.md): Get the fan power associated with a fan object.
  * [get_heat_rejection_loops_connected_to_baseline_systems](ruleset_functions/get_heat_rejection_loops_connected_to_baseline_systems.md): Get a list of all heat rejection loops in an RMI that are connected to a baseline HVAC System (Type-7, 8, 11.1, 11.2, 12, 13, 7b, 8b, 11.1b, 12b)
  * [get_fan_system_object_supply_return_exhaust_relief_total_kW_CFM](ruleset_functions/get_fan_system_object_supply_return_exhaust_relief_total_kW_CFM.md): Get the supply, return, exhaust, and relief total fan power, CFM, quantity, and information about whether the pressure drop is consistent across the fans if more than one for a fan system object.   The function returns a dictionary that saves the supply, return, exhaust, and relief fan power as a list, saves the supply, return, exhaust, and relief cfm as a list, saves the supply, return, exhaust, and relief quantity as a list, and saves for each fan whether the pressure drop is undefined, identical, or different across fans (if only one it will return undefined or identical) but returns the quantity and information about the pressure drop across fans to help assess whether series or parallel.
  * [are_all_hvac_sys_fan_objs_autosized](ruleset_functions/are_all_hvac_sys_fan_objs_autosized.md): Returns true or false. The function returns true if all supply fan objects associated with an hvac system are autosized.
  * [is_economizer_modeled_in_proposed](ruleset_functions/is_economizer_modeled_in_proposed.md): Returns true or false. The function returns true if at least one zone served by the baseline HVAC system sent to the function is served by an hvac system with an economizer in the proposed design. The function returns false otherwise.

### HVAC type functions
  * [is_baseline_system_1](ruleset_functions/baseline_systems/is_baseline_system_1.md): Get either Sys-1, Sys-1a, Sys-1b, Sys-1c, or Not_Sys_1 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 1 (PTAC), system 1a (system 1 with purchased CHW), system 1b (system 1 with purchased heating), system 1c (system 1 with purchased CHW and purchased HW).
  * [is_baseline_system_1a](ruleset_functions/baseline_systems/is_baseline_system_1a.md): Returns true or false to whether the baseline system type is 1a (system 1 with purchased CHW and HW served by a boiler). 
  * [is_baseline_system_1c](ruleset_functions/baseline_systems/is_baseline_system_1c.md): Returns true or false to whether the baseline system type is 1c (system 1 with purchased CHW and purchased HW).
  * [is_baseline_system_2](ruleset_functions/baseline_systems/is_baseline_system_2.md): Get either Sys-2 or Not_Sys_2 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 2 (PTHP).
  * [is_baseline_system_3](ruleset_functions/baseline_systems/is_baseline_system_3.md): Get either Sys-3, Sys-3a, Sys-3b, Sys-3c, or Not_Sys_3 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 3 (PSZ), system 3a (system 3 with purchased CHW), system 3b (system 3 with purchased heating), system 3c (system 3 with purchased CHW and purchased HW).
  * [is_baseline_system_4](ruleset_functions/baseline_systems/is_baseline_system_4.md): Get either Sys-4 or Not_Sys_4 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 4 (PSZ-HP).
  * [is_baseline_system_5](ruleset_functions/baseline_systems/is_baseline_system_5.md): Get either Sys-5, Sys-5b, or Not_Sys_5 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 5 (Package VAV with Reheat) or system 5b (system 5 with purchased heating). 
  * [is_baseline_system_6](ruleset_functions/baseline_systems/is_baseline_system_6.md): Get either Sys-6, Sys-6b, or Not_Sys_6 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 6 (Package VAV with PFP Boxes) or system 6b (system 6 with purchased heating).
  * [is_baseline_system_7](ruleset_functions/baseline_systems/is_baseline_system_7.md): Get either Sys-7, Sys-7a, Sys-7b, Sys-7c or Not_Sys_7 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 7 (VAV with Reheat), system 7a (system 7 with purchased CHW), system 7b (system 7 with purchased heating), pr system 7c (system 7 with purchased heating and purchased CHW).
  * [is_baseline_system_8](ruleset_functions/baseline_systems/is_baseline_system_8.md): Get either Sys-8, Sys-8a, Sys-8b, Sys-8c, or Not_Sys_8 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 8 (VAV with Parallel Fan-Powered Boxes and Reheat), system 8a (system 8 with purchased CHW), system 8b (system 8 with purchased heating), or 8c (system 8 with purchased heating and purchased chilled water).
  * [is_baseline_system_9](ruleset_functions/baseline_systems/is_baseline_system_9.md): Get either Sys-9, Sys-9b, or Not_Sys_9 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 9 (Heating and Ventilation) or system 9b (system 9 with purchased heating).
  * [is_baseline_system_9b](ruleset_functions/baseline_systems/is_baseline_system_9b.md): Returns true or false to whether the baseline system type is 9b (system 9 with purchased HW).
  * [is_baseline_system_10](ruleset_functions/baseline_systems/is_baseline_system_10.md): Get either Sys-10 or Not_Sys_10 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 10 (Heating and Ventilation with electric heating).
  * [is_baseline_system_11.1](ruleset_functions/baseline_systems/is_baseline_system_11.1.md): Get either Sys-11.1, Sys-11.1a, Sys-11b, Sys-11c, or Not_Sys_11.1 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 11.1 (Single Zone VAV System with Electric Resistance Heating), system 11.1a (system 11.1 with purchased CHW), system 11b (system 11.1 with purchased heating), or system 11c (system 11.1 with purchased CHW and purchased heating).
  * [is_baseline_system_11.2](ruleset_functions/baseline_systems/is_baseline_system_11.2.md): Get either Sys-11.2, Sys-11.2a or Not_Sys_11.2 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 11.2 (Single Zone VAV System with Hot Water Heating (Boiler)) or system 11.2a (system 11.2 with purchased CHW).
  * [is_baseline_system_12](ruleset_functions/baseline_systems/is_baseline_system_12.md): Get either Sys-12, Sys-12a, Sys-12b, Sys-12c, or Not_Sys_12 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 12 (Single Zone Constant Volume System with CHW and HW), system 12a (system 12 with purchased CHW), system 12b (system 12 with purchased heating), system 12c (system 12 with purchased CHW and purchased HW).
  * [is_baseline_system_13](ruleset_functions/baseline_systems/is_baseline_system_13.md): Get either Sys-13, Sys-13a, or Not_Sys_13 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 13 (Single Zone Constant Volume System with CHW and Electric Resistance) or system 13a (system 13 with purchased CHW).

### HVAC sub functions
  * [are_all_terminal_heat_sources_hot_water](ruleset_functions/baseline_systems/baseline_hvac_sub_functions/are_all_terminal_heat_sources_hot_water(hvac.id).md): Returns TRUE if the heat source associated with all terminal units input to this function is HOT_WATER. It returns FALSE if any terminal unit has a heat source other than HOT_WATER.
  * [is_hvac_sys_heating_type_elec_resistance](ruleset_functions/baseline_systems/baseline_hvac_sub_functions/is_hvac_sys_heating_type_elec_resistance.md): Returns TRUE if the HVAC system heating system heating type is ELECTRIC_RESISTANCE. Returns FALSE if the HVAC system heating system has anything other than ELECTRIC_RESISTANCE.
  * [is_hvac_sys_cooling_type_none](ruleset_functions/baseline_systems/baseline_hvac_sub_functions/is_hvac_sys_cooling_type_none.md): Returns TRUE if the HVAC system cooling type is None or Null. Returns FALSE if the HVAC system has anything other than None or Null for the cooling type or if it has more than 1 or no cooling system.
  * [do_all_terminals_have_one_fan](ruleset_functions/baseline_systems/baseline_hvac_sub_functions/do_all_terminals_have_one_fan.md): Returns TRUE if the fan data element associated with all terminal units input to this function are equal to one (i.e., there is only one fan associated with the terminal unit). It returns FALSE if any terminal unit has a fan data element not equal to one (i.e., there is NOT only one fan associated with the terminal unit).
  * [are_all_terminal_fan_configs_parallel](ruleset_functions/baseline_systems/baseline_hvac_sub_functions/are_all_terminal_fan_configs_parallel.md): Returns TRUE if the fan configuration associated with all terminal units input to this function are parallel. It returns FALSE if any terminal unit has a fan configuration other than parallel.
  * [are_all_terminal_heat_sources_electric](ruleset_functions/baseline_systems/baseline_hvac_sub_functions/are_all_terminal_heat_sources_electric.md): Returns TRUE if the heat source associated with all terminal units input to this function are electric. It returns FALSE if any terminal unit has a heat source other than electric.
  * [is_hvac_sys_preheating_type_elec_resistance](ruleset_functions/baseline_systems/baseline_hvac_sub_functions/is_hvac_sys_preheating_type_elec_resistance.md): Returns TRUE if the HVAC system preheating system heating type is ELECTRIC_RESISTANCE. Returns FALSE if the HVAC system preheating system has anything other than ELECTRIC_RESISTANCE.
  * [are_all_terminal_heating_loops_purchased_heating](ruleset_functions/baseline_systems/baseline_hvac_sub_functions/are_all_terminal_heating_loops_purchased_heating.md): Returns TRUE if the fluid loop associated with the heating_from_loop associated with each terminal unit is purchased heating. Returns FALSE if this is not the case.
  * [is_hvac_sys_preheat_fluid_loop_attached_to_boiler](ruleset_functions/baseline_systems/baseline_hvac_sub_functions/is_hvac_sys_preheat_fluid_loop_attached_to_boiler.md): Returns TRUE if the fluid loop associated with the preheat system associated with the HVAC system is attached to a boiler. Returns FALSE if this is not the case.
  * [is_hvac_sys_preheat_fluid_loop_purchased_heating](ruleset_functions/baseline_systems/baseline_hvac_sub_functions/is_hvac_sys_preheat_fluid_loop_purchased_heating.md): Returns TRUE if the fluid loop associated with the preheating system associated with the HVAC system is attached to an external purchased heating loop. Returns FALSE if this is not the case.
  * [is_hvac_sys_preheating_type_fluid_loop](ruleset_functions/baseline_systems/baseline_hvac_sub_functions/is_hvac_sys_preheating_type_fluid_loop.md): Returns TRUE if the HVAC system preheating system heating type is fluid loop. Returns FALSE if the HVAC system preheating system has anything other than fluid loop.
  * [are_all_terminal_cool_sources_chilled_water](ruleset_functions/baseline_systems/baseline_hvac_sub_functions/are_all_terminal_cool_sources_chilled_water.md): Returns TRUE if the cool source associated with all terminal units is CHILLED_WATER. It returns FALSE if any terminal unit has a cool source other than CHILLED_WATER.
  * [are_all_terminal_types_VAV](ruleset_functions/baseline_systems/baseline_hvac_sub_functions/are_all_terminal_types_VAV.md): Returns TRUE if all of the terminal unit types input to this function are variable air volume (VAV). It returns FALSE if any of the terminal units are of a type other than variable air volume (VAV).
  * [is_hvac_sys_heating_type_furnace](ruleset_functions/baseline_systems/baseline_hvac_sub_functions/is_hvac_sys_heating_type_furnace.md): Returns TRUE if the HVAC system heating system heating type is furnace. Returns FALSE if the HVAC system heating system has anything other than furnace or if it has more than 1 heating system.
  * [is_hvac_sys_fluid_loop_attached_to_chiller](ruleset_functions/baseline_systems/baseline_hvac_sub_functions/is_hvac_sys_fluid_loop_attached_to_chiller.md): Returns TRUE if the fluid loop associated with the cooling system associated with the HVAC system is attached to a chiller. Returns FALSE if this is not the case.
  * [is_hvac_sys_cooling_type_DX](ruleset_functions/baseline_systems/baseline_hvac_sub_functions/is_hvac_sys_cooling_type_DX.md): Returns TRUE if the HVAC system has DX cooling. Returns FALSE if the HVAC system has anything other than DX cooling or if it has more than 1 or no cooling system.
  * [is_hvac_sys_fan_sys_CV](ruleset_functions/baseline_systems/baseline_hvac_sub_functions/is_hvac_sys_fan_sys_CV.md): Returns TRUE if the HVAC system fan system is constant volume. Returns FALSE if the HVAC system fan system is anything other than constant volume.
  * [is_hvac_sys_heating_type_heat_pump](ruleset_functions/baseline_systems/baseline_hvac_sub_functions/is_hvac_sys_heating_type_heat_pump.md): Returns TRUE if the HVAC system has heat pump as the heating system type. Returns FALSE if the HVAC system has anything other than heat pump as the heating system type or if it has more than 1 heating system.
  * [is_hvac_sys_fluid_loop_attached_to_boiler](ruleset_functions/baseline_systems/baseline_hvac_sub_functions/is_hvac_sys_fluid_loop_attached_to_boiler.md): Returns TRUE if the fluid loop associated with the heating system associated with the HVAC system is attached to a boiler. Returns FALSE if this is not the case. 
  * [does_hvac_system_serve_single_zone](ruleset_functions/baseline_systems/baseline_hvac_sub_functions/does_hvac_system_serve_single_zone.md): Returns TRUE if the HVAC system serves a single zone. Returns FALSE if the HVAC system serves multiple zones. 
  * [is_hvac_sys_heating_type_fluid_loop](ruleset_functions/baseline_systems/baseline_hvac_sub_functions/is_hvac_sys_heating_type_fluid_loop.md): Returns TRUE if the HVAC system heating system heating type is fluid loop. Returns FALSE if the HVAC system heating system has anything other than fluid loop or if it has more than 1 heating system. 
  * [is_hvac_sys_cooling_type_fluid_loop](ruleset_functions/baseline_systems/baseline_hvac_sub_functions/is_hvac_sys_cooling_type_fluid_loop.md): Returns TRUE if the HVAC system has fluid_loop cooling. Returns FALSE if the HVAC system has anything other than fluid_loop cooling or if it has more than 1 cooling system.
  * [are_all_terminal_cool_sources_none_or_null](ruleset_functions/baseline_systems/baseline_hvac_sub_functions/are_all_terminal_cool_sources_none_or_null.md): Returns TRUE if the cool source associated with all terminal units input to this function are None or Null. It returns FALSE if any terminal unit has a cool source other than None or Null. 
  * [are_all_terminal_heat_sources_none_or_null](ruleset_functions/baseline_systems/baseline_hvac_sub_functions/are_all_terminal_heat_sources_none_or_null.md): Returns TRUE if the heat source associated with all terminal units input to this function are None or Null. It returns FALSE if any terminal unit has a heat source other than None or Null.
  * [are_all_terminal_supplies_ducted](ruleset_functions/baseline_systems/baseline_hvac_sub_functions/are_all_terminal_supplies_ducted.md): Returns TRUE if all of the terminal supplies are ducted (i.e., is_supply_ducted = TRUE) for the list of terminal units input to the function. It returns FALSE if any of the terminal supplies are not ducted (i.e., is_supply_ducted = FALSE). 
  * [are_all_terminal_types_CAV](ruleset_functions/baseline_systems/baseline_hvac_sub_functions/are_all_terminal_types_CAV.md): Returns TRUE if all of the terminal unit types input to this function are constant air volume (CAV) or if this data element is undefined. It returns FALSE if any of the terminal units are of a type other than constant air volume (CAV).
  * [are_all_terminal_fans_null](ruleset_functions/baseline_systems/baseline_hvac_sub_functions/are_all_terminal_fans_null.md): Returns TRUE if the fan data element associated with all terminal units input to this function are equal to Null. It returns FALSE if any terminal unit has a fan data element not equal to Null.
  * [does_each_zone_have_only_one_terminal](ruleset_functions/baseline_systems/baseline_hvac_sub_functions/does_each_zone_have_only_one_terminal.md): Returns TRUE if each zone input to this function only has one terminal unit. It returns FALSE if any zone has more than one terminal unit. 
  * [is_hvac_sys_fluid_loop_purchased_CHW](ruleset_functions/baseline_systems/baseline_hvac_sub_functions/is_hvac_sys_fluid_loop_purchased_CHW.md): Returns TRUE if the fluid loop associated with the cooling system associated with the HVAC system is attached to an external purchased chilled water loop. Returns FALSE if this is not the case. 
  * [is_hvac_sys_fan_sys_VSD](ruleset_functions/baseline_systems/baseline_hvac_sub_functions/is_hvac_sys_fan_sys_VSD.md): Returns TRUE if the HVAC system fan system is variable speed drive controlled. Returns FALSE if the HVAC system fan system is anything other than variable speed drive controlled. 
  * [are_all_terminal_heating_loops_attached_to_boiler](ruleset_functions/baseline_systems/baseline_hvac_sub_functions/are_all_terminal_heating_loops_attached_to_boiler.md): Returns TRUE if the fluid loop associated with the heating_from_loop associated with each terminal unit is attached to a boiler. Returns FALSE if this is not the case.
  * [is_hvac_system_multizone](ruleset_functions/baseline_systems/baseline_hvac_sub_functions/is_hvac_system_multizone.md): Returns TRUE if the HVAC system serves multiple zones. Returns FALSE if the HVAC system serves a single or no zones.
  * [is_hvac_sys_fluid_loop_purchased_heating](ruleset_functions/baseline_systems/baseline_hvac_sub_functions/is_hvac_sys_fluid_loop_purchased_heating.md): Returns TRUE if the fluid loop associated with the heating system associated with the HVAC system is attached to an external purchased heating loop. Returns FALSE if this is not the case.
  * [are_all_terminal_types_CAV_With_None_Equal_to_Null](ruleset_functions/baseline_systems/baseline_hvac_sub_functions/are_all_terminal_types_CAV_With_None_Equal_to_Null.md): Returns TRUE if all of the terminal unit types input to this function are constant air volume (CAV). It returns FALSE if any of the terminal units are of a type other than constant air volume (CAV).
  * [get_dict_with_terminal_units_and_zones](ruleset_functions/baseline_systems/baseline_hvac_sub_functions/get_dict_with_terminal_units_and_zones.md): Returns a dictionary of zone IDs associated with each terminal unit in the RMD.
  * [are_all_terminal_CHW_loops_purchased_cooling](ruleset_functions/baseline_systems/baseline_hvac_sub_functions/are_all_terminal_CHW_loops_purchased_cooling.md): Returns TRUE if the fluid loop associated with the cooling_from_loop associated with each terminal unit is purchased CHW. Returns FALSE if this is not the case.
  * [get_most_used_weekday_hourly_schedule](ruleset_functions/get_most_used_weekday_hourly_schedule.md): Get the most used weekday hourly schedule from an annual 8760 schedule as list of hourly values for a 24 hour period.
  * [get_aggregated_zone_hvac_fan_operating_schedule](ruleset_functions/get_aggregated_zone_hvac_fan_operating_schedule.md): This function loops through all of the HVAC system fan operating schedules associated with a specific zone and creates an aggregated fan operating schedule for the zone. More specifically, if any of the fan operating schedules associated with any of the hvac systems serving the zone have a 1 for a particular hour of the year then the aggregated schedule will equal 1 for that particular hour of the year. The function will check this for each hour of the year and return an 8760 aggregated fan operating schedule.
  * [get_zone_supply_return_exhaust_relief_terminal_fan_power_dict](ruleset_functions/get_zone_supply_return_exhaust_relief_terminal_fan_power_dict.md): Get the supply, return, exhaust, relief, and terminal total fan power for each zone. The function returns a dictionary that saves each zone's supply, return, exhaust, relief  and terminal unit fan power as a list {zone.id: [supply fan power kW, return fan power kW, exhaust fan power kW, relief fan power kW, terminal fan power]}. Values will be equal to zero where not defined for a fan system. Zonal exhaust and non-mechanical cooling is not included.
  * [get_hvac_sys_and_assoc_zones_largest_exhaust_source](ruleset_functions/get_hvac_sys_and_assoc_zones_largest_exhaust_source.md): Returns a list with the sum of the hvac fan system exhaust fan cfm values, the maximum zone level exhaust source across the zones associated with the HVAC system, the number of exhaust fans associated with the hvac fan system, and the maximum cfm of all of the exhaust fans associated with the hvac system fan system [hvac_sys_exhaust_cfm_sum, maximum_zone_exhaust, num_hvac_exhaust_fans, maximum_hvac_exhaust]. This is for evaluating G3.1.2.10 exception 6 which states "Where the largest exhaust source is less than 75% of the design outdoor airflow. This exception shall only be used if exhaust air energy recovery is not used in the proposed design. "
  * [is_CZ_0_to_3a](ruleset_functions/is_CZ_0_to_3a.md): Determines whether the building is in climate zone 0 to 3a - used for Appendix G Table G3.1.1-3.
  * [get_zone_peak_internal_load_floor_area](ruleset_functions/get_zone_peak_internal_load_floor_area.md): finds the peak coincident internal loads of a zone and returns the value in btu/h/ft2


## Data Tables
  * [8.4.4](data_tables/Table8-4-4.md): Minimum Nominal Efficiency Levels for Low-Voltage Dry-Type Distribution Transformers  
  * [G3.1.1-1](data_tables/Table3-1-1-1.md): Baseline Building Vertical Fenestration Percentage of Gross Above-Grade-Wall Area  
  * G3.1.1-2: Baseline Service Water-Heating System
  * G3.1.1-3: Baseline HVAC System Types
  * G3.1.1-4: Baseline System Descriptions
  * G3.1.2.6: Climate Conditions under which Economizers are Included for Comfort Cooling for Baseline Systems 3 through 8 and 11, 12, 13
  * G3.1.2.9: Baseline Fan Brake Horsepower
  * G3.1.3.7: Type and Number of Chillers
  * G3.1.3.11: Heat-Rejection Leaving Water Temperature
  * G3.1.3.15: Part-Load Performance for VAV Fan Systems
  * G3.4-1: Performance Rating Method Building Envelope Requirements for Climate Zones 0 and 1 (A,B)
  * G3.4-2: Performance Rating Method Building Envelope Requirements for Climate Zone 2 (A,B)
  * G3.4-3: Performance Rating Method Building Envelope Requirements for Climate Zone 3 (A,B,C)
  * G3.4-4: Performance Rating Method Building Envelope Requirements for Climate Zone 4 (A,B,C)   
  * G3.4-5: Performance Rating Method Building Envelope Requirements for Climate Zone 5 (A,B,C)  
  * G3.4-6: Performance Rating Method Building Envelope Requirements for Climate Zone 6 (A,B)
  * G3.4-7: Performance Rating Method Building Envelope Requirements for Climate Zone 7
  * G3.4-8: Performance Rating Method Building Envelope Requirements for Climate Zone 8  
  * G3.5.1: Performance Rating Method Air Conditioners (efficiency ratings excludeing supply fan power)
  * G3.5.2: Performance Rating Method Electrically Operated Unitary and Applied Heat Pumps -- Minimum Efficiency Requirements (efficiency ratings excluding supply fan power)
  * G3.5.3: Performance Rating Method Water Chilling Packages -- Minimum Efficiency Requirements
  * G3.5.4: Performance Rating Method Electrically Operated Packaged Terminal Air Conditioners, Packaged Terminal Heat Pumps (efficiency ratings excluding supply fan power)
  * G3.5.5: Performance Rating Method Warm-Air Furnaces and Unit Heaters
  * G3.5.6: Performance Rating Method Gas-Fired Boilers -- Minimum Efficiency Requirements
  * G3.6: Performance Rating Method Lighting Power Densities for Building Exteriors
  * G3.7: Performance Rating Method Lighting Power Density Allowances and Occupancy Sensor Reductions Using the Space-by-Space Method
  * G3.8: Performance Rating Method Lighting Power Densities Using the Building Area Method
  * G3.9.1: Performance Rating Method Motor Efficiency Requirements
  * G3.9.2: Performance Rating Method Baseline Elevator Motor
  * G3.9.3: Performance Rating Method Hydraulic Elevator Motor Efficiency
  * G3.10.1: Performance Rating Method Commercial Refrigerators and Freezers
  * G3.10.2: Performance Rating Method Commercial Refrigeration

## Section 0 - General Requirements

## Section 3 - Space Use Classification
  
## Section 4 - Schedules
  * [4-1](section4/4-1.md): Temperature Control Setpoints shall be the same for proposed design and baseline building design.  
  * [4-2](section4/4-2.md): Humidity Control Setpoints shall be the same for proposed design and baseline building design. 
  * [4-3](section4/4-3.md): Schedules for HVAC fans that provide outdoor air for ventilation shall run continuously whenever spaces are occupied.  
  * [4-4](section4/4-4.md): Where no heating and/or cooling system is to be installed, and a heating or cooling system is being simulated only to meet the requirements described in Section G3.1-10 HVAC Systems proposed column c and d, heating and/or cooling system fans shall simulated to be cycled ON and OFF to meet heating and cooling loads during occupied hours.  
  * [4-5](section4/4-5.md): HVAC fans shall remain on during unoccupied hours in spaces that have health and safety mandated minimum ventilation requirements during unoccupied hours.  
  * [4-6](section4/4-6.md): HVAC fans in the proposed design model shall remain on during unoccupied hours in systems primarily serving computer rooms.  
  * [4-8](section4/4-8.md): Schedules may be allowed to differ between proposed design and baseline building design when necessary to model nonstandard efficiency measures, such as automatic natural ventilation controls, automatic demand control ventilation controls. In no case shall schedules differ where the controls are manual.  
  * [4-10](section4/4-10.md): Schedules for HVAC fans that provide outdoor air for ventilation shall be cycled ON and OFF to meet heating and cooling loads during unoccupied hours excluding HVAC systems that meet Table G3.1-4 Schedules for the proposed building exceptions #s 2 and 3.  
  * [4-11](section4/4-11.md): Fan schedules shall be modeled identically in the baseline and proposed unless Table G3.1 Section 4 baseline exceptions are applicable. Fan Schedules may be allowed to differ when Section 4 Baseline Column Exceptions #1, #2 Or #3 are applicable.
  * [4-12](section4/4-12.md): For Systems 6 and 8, only the terminal-unit fan and reheat coil shall be energized to meet heating set point during unoccupied hours.  
  * [4-15](section4/4-15.md): Schedules for HVAC fans that provide outdoor air for ventilation shall run continuously whenever spaces are occupied in the B_RMD. 
  * [4-16](section4/4-16.md): Where no heating and/or cooling system is to be installed, and a heating or cooling system is being simulated only to meet the requirements described in this table, heating and/or cooling system fans shall not be simulated as running continuously during occupied hours but shall be cycled ON and OFF to meet heating and cooling loads during all hours in the B_RMD.  
  * [4-17](section4/4-17.md): HVAC fans shall remain on during  unoccupied hours in spaces that have health and safety mandated minimum ventilation requirements during unoccupied hours in the B_RMD.  
  * [4-18](section4/4-18.md): HVAC fans in the baseline design model shall remain on during unoccupied hours in systems primarily serving computer rooms in the B_RMD.  
  * [4-19](section4/4-19.md): Schedules for HVAC fans in the baseline design model that provide outdoor air for ventilation shall be cycled ON and OFF to meet heating and cooling loads during unoccupied hours excluding HVAC systems that meet Table G3.1-4 Schedules per the proposed column exceptions #s 2 and 3.  

## Section 5 - Building Envelope
  * [5-2](section5/Rule5-2.md): Orientation is the same in user model and proposed model  
  * [5-3](section5/Rule5-3.md): Baseline building must be modeled so that it doesn't shade itself  
  * [5-4](section5/Rule5-4.md): Baseline roof assemblies must conform with assemblies detailed in Appendix A ( Above-grade walls—Steel-framed A2.2) 
  * [5-5](section5/Rule5-5.md): Baseline roof assemblies must match the appropriate assembly maximum U-factors in Tables G3.4-1 through G3.4-8.  
  * [5-6](section5/Rule5-6.md): Building above-grade opaque surface U-factors must be modeled in proposed design as designed.  
  * [5-7](section5/Rule5-7.md): Baseline below-grade walls shall conform with assemblies detailed in Appendix A Concrete block, A4) 
  * [5-8](section5/Rule5-8.md): Baseline below-grade walls shall match the appropriate assembly maximum C-factors in Tables G3.4-1 through G3.4-8
  * [5-9](section5/Rule5-9.md): Below-grade wall C-factor must be the same in the proposed model as in the user model  
  * [5-10](section5/Rule5-10.md): Baseline above-grade wall assemblies must conform with assemblies detailed in  Appendix A (Steel-framed A3.3) 
  * [5-11](section5/Rule5-11.md): Baseline above-grade wall assemblies must match the appropriate assembly maximum U-factors in Tables G3.4-1 through G3.4-8
  * [5-12](section5/Rule5-12.md): Baseline floor assemblies must conform with assemblies detailed in Appendix A (Floors—Steel-joist (A5.3)) 
  * [5-13](section5/Rule5-13.md): Baseline floor assemblies must  match the appropriate assembly maximum U-factors in Tables G3.4-1 through G3.4-9
  * [5-14](section5/Rule5-14.md): Baseline slab-on-grade assemblies must conform with assemblies detailed in Appendix A ( Slab-on-grade floors shall match the F-factor for unheated slabs from the same tables (A6).) 
  * [5-15](section5/Rule5-15.md): Baseline slab-on-grade floor assemblies must match the appropriate assembly maximum F-factors in Tables G3.4-1 through G3.4-9
  * [5-16](section5/Rule5-16.md): Slab-on-grade F-factor in the proposed design must be modeled as-designed
  * [5-17](section5/Rule5-17.md): Opaque surfaces that are not regulated (not part of opaque building envelope) must be modeled the same in the baseline as in the proposed design.
  * [5-18](section5/Rule5-18.md): For building area types included in Table G3.1.1-1, vertical fenestration areas for new buildings and additions shall equal that in Table G3.1.1-1 based on the area of gross above-grade walls that separate conditioned spaces and semi-heated spaces from the exterior
  * [5-19](section5/Rule5-19.md): For building areas not shown in Table G3.1.1-1, vertical fenestration areas for new buildings and additions shall equal that in the proposed design or 40% of gross above-grade wall area, whichever is smaller. 
  * [5-21](section5/Rule5-21.md): The vertical fenestration shall be distributed on each face of the building in the same proportion as in the proposed design.  
  * [5-22](section5/Rule5-22.md): The baseline fenestration area for an existing building shall equal the existing fenestration area prior to the proposed work.
  * [5-23](section5/Rule5-23.md): Subsurface area in the proposed design must be as-designed.  
  * [5-24](section5/Rule5-24.md): Vertical fenestration U-factors for residential, non-residential and semi-heated spaces in the baseline model must match the appropriate requirements in Table G3.4-1 through G3.4-8 for the appropriate WWR in the baseline RMD.  
  * [5-25](section5/Rule5-25.md): Fenestration (window and skylight) U-factors in the proposed model must match the user model.  
  * [5-27](section5/Rule5-27.md): Fenestration (window and skylight) SHGC in the proposed model must match the user model.  
  * [5-28](section5/Rule5-28.md): Subsurface that is not regulated (not part of building envelope) must be modeled with the same area, U-factor and SHGC in the baseline as in the proposed design.
  * [5-29](section5/Rule5-29.md): Baseline fenestration shall be assumed to be flush with the exterior wall, and no shading projections shall be modeled.  
  * [5-30](section5/Rule5-30.md): Proposed fenestration has the same shading projections as the user model.
  * [5-31](section5/Rule5-31.md): Manual fenestration shading devices, such as blinds or shades, shall be modeled or not modeled the same as in the baseline building design.
  * [5-33](section5/Rule5-33.md): Automatically controlled fenestration shading devices must be modeled in the proposed design the same as in user model.  
  * [5-34](section5/Rule5-34.md): If skylight area in the proposed design is 3% or less of the roof surface, the skylight area in baseline shall be equal to that in the proposed design.  
  * [5-35](section5/Rule5-35.md): If the skylight area of the proposed design is greater than 3%, baseline skylight area shall be decreased by an identical percentage in all roof components in which skylights are located to reach 3%.  
  * [5-36](section5/Rule5-36.md): Skylight area must be allocated to surfaces in the same proportion in the baseline as in the proposed design; Skylight orientation and tilt shall be the same as in the proposed design.  
  * [5-38](section5/Rule5-38.md): Skylight SHGC properties shall match the appropriate requirements in Tables G3.4-1 through G3.4-8 using the value and the applicable skylight percentage.
  * [5-37](section5/Rule5-37.md): Skylight U-factors for residential, non-residential and semi-heated spaces in the baseline model must match the appropriate requirements in Table G3.4-1 through G3.4-8.  
  * [5-39](section5/Rule5-39.md): Automatically controlled dynamic glazing may be modeled. Manually controlled dynamic glazing shall use the average of the minimum and maximum SHGC and VT.  
  * [5-40](section5/Rule5-40.md): The baseline roof surfaces shall be modeled using a thermal emittance of 0.9.
  * [5-41](section5/Rule5-41.md): The proposed roof surfaces shall be modeled using the same thermal emittance as in the user model.  
  * [5-42](section5/Rule5-42.md): The baseline roof surfaces shall be modeled using a solar reflectance of 0.30.  
  * [5-43](section5/Rule5-43.md): The proposed roof surfaces shall be modeled using the same solar reflectance as in the user model.  
  * [5-44](section5/Rule5-44.md): The infiltration modeling method in the baseline includes adjustment for weather and building operation.  
  * [5-45](section5/Rule5-45.md): The infiltration schedules are the same in the proposed RMD as in the baseline RMD.  
  * [5-46](section5/Rule5-46.md): The infiltration shall be modeled using the same methodology and adjustments for weather and building operation in both the proposed design and the baseline building design.  
  * [5-48](section5/Rule5-48.md): The air leakage rate in unconditioned and unenclosed spaces must be the same the baseline and proposed design.  
  * [5-50](section5/Rule5-50.md): Shading by adjacent structures and terrain is the same in the baseline and proposed.  
  * [5-51](section5/Rule5-51.md): Shading by adjacent structures and terrain is the same in the proposed design as in user model.  
  * [5-52](section5/Rule5-52.md): It is acceptable to use either an annual average ground temperature or monthly average ground temperatures for calculation of heat loss through basement floors.

## Section 6 - Lighting
  * [6-1](section6/Rule6-1.md): Proposed building interior lighting power shall not exceel total interior lighting power allowance determined using either G3.7 or G3.8
  * [6-2](section6/Rule6-2.md): Spaces in proposed building with hardwired lighting, including Hotel/Motel Guest Rooms, Dormitory Living Quarters interior lighting power >= Table 9.6.1. and Interior lighting power for  'Dwelling Units' space type in the proposed building shall be >= 0.60 W/ft2.
  * [6-3](section6/Rule6-3.md): Where a complete lighting system exists, the actual lighting power for each thermal block shall be used in the model.
  * [6-4](section6/Rule6-4.md): Where a complete lighting system exists and where a lighting system has been designed and submitted with design documents, the baseline LPD is equal to expected value in Table G3.7.  
  * [6-5](section6/Rule6-5.md): Baseline building is modeled with automatic shutoff controls in buildings >5000 ft2
  * [6-6](section6/Rule6-6.md): Baseline building is not modeled with daylighting control
  * [6-7](section6/Rule6-7.md): Proposed building is modeled with daylighting controls
  * [6-8](section6/Rule6-8.md): Proposed building is modeled with additional occupancy sensor controls using occupancy sensor schedule reduction factors specified in Table G3.7.  
  * [6-9](section6/Rule6-9.md): Proposed building is modeled with other programmable lighting controls through a 10% schedule reduction in buildings less than 5,000sq.ft.  

## Section 10 - Airside systems
  * [10-1](section10/10-1.md): The proposed design includes humidification and the baseline building design has been modeled with adiabatic humidification if proposed design does not comply with 90.1-2019 Section 6.5.2.4 and non-adiabatic humidification otherwise.
  * [10-3](section10/10-3.md): For systems serving computer rooms, the baseline building design shall not have reheat for the purpose of dehumidification.
  * [10-4](section10/10-4.md): Baseline HVAC systems using fossil fuel shall be modeled using natural gas. Except where natural gas is not available for the proposed building site, propane shall be used as the heating fuel.
  * [10-6](section10/10-6.md): For HVAC systems designed, mechanical cooling equipment efficiencies shall be adjusted to remove the supply fan energy from the efficiency rating.
  * [10-7](section10/10-7.md): Baseline shall be modeled with the COPnfcooling HVAC system efficiency per Tables G3.5.1-G3.5.6.  Where multiple HVAC zones or residential spaces are combined into a single thermal block the cooling efficiencies (for baseline HVAC System Types 3 and 4) shall be based on the  equipment capacity of the thermal block divided by the number of HVAC zones or residential spaces.
  * [10-9](section10/10-9.md): Where multiple HVAC zones or residential spaces are combined into a single thermal block, baseline HVAC System Types 5 or 6 efficiencies shall be based on the cooling equipment capacity of a single floor.
  * [10-10](section10/10-10.md): Where no heating system exists or no heating system has been submitted with design documents, the proposed building system type shall be the same system as modeled in the baseline building design and shall comply with but not exceed the requirements of Section 6.
  * [10-11](section10/10-11.md): Except for spaces with baseline system 9 or 10, if no cooling system exists or no cooling system has been submitted with design documents, the proposed building cooling system type shall be the same as modeled in the baseline building design and shall comply with the requirements of Section 6.
  * [10-13A](section10/10-13A.md): For HVAC systems designed, mechanical heating equipment efficiencies shall be adjusted to remove the supply fan energy from the efficiency rating.
  * [10-13B](section10/10-13B.md): For proposed HVAC systems designed, mechanical preheating equipment efficiencies shall be adjusted to remove the supply fan energy from the efficiency rating.

## Section 12 - Receptacles and Other Loads
  * [12-1](section12/Rule12-1.md): Number of spaces modeled in User RMD and Baseline RMD are the same
  * [12-2](section12/Rule12-2.md): Number of spaces modeled in User RMD and Proposed RMD are the same
  * [12-3](section12/Rule12-3.md): User RMD Space Name in Proposed RMD? 

## Section 15 - Distribution Transformers
  * [15-1](section15/Rule15-1.md): Number of transformers modeled in User RMD and Baseline RMD are the same
  * [15-2](section15/Rule15-2.md): Number of transformers modeled in User RMD and Baseline RMD are the same
  * [15-3](section15/Rule15-3.md): User RMD transformer Name in Proposed RMD  
  * [15-4](section15/Rule15-4.md): User RMD transformer Name in Baseline RMD   
  * [15-5](section15/Rule15-5.md): Transformer efficiency reported in Baseline RMD equals Table 8.4.4  
  * [15-6](section15/Rule15-6.md): Transformer efficiency reported in User RMD equals Table 8.4.4.
  
## Section 16 - Elevators

## Section 17 - Refrigeration

## Section 18 - Air Side

## Section 19 - Air Side Baseline HVAC System
  * [19-1](section19/Rule19-1.md): HVAC system coil capacities for the baseline building design shall be oversized by 15% for cooling and 25% for heating.
  * [19-2](section19/Rule19-2.md): Baseline building plant capacities shall be based on coincident loads.
  * [19-4](section19/Rule19-4.md): For baseline cooling sizing runs in residential dwelling units, the infiltration, occupants, lighting, gas and electricity using equipment hourly schedule shall be the same as the most used hourly weekday schedule from the annual simulation.
  * [19-5](section19/Rule19-5.md): Unmet load hours for the proposed design shall not exceed 300 (of the 8760 hours simulated).
  * [19-6](section19/Rule19-6.md): Unmet load hours for the baseline design shall not exceed 300 (of the 8760 hours simulated).
  * [19-7](section19/Rule19-7.md): Minimum ventilation system outdoor air intake flow shall be the same for the proposed design and baseline building design except when any of the 4 exceptions defined in Section G3.1.2.5 are met.
  * [19-8](section19/Rule19-8.md): Demand control ventilation is modeled in the baseline design in systems with outdoor air capacity greater than 3000 cfm serving areas with an average occupant design capacity greater than 100 people per 1000 ft^2.
  * [19-9](section19/Rule19-9.md): Air economizers shall not be included in baseline HVAC Systems 1, 2, 9, and 10.
  * [19-10](section19/Rule19-10.md): Air economizers shall be included in baseline HVAC Systems 3 through 8, and 11, 12, and 13 based on climate as specified in Section G3.1.2.6 with exceptions.
  * [19-11](section19/Rule19-11.md): For systems that serve computer rooms, if the  baseline system is HVAC System 11, it shall include an integrated fluid economizer meeting the requirements of Section 6.5.1.2 in the baseline building design.
  * [19-12](section19/Rule19-12.md): The baseline system economizer high-limit shutoff shall be a dry-bulb fixed switch with set-point temperatures in accordance with the values in Table G3.1.2.7.
  * [19-13](section19/Rule19-13.md): For baseline system types 1-8 and 11-13, system design supply airflow rates shall be based on a supply-air-to-room temperature set-point difference of 20°F or the minimum outdoor airflow rate, or the airflow rate required to comply with applicable codes or accreditation standards, whichever is greater. For systems with multiple zone thermostat setpoints, use the design set point that will result in the lowest supply air cooling set point or highest supply air heating set point.
  * [19-14](section19/Rule19-14.md): For baseline system types 1-8 and 11-13, if return or relief fans are specified in the proposed design, the baseline building design shall also be modeled with fans serving the same functions and sized for the baseline system supply fan air quantity less the minimum outdoor air, or 90% of the supply fan air quantity, whichever is larger.
  * [19-15](section19/Rule19-15.md): For baseline system types 9 & 10, the system design supply airflow rates shall be based on the temperature difference between a supply air temperature set point of 105°F and the design space-heating temperature set point, the minimum outdoor airflow rate, or the airflow rate required to comply with applicable codes or accreditation standards, whichever is greater.
  * [19-16](section19/Rule19-16.md): For zones served by baseline system types 9 & 10, if the proposed design includes a fan or fans sized and controlled to provide non-mechanical cooling, the baseline building design shall include a separate fan to provide nonmechanical cooling, sized and controlled the same as the proposed design.
  * [19-17](section19/Rule19-17.md): For baseline system 1 and 2, the total fan electrical power (Pfan) for supply, return, exhaust, and relief shall be = CFMs × 0.3, where, CFMs = the baseline system maximum design supply fan airflow rate, cfm.
  * [19-19](section19/Rule19-19.md): For baseline systems 9 and 10 the system fan electrical power (Pfan) for supply, return, exhaust, and relief shall be  CFMs × 0.3, where, CFMs = the baseline system maximum design supply fan airflow rate, cfm. If modeling a non-mechanical cooling fan is required by Section G3.1.2.8.2, there is a fan power allowance of Pfan = CFMnmc × 0.054, where, CFMnmc = the baseline non-mechanical cooling fan airflow, cfm for the non-mechanical cooling.
  * [19-20](section19/Rule19-20.md): The calculated system fan power shall be distributed to supply, return, exhaust, and relief fans in the same proportion as the proposed design.
  * [19-21](section19/Rule19-21.md): Baseline systems with >= 5,000 CFM supply air and >= 70 %OA shall have energy recovery modeled in the baseline design model (this RDS does not check the modeled value for the enthalpy recovery ratio).
  * [19-22](section19/Rule19-22.md): Baseline systems modeled with exhaust air energy recovery shall allow bypass or control heat recovery system to permit air economizer operation.
  * [19-24](section19/Rule19-24.md): Schedules for HVAC fans that provide outdoor air for ventilation shall run continuously whenever spaces are occupied in the proposed design.
  * [19-25](section19/Rule19-25.md): Schedules for HVAC fans that provide outdoor air for ventilation shall run continuously whenever spaces are occupied in the baseline design.
  * [19-26](section19/Rule19-26.md): HVAC fans shall remain on during unoccupied hours in spaces that have health and safety mandated minimum ventilation requirements during unoccupied hours in the proposed design.
  * [19-27](section19/Rule19-27.md): HVAC fans shall remain on during unoccupied hours in spaces that have health and safety mandated minimum ventilation requirements during unoccupied hours in the baseline design.
  * [19-28](section19/Rule19-28.md): Schedules for HVAC fans that provide outdoor air for ventilation in the proposed design shall be cycled ON and OFF to meet heating and cooling loads during unoccupied hours excluding HVAC systems that meet Table G3.1-4 Schedules for the proposed building exceptions #s 2 and 3.
  * [19-29](section19/Rule19-29.md): Schedules for HVAC fans in the baseline design model that provide outdoor air for ventilation shall be cycled ON and OFF to meet heating and cooling loads during unoccupied hours excluding HVAC systems that meet Table G3.1-4 Schedules per the proposed column exceptions #s 2 and 3.
  * [19-30](section19/Rule19-30.md): For Systems 6 and 8, only the terminal-unit fan and reheat coil shall be energized to meet heating set point during unoccupied hours in the baseline design.
  * [19-31](section19/Rule19-31.md): HVAC fans in the proposed design model shall remain on during unoccupied hours in systems primarily serving computer rooms.
  * [19-32](section19/Rule19-32.md): HVAC fans in the baseline design model shall remain on during unoccupied hours in systems primarily serving computer rooms in the B_RMR.
  * [19-33](section19/Rule19-33.md): Where no heating and/or cooling system is to be installed, and a heating or cooling system is being simulated only to meet the requirements described in Section G3.1-10 HVAC Systems proposed column c and d, heating and/or cooling system fans shall simulated to be cycled ON and OFF to meet heating and cooling loads during occupied hours in the proposed design.
  * [19-34](section19/Rule19-34.md): Where no heating and/or cooling system is to be installed, and a heating or cooling system is being simulated only to meet the requirements described in this table, heating and/or cooling system fans shall not be simulated as running continuously during occupied hours but shall be cycled ON and OFF to meet heating and cooling loads during all hours in the baseline design.
  * [19-35](section19/Rule19-35.md): For baseline systems serving only laboratory spaces that are prohibited from recirculating return air by code or accreditation standards, the baseline system shall be modeled as 100% outdoor air. Rule only applies when baseline outdoor air CFM is modeled as greater than proposed design outdoor air CFM.

## Section 21 - Central Heating Hot Water Systems
  * [21-1](section21/Rule21-1.md): For systems using purchased hot water or steam, the heating source shall be modeled as purchased hot water or steam in both the proposed design and baseline building design. If any system in the proposed design uses purchased hot water or steam, all baseline systems with hot water coils shall use the same type of purchased hot water or steam.
  * [21-2](section21/Rule21-2.md): For purchased HW/steam in the proposed model, the baseline shall have the same number of pumps as proposed
  * [21-3](section21/Rule21-3.md): Heating hot water plant capacity shall be based on coincident loads.  
  * [21-4](section21/Rule21-4.md): When baseline building does not use purchased heat, baseline systems 1,5,7,11,12 shall be modeled with natural draft boilers.
  * [21-5](section21/Rule21-5.md): The baseline building design boiler plant shall be modeled as having a single boiler if the baseline building design plant serves a conditioned floor area of 15,000sq.ft. or less, and as having two equally sized boilers for plants serving more than 15,000sq.ft.
  * [21-6](section21/Rule21-6.md): When baseline building includes two boilers each shall stage as required by load.  
  * [21-7](section21/Rule21-7.md): When baseline building requires boilers, systems 1,5,7,11 and 12 - Model HWST = 180F and return design temp = 130F.
  * [21-9](section21/Rule21-9.md): When baseline building includes boilers, Hot Water Pump Power = 19W/gpm.  
  * [21-10](section21/Rule21-10.md): When the building is modeled with HHW plant (served by either boiler(s) or purchased hot water/steam), the hot water pump shall be modeled as riding the pump curve if the hot water system serves less than 120,000 ft^2 otherwise it shall be modeled with a VFD.  
  * [21-11](section21/Rule21-11.md): When the system uses boilers the hot water system shall be modeled as primary only.  
  * [21-12](section21/Rule21-12.md): When the system uses boilers the hot water system shall be modeled with continuous variable flow.  
  * [21-13](section21/Rule21-13.md): When the system uses boilers the hot water system shall be modeled with a minimum turndown ratio of 0.25.
  * [21-14](section21/Rule21-14.md): When the baseline building is modeled with a hot water plant, served by purchased HW system, hot water supply temperature reset is not modeled.
  * [21-15](section21/Rule21-15.md): When the baseline building is modeled with a hot water plant, served by purchased HW system, the hot water pump power shall be 14 W/gpm.
  * [21-16](section21/Rule21-16.md): Baseline shall have only one heating hot water plant.
  * [21-17](section21/Rule21-17.md): All boilers in the baseline building design shall be modeled at the minimum efficiency levels, both part load and full load, in accordance with Tables G3.5.6.
  * [21-18](section21/Rule21-18.md): For baseline building, fossil fuel systems shall be modeled using natural gas as their fuel source.

## Section 22 - Central Chilled Water Systems
  * [22-1](section22/Rule22-1.md): Baseline chilled water design supply temperature shall be modeled at 44F.  
  * [22-2](section22/Rule22-2.md): Baseline chilled water design supply temperature shall be modeled at 44F. 
  * [22-3](section22/Rule22-3.md): For Baseline chilled water loop that is not purchased cooling, chilled-water supply temperature shall be reset based on outdoor dry-bulb temperature if loop does not serve any Baseline System Type-11.
  * [22-4](section22/Rule22-4.md): For Baseline chilled water loop that is not purchased chilled water and does not serve any computer room HVAC systems, chilled-water supply temperature shall be reset using the following schedule: 44F at outdoor dry-bulb temperature of 80F and above, 54F at 60F and below, and ramped linearly between 44F and 54F at temperature between 80F and 60F.
  * [22-5](section22/Rule22-5.md): For Baseline chilled water loop that is not purchased chilled water and serves computer room HVAC systems (System Type-11), chilled-water supply temperature shall be reset higher based on the HVAC system requiring the most cooling.  
  * [22-6](section22/Rule22-6.md): For Baseline chilled water loop that is not purchased chilled water and serves computer room HVAC systems (System Type-11), The maximum reset chilled-water supply temperature shall be 54F.
  * [22-7](section22/Rule22-7.md): Baseline chilled water system that does not use purchased chilled water shall be modeled as primary/secondary systems.
  * [22-8](section22/Rule22-8.md): For Baseline chilled water system with cooling capacity of 300 tons or more, the secondary pump shall be modeled with variable-speed drives.
  * [22-9](section22/Rule22-9.md): For Baseline chilled water system with cooling capacity of 300 tons or more, the secondary loop shall be modeled with a minimum flow of 25% of the design flow rate. 
  * [22-10](section22/Rule22-10.md): For Baseline chilled water system with cooling capacity less than 300ton, the secondary pump shall be modeled as riding the pump curve. For Baseline chilled water system with cooling capacity of 300 tons or more, the secondary pump shall be modeled with variable-speed drives. 
  * [22-11](section22/Rule22-11.md): For Baseline chilled-water system that does not use purchased chilled water, variable-flow secondary pump shall be modeled as 13W/gpm at design conditions. 
  * [22-12](section22/Rule22-12.md): The heat rejection system shall be a single loop, modeled with a single cooling tower.
  * [22-13](section22/Rule22-13.md): The baseline heat rejection loop shall be an axial-fan open circuit cooling tower.
  * [22-14](section22/Rule22-14.md): The baseline heat-rejection device shall have a design temperature rise of 10°F. 
  * [22-15](section22/Rule22-15.md): Heat Rejection Device Approach calaculated correctly (T/F), Approach = 25.72-(0.24*WB).
  * [22-16](section22/Rule22-16.md): The baseline condenser-water design supply temperature shall be calculated using the cooling tower approach to the 0.4% evaporation design wet-bulb temperature, valid for wet-bulbs from 55°F to 90°F. 
  * [22-17](section22/Rule22-17.md): The baseline heat rejection device shall have an efficiency of 38.2 gpm/hp.
  * [22-18](section22/Rule22-18.md): The baseline heat rejection device shall be modeled with variable speed fan control.
  * [22-19](section22/Rule22-19.md): The tower shall be controlled to maintain a leaving water temperature, where weather permits.
  * [22-20](section22/Rule22-20.md): The baseline minimum condenser water reset temperature is per Table G3.1.3.11.
  * [22-21](section22/Rule22-21.md): The baseline building design’s chiller plant shall be modeled with chillers having the type as indicated in Table G3.1.3.7 as a function of building peak cooling load. 
  * [22-22](section22/Rule22-22.md): The baseline chiller efficiencies shall be modeled at the minimum efficiency levels for full load, in accordance with Tables G3.5.3.
  * [22-23](section22/Rule22-23.md): Each baseline chiller shall be modeled with separate chilled water pump interlocked to operate with the associated chiller.
  * [22-24](section22/Rule22-24.md): For baseline chilled-water systems served by chiller(s), the primary pump shall be modeled as constant volume. 
  * [22-25](section22/Rule22-25.md): For chilled-water systems served by chiller(s) and does not serve baseline System-11, the baseline building constant-volume primary pump power shall be modeled as 9 W/gpm. 
  * [22-26](section22/Rule22-26.md): For chilled-water systems served by chiller(s) and serves baseline System-11, the baseline building constant-volume primary pump power shall be modeled as 12 W/gpm. 
  * [22-27](section22/Rule22-27.md): Each baseline chiller shall be modeled with separate condenser-water pump interlocked to operate with the associated chiller.
  * [22-29](section22/Rule22-29.md): For chilled-water systems served by chiller(s) and does not serve baseline System-11, condenser-water pump power shall be 19 W/gpm. 
  * [22-30](section22/Rule22-30.md): For chilled-water systems served by chiller(s) and serves baseline System-11, condenser-water pump power shall be 22 W/gpm. 
  * [22-31](section22/Rule22-31.md): The baseline building design’s chiller plant shall be modeled with chillers having the number as indicated in Table G3.1.3.7 as a function of building peak cooling load. 
  * [22-32](section22/Rule22-32.md): The baseline chiller efficiencies shall be modeled at the minimum efficiency levels for part load, in accordance with Tables G3.5.3.
  * [22-33](section22/Rule22-33.md): Baseline chilled water system that does not use purchased chilled water must only have no more than one CHW plant.
  * [22-34](section22/Rule22-34.md): For baseline cooling chilled water plant that is served by chiller(s), the capacity shall be based on coincident loads.
  * [22-35](section22/Rule22-35.md): Baseline systems served by purchased chilled water shall not be modeled with chilled water reset.
  * [22-36](section22/Rule22-36.md): Baseline chilled water system that does not use purchased chilled water shall be modeled with constant flow primary loop and variable flow secondary loop.
  * [22-37](section22/Rule22-37.md): Baseline systems served by purchased chilled water loop shall be modeled with a distribution pump with a variable speed drive.
  * [22-38](section22/Rule22-38.md): Baseline systems served by purchased chilled water loop shall have a minimum flow setpoint of 25%.
  * [22-39](section22/Rule22-39.md): Baseline systems served by purchased chilled water loop shall be modeled with a distribution pump whose pump power is 16W/gpm.
  * [22-40](section22/Rule22-40.md): For systems using purchased chilled water, the cooling source shall be modeled as purchased chilled water in both the proposed design and baseline building design. If any system in the proposed design uses purchased chilled water, all baseline systems with chilled water coils shall use purchased chilled water. On-site chillers and direct expansion equipment shall not be modeled in the baseline building design.
  * [22-41](section22/Rule22-41.md): Purchased CHW systems must be modeled with only one external fluid loop in the baseline design.

## Section 23 - Chilled Water Systems and Condenser Water Systems
  * [23-2](section23/Rule23-2.md): For baseline systems 5-8 and 11, the SAT is reset higher by 5F under minimum cooling load conditions.
  * [23-3](section23/Rule23-3.md): System 5, 6, 7 and 8 minimum volume setpoint shall be 30% of zone peak airflow, minimum outdoor airflow, or rate required to comply with minimum accreditation standards whichever is larger.
  * [23-6](section23/Rule23-6.md): For baseline systems 6 and 8, Fans in parallel VAV fan-powered boxes shall be sized for 50% of the peak design primary air (from the VAV air-handling unit) flow rate and shall be modeled with 0.35 W/cfm fan power.
  * [23-7](section23/Rule23-7.md): Systems 6&8: Supply air temperature setpoint shall be constant at the design condition.
  * [23-8](section23/Rule23-8.md): System 5-8 and 11 - part load VAV fan power shall be modeled using either method 1 or 2 in Table G3.1.3.15. This rule will only validate data points from Method-1 Part-load Fan Power Data. However, both methods are equivalent. When modeling inputs are based on Method 2, values should be converted to Method 1 when writing to RMD.
  * [23-16](section23/Rule23-16.md): Systems 5 - 8, the baseline system shall be modeled with preheat coils controlled to a fixed set point 20F less than the design room heating temperature setpoint.
