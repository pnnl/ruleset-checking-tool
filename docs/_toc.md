# Rule Definition Development Strategy

### Introduction
The following documentation provides a technical description of ASHRAE 90.1-2019 Appendix G rules as defined in the ASHRAE 229P Test Case Descriptions (TCD) based on the construct of the Ruleset Checking Tool (RCT) Rule Definitions.  This document serves as a bridge between the ASHRAE 229 TCDs, which are in the form of the ruleset, and the RCT Rule Definitions, which are in the form of Python classes.  Each Rule Definition Development Strategy document seeks to describe a TCD Rule in pseudocode that can be understood by ASHRAE 90.1 professionals and Python developers alike.  The documents are organized based on 90.1 section and TCD Rule.  Front matter is included that describes any standard conventions, nomenclature or use of pseudocode functions.  The purpose of this document is not to provide direct Python code, rather to convey the logic necessary to develop code that meets the intent of the 229 TCDs.

### Notes on Evaluating Rules Separately for Buildings
Most rules documented in the RDS apply to data groups that are located within the *buildings* array.  It is typical that an RMR will only include a single *building* object.  In the case where multiple *building* objects exists in an RMR, each rule will be evaluated independently for each *building* object.  The following is a list of sections that will be evaluated for each *building* object in the RMR per the previous description: 
 - 5  
 - 6  
 - 12  
 - 16  
 - 17  

The *transformers* data group is handled differently, since the data group exists at the top level of the RMR schema.  For any rules related to distribution transformers, the rule is evaluated only the *transformers* list and *buildings* are ignored in the rule evaluation.  This is only applicable to the following section:
- 15  

These conventions are used in all RDS below, and the logic of evaluating rules for each *building* or *transformer* are not described in the individual RDS document.

## Reference Material
  * [Rule Template](_rule_template.md): Template file for creating a new Rule Definition Development Strategy document
  * [Functions](_functions.md): A list of functions used within the Rule Definition Development Strategy documents

## Ruleset Functions
### General functions
  * [get_lighting_status_type](ruleset_functions/get_lighting_status_type.md): This function would determine whether the space lighting status type is 1). not-yet designed or match Table 9_5_1, 2). as-designed or as-existing.  
  * [get_opaque_surface_type.md](ruleset_functions/get_opaque_surface_type.md): This function would determine whether it is a wall, ceiling or floor.  
  * [get_surface_conditioning_category.md](ruleset_functions/get_surface_conditioning_category.md): This function would cycle through each surface in  a zone and categorize it as exterior res, exterior non res, exterior mixed, semi-exterior or unregulated.  
  * [get_wwr.md](ruleset_functions/get_wwr.md): This function would determine window wall ratio for a building segment.  
  * [get_zone_conditioning_category.md](ruleset_functions/get_zone_conditioning_category.md): Determine the Zone Conditioning Category for each zone. This function would cycle through each zone in an RMR and categorize it as ‘conditioned’, 'semi-heated’, 'unenclosed' or ‘unconditioned’.  If ‘conditioned’ it will also categorize the space as ‘residential’ or ‘non-residential’.  
  * [normalize_interior_lighting_schedules.md](ruleset_functions/normalize_interior_lighting_schedules.md):This function would determine a normalized schedule for a data element in space.
  * [compare_schedules](ruleset_functions/compare_schedules.md): This function would compare two schedules and determine if they match with or without a comparison factor when applicable.  
  * [get_fuels_modeled_in_RMR.md](ruleset_functions/get_fuels_modeled_in_RMR.md): Get a list of the fuels used in the RMR.  Includes fuels used by HVAC systems including terminal units, chillers, boilers, ExternalFluidSources, and SWHs.
  * [get_primary_secondary_loops.md](ruleset_functions/get_primary_secondary_loops.md): Get the list of primary and secondary loops for CHW for a B-RMR.
  * [get_hvac_systems_5_6_serving_multiple_floors_b](ruleset_functions/get_hvac_systems_5_6_serving_multiple_floors_b.md): Get a dictionary of the system 5, 5a, 5b, 6, 6a, 6b hvac system IDs that are modeled as serving more than one floor in the baseline design model.  The dictionary consists of the hvac system ids as the key and the number of floors served as the value associated with the key.
  * [get_zones_computer_rooms](ruleset_functions/get_zones_computer_rooms.md): Returns a dictionary with the zones that have at least one computer room space associated with them in the RMR as the keys. The values associated with each key are in a list form. The list associated with each key contains the computer room floor area as the first item in the list and the total zone floor area as the second item in the list.

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
  * [are_all_terminal_types_VAV](ruleset_functions/baseline_systems/baseline_hvac_sub_functions/are_all_terminal_types_VAV.md): Returns TRUE if all of the terminal unit types input to this function are variable air volume (VAV). It returns FALSE if any of the terminal units are of a type other than variable air volume (VAV).
  * [is_hvac_sys_heating_type_furnace](ruleset_functions/baseline_systems/baseline_hvac_sub_functions/is_hvac_sys_heating_type_furnace.md): Returns TRUE if the HVAC system heating system heating type is furnace. Returns FALSE if the HVAC system heating system has anything other than furnace or if it has more than 1 heating system.
  * [is_hvac_sys_cooling_type_DX](ruleset_functions/baseline_systems/baseline_hvac_sub_functions/is_hvac_sys_cooling_type_DX.md): Returns TRUE if the HVAC system has DX cooling. Returns FALSE if the HVAC system has anything other than DX cooling or if it has more than 1 or no cooling system.
  * [is_hvac_sys_fan_sys_CV](ruleset_functions/baseline_systems/baseline_hvac_sub_functions/is_hvac_sys_fan_sys_CV.md): Returns TRUE if the HVAC system fan system is constant volume. Returns FALSE if the HVAC system fan system is anything other than constant volume.
  * [is_hvac_sys_heating_type_heat_pump](ruleset_functions/baseline_systems/baseline_hvac_sub_functions/is_hvac_sys_heating_type_heat_pump.md): Returns TRUE if the HVAC system has heat pump as the heating system type. Returns FALSE if the HVAC system has anything other than heat pump as the heating system type or if it has more than 1 heating system.
  * [is_hvac_sys_fluid_loop_attached_to_boiler](ruleset_functions/baseline_systems/baseline_hvac_sub_functions/is_hvac_sys_fluid_loop_attached_to_boiler.md): Returns TRUE if the fluid loop associated with the heating system associated with the HVAC system is attached to a boiler. Returns FALSE if this is not the case. 
  * [does_hvac_system_serve_single_zone](ruleset_functions/baseline_systems/baseline_hvac_sub_functions/does_hvac_system_serve_single_zone.md): Returns TRUE if the HVAC system serves a single zone. Returns FALSE if the HVAC system serves multiple zones. 
  * [is_hvac_sys_heating_type_fluid_loop](ruleset_functions/baseline_systems/baseline_hvac_sub_functions/is_hvac_sys_heating_type_fluid_loop.md): Returns TRUE if the HVAC system heating system heating type is fluid loop. Returns FALSE if the HVAC system heating system has anything other than fluid loop or if it has more than 1 heating system. 
  * [are_all_terminal_supplies_ducted](ruleset_functions/baseline_systems/baseline_hvac_sub_functions/are_all_terminal_supplies_ducted.md): Returns TRUE if all of the terminal supplies are ducted (i.e., is_supply_ducted = TRUE) for the list of terminal units input to the function. It returns FALSE if any of the terminal supplies are not ducted (i.e., is_supply_ducted = FALSE). 

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
  * [4-12](section4/4-12.md): For Systems 6 and 8, only the terminal-unit fan and reheat coil shall be energized to meet heating set point during unoccupied hours.  
  * [4-15](section4/4-15.md): Schedules for HVAC fans that provide outdoor air for ventilation shall run continuously whenever spaces are occupied in the B_RMR. 
  * [4-16](section4/4-16.md): Where no heating and/or cooling system is to be installed, and a heating or cooling system is being simulated only to meet the requirements described in this table, heating and/or cooling system fans shall not be simulated as running continuously during occupied hours but shall be cycled ON and OFF to meet heating and cooling loads during all hours in the B_RMR.  
  * [4-17](section4/4-17.md): HVAC fans shall remain on during  unoccupied hours in spaces that have health and safety mandated minimum ventilation requirements during unoccupied hours in the B_RMR.  
  * [4-18](section4/4-18.md): HVAC fans in the baseline design model shall remain on during unoccupied hours in systems primarily serving computer rooms in the B_RMR.  
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
  * [5-24](section5/Rule5-24.md): Vertical fenestration U-factors for residential, non-residential and semi-heated spaces in the baseline model must match the appropriate requirements in Table G3.4-1 through G3.4-8 for the appropriate WWR in the baseline RMR.  
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
  * [5-37](section5/Rule5-37.md): Skylight U-factors for residential, non-residential and semi-heated spaces in the baseline model must match the appropriate requirements in Table G3.4-1 through G3.4-8.  
  * [5-39](section5/Rule5-39.md): Automatically controlled dynamic glazing may be modeled. Manually controlled dynamic glazing shall use the average of the minimum and maximum SHGC and VT.  
  * [5-40](section5/Rule5-40.md): The baseline roof surfaces shall be modeled using a thermal emittance of 0.9.
  * [5-41](section5/Rule5-41.md): The proposed roof surfaces shall be modeled using the same thermal emittance as in the user model.  
  * [5-42](section5/Rule5-42.md): The baseline roof surfaces shall be modeled using a solar reflectance of 0.30.  
  * [5-43](section5/Rule5-43.md): The proposed roof surfaces shall be modeled using the same solar reflectance as in the user model.  
  * [5-44](section5/Rule5-44.md): The infiltration modeling method in the baseline includes adjustment for weather and building operation.  
  * [5-45](section5/Rule5-45.md): The infiltration schedules are the same in the proposed RMR as in the baseline RMR.  
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
  * [10-3](section10/10-3.md): For systems serving computer rooms, the baseline building design shall not have reheat for the purpose of dehumidification.
  * [10-6](section10/10-6.md): For HVAC systems designed, mechanical cooling equipment efficiencies shall be adjusted to remove the supply fan energy from the efficiency rating.
  * [10-7](section10/10-7.md): Baseline shall be modeled with the COPnfcooling HVAC system efficiency per Tables G3.5.1-G3.5.6.  Where multiple HVAC zones or residential spaces are combined into a single thermal block the cooling efficiencies (for baseline HVAC System Types 3 and 4) shall be based on the  equipment capacity of the thermal block divided by the number of HVAC zones or residential spaces.
  * [10-10](section10/10-10.md): Where no heating system exists or no heating system has been submitted with design documents, the proposed building system type shall be the same system as modeled in the baseline building design and shall comply with but not exceed the requirements of Section 6.
  * [10-11](section10/10-11.md): Except for spaces with baseline system 9 or 10, if no cooling system exists or no cooling system has been submitted with design documents, the proposed building cooling system type shall be the same as modeled in the baseline building design and shall comply with the requirements of Section 6.

## Section 12 - Receptacles and Other Loads
  * [12-1](section12/Rule12-1.md): Number of spaces modeled in User RMR and Baseline RMR are the same
  * [12-2](section12/Rule12-2.md): Number of spaces modeled in User RMR and Proposed RMR are the same
  * [12-3](section12/Rule12-3.md): User RMR Space Name in Proposed RMR? 

## Section 15 - Distribution Transformers
  * [15-1](section15/Rule15-1.md): Number of transformers modeled in User RMR and Baseline RMR are the same
  * [15-2](section15/Rule15-2.md): Number of transformers modeled in User RMR and Baseline RMR are the same
  * [15-3](section15/Rule15-3.md): User RMR transformer Name in Proposed RMR  
  * [15-4](section15/Rule15-4.md): User RMR transformer Name in Baseline RMR   
  * [15-5](section15/Rule15-5.md): Transformer efficiency reported in Baseline RMR equals Table 8.4.4  
  * [15-6](section15/Rule15-6.md): Transformer efficiency reported in User RMR equals Table 8.4.4   
  
## Section 16 - Elevators

## Section 17 - Refrigeration

## Section 18 - Central Chilled Water Systems

## Section 21 - Central Heating Hot Water Systems
  * [21-1](section21/Rule21-1.md): For systems using purchased hot water or steam, the heating source shall be modeled as purchased hot water or steam in both the proposed design and baseline building design. If any system in the proposed design uses purchased hot water or steam, all baseline systems with hot water coils shall use the same type of purchased hot water or steam.
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
  * [22-14](section22/Rule22-14.md): The baseline heat-rejection device shall have a design temperature rise of 10°F. 
  * [22-16](section22/Rule22-16.md): The baseline condenser-water design supply temperature shall be calculated using the cooling tower approach to the 0.4% evaporation design wet-bulb temperature, valid for wet-bulbs from 55°F to 90°F. 
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
  * [22-33](section22/Rule22-33.md): Baseline chilled water system that does not use purchased chilled water must only have no more than one CHW plant.
  * [22-34](section22/Rule22-34.md): For baseline cooling chilled water plant that is served by chiller(s), the capacity shall be based on coincident loads.
  * [22-36](section22/Rule22-36.md): Baseline chilled water system that does not use purchased chilled water shall be modeled with constant flow primary loop and variable flow secondary loop.
  * [22-37](section22/Rule22-37.md): The baseline chiller efficiencies shall be modeled at the minimum efficiency levels for part load, in accordance with Tables G3.5.3.
  * [22-40](section22/Rule22-40.md): For systems using purchased chilled water, the cooling source shall be modeled as purchased chilled water in both the proposed design and baseline building design. If any system in the proposed design uses purchased chilled water, all baseline systems with chilled water coils shall use purchased chilled water. On-site chillers and direct expansion equipment shall not be modeled in the baseline building design.

## Section 23 - Chilled Water Systems and Condenser Water Systems
  * [23-1](section23/Rule23-1.md): For baseline systems 5-8 and 11, the SAT is reset higher by 5F under minimum cooling load conditions.
  * [23-2](section23/Rule23-2.md): System 5, 6, 7 and 8 minimum volume setpoint shall be 30% of zone peak airflow, minimum outdoor airflow, or rate required to comply with minimum accreditation standards whichever is larger.
  * [23-5](section23/Rule23-5.md): For baseline systems 6 and 8, Fans in parallel VAV fan-powered boxes shall be sized for 50% of the peak design primary air (from the VAV air-handling unit) flow rate and shall be modeled with 0.35 W/cfm fan power.
  * [23-9](section23/Rule23-9.md): Systems 6&8: Supply air temperature setpoint shall be constant at the design condition.
  * [23-10](section23/Rule23-10.md): System 5-8 and 11 - part load VAV fan power shall be modeled using either method 1 or 2 in Table G3.1.3.15. This rule will only validate data points from Method-1 Part-load Fan Power Data. However, both methods are equivalent. When modeling inputs are based on Method 2, values should be converted to Method 1 when writing to RMD.
  * [23-19](section23/Rule23-19.md): Systems 5 - 8, the baseline system shall be modeled with preheat coils controlled to a fixed set point 20F less than the design room heating temperature setpoint.
