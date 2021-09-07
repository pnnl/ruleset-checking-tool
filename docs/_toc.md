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
  * [get_lighting_status_type](ruleset_functions/get_lighting_status_type.md): This function would determine whether the space lighting status type is 1). not-yet designed or match Table 9_5_1, 2). as-designed or as-existing.  
  * [get_opaque_surface_type.md](ruleset_functions/get_opaque_surface_type.md): This function would determine whether it is a wall, ceiling or floor.  
  * [get_surface_conditioning_category.md](ruleset_functions/get_surface_conditioning_category.md): This function would cycle through each surface in  a zone and categorize it as exterior res, exterior non res, exterior mixed, semi-exterior or unregulated.  
  * [get_wwr.md](ruleset_functions/get_wwr.md): This function would determine window wall ratio for a building segment.  
  * [get_zone_conditioning_category.md](ruleset_functions/get_zone_conditioning_category.md): Determine the Zone Conditioning Category for each zone. This function would cycle through each zone in an RMR and categorize it as ‘conditioned’, 'semi-heated’, 'unenclosed' or ‘unconditioned’.  If ‘conditioned’ it will also categorize the space as ‘residential’ or ‘non-residential’.  
  * [normalize_space_schedules.md](ruleset_functions/normalize_space_schedules.md):This function would determine a normalized schedule for a data element in space.  

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

## Section 5 - Building Envelope
  * 5-1: Baseline Performance is the average of 4 rotations if vertical fenestration area per each orientation differ by more than 5%  
  * [5-2](section5/Rule5-2.md): Orientation is the same in user model and proposed model  
  * [5-3](section5/Rule5-3.md): Baseline building must be modeled so that it doesn't shade itself  
  * [5-4](section5/Rule5-4.md): Baseline roof assemblies must conform with assemblies detailed in Appendix A ( Above-grade walls—Steel-framed A2.2) 
  * 5-5: Baseline roof assemblies must match the appropriate assembly maximum U-factors in Tables G3.4-1 through G3.4-8
  * 5-6: Building enevelope U-factors must be modeled in proposed design as designed (roof, wall, windows, exterior floors)
  * [5-7](section5/Rule5-7.md): Baseline below-grade walls shall conform with assemblies detailed in Appendix A Concrete block, A4) 
  * [5-8](section5/Rule5-8.md): Baseline below-grade walls shall match the appropriate assembly maximum C-factors in Tables G3.4-1 through G3.4-8
  * 5-9: Below-grade wall C-factor must be the same in the proposed model as in the user model
  * [5-10](section5/Rule5-10.md): Baseline above-grade wall assemblies must conform with assemblies detailed in  Appendix A (Steel-framed A3.3) 
  * [5-11](section5/Rule5-11.md): Baseline above-grade wall assemblies must match the appropriate assembly maximum U-factors in Tables G3.4-1 through G3.4-8
  * [5-12](section5/Rule5-12.md): Baseline floor assemblies must conform with assemblies detailed in Appendix A (Floors—Steel-joist (A5.3)) 
  * [5-13](section5/Rule5-13.md): Baseline floor assemblies must  match the appropriate assembly maximum U-factors in Tables G3.4-1 through G3.4-9
  * [5-14](section5/Rule5-14.md): Baseline slab-on-grade assemblies must conform with assemblies detailed in Appendix A ( Slab-on-grade floors shall match the F-factor for unheated slabs from the same tables (A6).) 
  * 5-15: Baseline slab-on-grade assemblies must match the appropriate assembly maximum F-factors in Tables G3.4-1 through G3.4-9
  * 5-16: Slab-on-grade F-factor in the proposed design must be modeled as-designed
  * [5-17](section5/Rule5-17.md): Opaque surfaces that are not regulated (not part of opaque building envelope) must be modeled the same in the baseline as in the proposed design.
  * 5-18: Need to add rule for building types not included in Table G3.1.1-1
  * 5-19: The vertical fenestration shall be distributed on each face of the building in the same proportion as in the proposed design. 
  * 5-20: The vertical fenestration area for eexisiting buildings shall match the user model
  * 5-21: Need to add that fenestration area in the proposed model must be equal to user model
  * 5-22: Fenestration U-factors for residential, non-residential and semiheated spaces in the baseline model must match the appropriate requirements in Table G3.4-1 through G3.4-8 for the appropriate WWR in the baseline RMR.
  * 5-23: Fenestration (window and skylight) U-factors in the proposed  model must match the user model
  * [5-24](section5/Rule5-24.md): Fenestration for new buildings, existing buildings, and additions shall be assumed to be flush with the exterior wall, and no shading projections shall be modeled.  
  * 5-25: Fenestration (window and skylight) SHGC in the proposed  model must match the user model
  * 5-26: Baseline fenestration shall be assumed to be flush with the exterior wall, and no shading projections shall be modeled.
  * 5-27: Proposed fenestration shall have the same shading projections as the user model.
  * 5-28: Manual fenestration shading devices, such as blinds or shades, shall be modeled or not modeled the same as in the baseline building design.
  * 5-29: Automatically controlled fenestration shading devices must not be modeled in the baseline building design.
  * 5-30: Automatically controlled fenestration shading devices must be modeled in the proposed design the same as in user model.
  * 5-31: Skylight area shall be equal to that in the proposed design or 3%, whichever is smaller. If the skylight area of the proposed design is greater than 3%, baseline skylight area shall be decreased by an identical percentage in all roof components in which skylights are located to reach 3%.
  * 5-32: Skylight area in the proposed design must be the same as in user model for each roof surface
  * 5-33: Skylight U-factors for residential, non-residential and semiheated spaces in the baseline model must match the appropriate requirements in Table G3.4-1 through G3.4-8
  * [5-34](section5/Rule5-34.md): The baseline roof surfaces shall be modeled using a solar reflectance of 0.30.  
  * 5-35: Skylight U-factors for unconditioned spaces in the baseline model must match the appropriate U-factors in the user model
  * 5-36: The  baseline roof surfaces shall be modeled using a solar reflectance of 0.30.
  * 5-37: The  proposed roof surfaces shall be modeled using the same solar reflectance as in the user model.
  * 5-38: The  baseline roof surfaces shall be modeled using a thermal emittance of 0.9
  * 5-39: The  proposed roof surfaces shall be modeled using the same thermal emittance as in the user model.
  * 5-40: The  baseline roof surfaces shall be modeled using reflectivity of 0.30.
  * 5-41: The  proposed roof surfaces shall be modeled using the same reflectivity as in the user model.
  * 5-42: The  infiltration modeling method in the baseline includes for adjustment for weather and building operation.
  * 5-43: The  infiltration equivalent full load hours are the same in the proposed RMR as in the baseline RMR
  * 5-44: The  infiltration modeling method in the proposed RMR is the same as in the baseline RMR
  * 5-45: The baseline air leakage rate of the building envelope (I75Pa) at a fixed building pressure differential of 0.3 in. of water shall be 1 cfm/ft2.  The air leakage rate of the building envelope shall be converted to appropriate units for the simulation program using one of the methods in Section G3.1.1.4.  
  * 5-46: The proposed air leakage rate shall be 0.6 cfm/ft2 for buildings tested.
  * 5-47: Shading by adjacent structures and terrain is the same in the baseline and proposed.
  * 5-48: Shading by adjacent structures and terrain is the same in the proposed design as in user model.
  * 5-49: It is acceptable to use either an annual average ground temperature or monthly average ground temperatures for calculation of heat loss through basement floors.
  * 5-50: Total gross area for walls, roofs, floors, and doors, and the exposed perimeters of concrete slabs on grade  be the same in the proposed design and baseline building design.

## Section 6 - Lighting
  * [6-1](section6/Rule6-1.md): Proposed building interior lighting power should be equal to user building interior lighting power
  * [6-2](section6/Rule6-2.md): Proposed building interior lighting power shall not exceel total interior lighting power allowance determined using either G3.7 or G3.8
  * [6-3](section6/Rule6-3.md): Spaces in proposed building with hardwired lighting, including Hotel/Motel Guest Rooms, Dormitory Living Quarters interior lighting power >= Table 9.6.1. and Interior lighting power for  'Dwelling Units' space type in the proposed building shall be >= 0.60 W/ft2.
  * 6-4: Interior lighting power for  'Dwelling Units' space type in the proposed building shall be >= 0.60 W/ft2
  * 6-5: Where a complete lighting system exists, the actual lighting power for each thermal block shall be used in he model. 
  * 6-6: Where a lighting system has been designed and submitted with design documents, lighting power shall be determined in accordance with Sections 9.1.3 and 9.1.4. 
  * 6-7: Where lighting neither exists nor is submitted with design documents, lighting shall comply with but not exceed the requirements of Section 9. Lighting power shall be determined in accordance with the Building Area Method (Section 9.6.1)
  * [6-8](section6/Rule6-8.md): Baseline Interior Lighting Power Allowance for all spaces is determined based in Table G3.7 when lighting systems has been designed and submitted with design documents (space by space method is used).  
  * [6-9](section6/Rule6-9.md): Baseline building is modeled with automatic shutoff controls in buildings >5000 ft2
  * 6-10: Baseline building is modeled with occupancy sensor controls in applicable space types
  * [6-11](section6/Rule6-11.md): Baseline building is not modeled with daylighting control
  * 6-12: Proposed building is modeled with dayligthing controls
  * 6-13: Proposed building is modeled with additional occupancy sensor controls using occupancy sensor schedule reduction factors specified in Table G3.7
  * 6-14: Proposed building is modeled with other programmable lighting controls through a 10% schedule reduction
  * 6-15: Proposed building has been modeled with 1.25 * occupancy sensor reduction factor (from Table G3.7) for spaces with manual-on and partial-on occupancy sensor controls
  * 6-16: Proposed building has been modeled with 30% occupancy sensor reduction factor for 'open plan' space with individually controlled workstation lighting

## Section 12 - Receptacles and Other Loads
  * [12-1](section12/Rule12-1.md): Number of spaces modeled in User RMR and Baseline RMR are the same
  * [12-2](section12/Rule12-2.md): Number of spaces modeled in User RMR and Proposed RMR are the same
  * [12-3](section12/Rule12-3.md): User RMR Space Name in Proposed RMR? 
  * 12-4: User RMR Space Name in Baseline RMR? 
  * 12-5: User RMR Receptacle Power in Proposed RMR?
  * 12-6: User RMR Receptacle Schedule in Proposed RMR?
  * 12-7: User RMR Receptacle Power in Base RMR?
  * 12-8: Receptacle control credit modeled correctly in User RMR and Baseline RMR are the same
  * 12-9: User RMR Receptacle Schedule in Base RMR?


## Section 15 - Distribution Transformers
  * [15-1](section15/Rule15-1.md): Number of transformers modeled in User RMR and Baseline RMR are the same
  * [15-2](section15/Rule15-2.md): Number of transformers modeled in User RMR and Baseline RMR are the same
  * [15-3](section15/Rule15-3.md): User RMR transformer Name in Proposed RMR  
  * [15-4](section15/Rule15-4.md): User RMR transformer Name in Baseline RMR   
  * [15-5](section15/Rule15-5.md): Transformer efficiency reported in Baseline RMR equals Table 8.4.4  
  * [15-6](section15/Rule15-6.md): Transformer efficiency reported in User RMR equals Table 8.4.4  
  * 15-7: Transformer efficiency reported in Baseline RMR equals User RMR  
  * 15-8: Transformer efficiency reported in Proposed RMR equals User RMR  
  * 15-9: Transformer capacity ratio reported in Baseline RMR equals User RMR  
  * [15-10](section15/Rule15-10.md): Transformer capacity ratio reported in Proposed RMR equals User RMR  

## Section 16 - Elevators

## Section 17 - Refrigeration
