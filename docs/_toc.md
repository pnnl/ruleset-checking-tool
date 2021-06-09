# Rule Definition Development Strategy

### Introduction
The following documentation provides a technical description of ASHRAE 90.1-2019 Appendix G rules as defined in the ASHRAE 229P Test Case Descriptions (TCD) based on the construct of the Ruleset Checking Tool (RCT) Rule Definitions.  This document serves as a bridge between the ASHRAE 229 TCDs, which are in the form of the ruleset, and the RCT Rule Definitions, which are in the form of Python classes.  Each Rule Definition Development Strategy document seeks to describe a TCD Rule in pseudocode that can be understood by ASHRAE 90.1 professionals and Python developers alike.  The documents are organized based on 90.1 section and TCD Rule.  Front matter is included that describes any standard conventions, nomenclature or use of pseudocode functions.  The purpose of this document is not to provide direct Python code, rather to convey the logic necessary to develop code that meets the intent of the 229 TCDs.

## Reference Material
  * [Rule Template](_rule_template.md): Template file for creating a new Rule Definition Development Strategy document
  * [Functions](_functions.md): A list of functions used within the Rule Definition Development Strategy documents
  * [Ruleset Functions](_ruleset_functions.md): A list of commonly used functions that are specific to a ruleset.

## Data Tables
  * [8.4.4](data_tables/Table8-4-4.md): Minimum Nominal Efficiency Levels for Low-Voltage Dry-Type Distribution Transformers  
  * [G3.1.1-1](data_tables/Table3-1-1-1.md): Baseline Building Vertical Fenestration Percentage of Gross Above-Grade-Wall Area  
  * G3.1.1-2 [FUTURE]: Baseline Service Water-Heating System
  * G3.1.1-3 [FUTURE]: Baseline HVAC System Types
  * G3.1.1-4 [FUTURE]: Baseline System Descriptions
  * G3.1.2.6 [FUTURE]: Climate Conditions under which Economizers are Included for Comfort Cooling for Baseline Systems 3 through 8 and 11, 12, 13
  * G3.1.2.9 [FUTURE]: Baseline Fan Brake Horsepower
  * G3.1.3.7 [FUTURE]: Type and Number of Chillers
  * G3.1.3.11 [FUTURE]: Heat-Rejection Leaving Water Temperature
  * G3.1.3.15 [FUTURE]: Part-Load Performance for VAV Fan Systems
  * G3.4-1 [FUTURE]: Performance Rating Method Building Envelope Requirements for Climate Zones 0 and 1 (A,B)
  * G3.4-2 [FUTURE]: Performance Rating Method Building Envelope Requirements for Climate Zone 2 (A,B)
  * G3.4-3 [FUTURE]: Performance Rating Method Building Envelope Requirements for Climate Zone 3 (A,B,C)
  * G3.4-4 [FUTURE]: Performance Rating Method Building Envelope Requirements for Climate Zone 4 (A,B,C)   
  * G3.4-5 [FUTURE]: Performance Rating Method Building Envelope Requirements for Climate Zone 5 (A,B,C)  
  * G3.4-6 [FUTURE]: Performance Rating Method Building Envelope Requirements for Climate Zone 6 (A,B)
  * G3.4-7 [FUTURE]: Performance Rating Method Building Envelope Requirements for Climate Zone 7
  * G3.4-8 [FUTURE]: Performance Rating Method Building Envelope Requirements for Climate Zone 8  
  * G3.5.1 [FUTURE]: Performance Rating Method Air Conditioners (efficiency ratings excludeing supply fan power)
  * G3.5.2 [FUTURE]: Performance Rating Method Electrically Operated Unitary and Applied Heat Pumps -- Minimum Efficiency Requirements (efficiency ratings excluding supply fan power)
  * G3.5.3 [FUTURE]: Performance Rating Method Water Chilling Packages -- Minimum Efficiency Requirements
  * G3.5.4 [FUTURE]: Performance Rating Method Electrically Operated Packaged Terminal Air Conditioners, Packaged Terminal Heat Pumps (efficiency ratings excluding supply fan power)
  * G3.5.5 [FUTURE]: Performance Rating Method Warm-Air Furnaces and Unit Heaters
  * G3.5.6 [FUTURE]: Performance Rating Method Gas-Fired Boilers -- Minimum Efficiency Requirements
  * G3.6 [FUTURE]: Performance Rating Method Lighting Power Densities for Building Exteriors
  * G3.7 [FUTURE]: Performance Rating Method Lighting Power Density Allowances and Occupancy Sensor Reductions Using the Space-by-Space Method
  * G3.8 [FUTURE]: Performance Rating Method Lighting Power Densities Using the Building Area Method
  * G3.9.1 [FUTURE]: Performance Rating Method Motor Efficiency Requirements
  * G3.9.2 [FUTURE]: Performance Rating Method Baseline Elevator Motor
  * G3.9.3 [FUTURE]: Performance Rating Method Hydraulic Elevator Motor Efficiency
  * G3.10.1 [FUTURE]: Performance Rating Method Commercial Refrigerators and Freezers
  * G3.10.2 [FUTURE]: Performance Rating Method Commercial Refrigeration

## Section 4 - Schedules
  * 4-1 [FUTURE]: User RMR has same number of Schedules as Baseline RMR - test Annual, Week and Day Schedules    
  * 4-2 [FUTURE]: User RMR has same number of Schedules as Proposed RMR - test Annual, Week and Day Schedules    
  * 4-3 [FUTURE]: User RMR Annual Schedules have corresponding Annual Schedule in Baseline RMR (using name)    
  * 4-4 [FUTURE]: Count of assigned weeks in an Annual Sch is the same in Base RMR and User RMR     
  * 4-5 [FUTURE]: Week names are same in Baseline RMR and in User RMR  
  * 4-6 [FUTURE]: Week start month same in Baseline RMR and User RMR
  * 4-7 [FUTURE]: Week start day same in Baseline RMR and User RMR
  * 4-8 [FUTURE]: Week end month same in Baseline RMR and User RMR
  * 4-9 [FUTURE]: Week end day same in Baseline RMR and User RMR
  * 4-10 [FUTURE]: Annual schedule type same in Baseline RMR and User RMR
  * 4-11 [FUTURE]: Annual schedule name same in Proposed RMR and User RMR
  * 4-12 [FUTURE]: Annual schedule week count same in Proposed RMR and User RMR
  * 4-13 [FUTURE]: Week names same in Proposed RMR and User RMR
  * 4-14 [FUTURE]: Week start month same in Proposed RMR and User RMR
  * 4-15 [FUTURE]: Week start day same in Proposed RMR and User RMR
  * 4-16 [FUTURE]: Week end month same in Proposed RMR and User RMR
  * 4-17 [FUTURE]: Week end day same Proposed RMR and User RMR
  * 4-18 [FUTURE]: Week schedule name same in Baseline RMR and User RMR
  * 4-19 [FUTURE]: Week schedule name in User RMR is in Baseline RMR
  * 4-20 [FUTURE]: Week type in User RMR same in Baseline RMR
  * 4-21 [FUTURE]: Day name in User RMR is in Baseline RMR 
  * 4-22 [FUTURE]: Week schedule name in User RMR is in Proposed RMR
  * 4-23 [FUTURE]: Week type in User RMR same in Baseline RMR
  * 4-24 [FUTURE]: Day name in User RMR is in Proposed RMR
  * 4-25 [FUTURE]: Day schedule name in User RMR is in Baseline RMR
  * 4-26 [FUTURE]: Day type in User RMR same in Baseline RMR
  * 4-27 [FUTURE]: Day schedule value in User RMR same in Baseline RMR
  * 4-28 [FUTURE]: Day schedule name in User RMR is in Proposed RMR
  * 4-29 [FUTURE]: Day type in User RMR same in Proposed RMR
  * 4-30 [FUTURE]: Day schedule value in User RMR same in Proposed RMR

## Section 5 - Envelope
  * 5-1 [FUTURE]: Baseline building performance is the average of actual orientation and rotation at 90, 180 and 270 degrees
  * 5-2 [FUTURE]: Baseline RMR roof objects match the appropriate assembly and maximum U-factors
  * 5-3 [FUTURE]: Baseline RMR below-grade wall objects match the appropriate assembly and maximum U-factors
  * 5-4 [FUTURE]: Baseline RMR above-grade wall objects match the appropriate assembly and maximum U-factors
  * 5-5 [FUTURE]: Baseline RMR floor objects match the appropriate assembly and maximum U-factors
  * 5-6 [FUTURE]: Baseline RMR unheated slab objects match the appropriate assembly and maximum F-factors
  * [5-7-1](section5/Rule5-7-1.md): Baseline WWR should be equal to User WWR or 40%, whichever is smaller
  * [5-7-2](section5/Rule5-7-2.md): Baseline RMR WWR is distributed in the same proportion as User RMR  
  * [5-7-3](section5/Rule5-7-3.md): Baseline RMR fenestration area prior to proposed work cannot be verified  
  * [5-7-4](section5/Rule5-7-4.md): Fenestration area is equal for Proposed RMR and User RMR  
  * 5-8 [FUTURE]: Baseline RMR fenestration objects match the appropriate U-factors  
  * 5-9 [FUTURE]: Baseline RMR fenestration objects match the appropriate SHGCs 
  * 5-10-1 [FUTURE]: Baseline RMR has no exterior shading projections
  * 5-10-2 [FUTURE]: Exterior shading projections in Proposed RMR equal to User RMR
  * 5-11-1 [FUTURE]: Manual interior shading devices in Baseline RMR are equal to Proposed RMR
  * 5-11-2 [FUTURE]: Manual interior shading devices in the Proposed RMR are equal to User RMR
  * 5-11-3 [FUTURE]: Automatic interior shading devices in Proposed RMR are equal to User RMR
  * 5-12-1 [FUTURE]: Proportion of skylight area in Baseline RMR equals User RMR
  * 5-12-2 [FUTURE]: Total skylight area in Baseline RMR equals User RMR
  * 5-12-3 [FUTURE]: Total skylight area in Proposed RMR equals User RMR
  * 5-13 [FUTURE]: Baseline RMR skylight objects match the appropriate U-factors  
  * 5-14 [FUTURE]: Baseline RMR skylight objects match the appropriate SHGCs 
  * 5-15-1 [FUTURE]: Baseline RMR roof surface solar reflectance equals 0.3
  * 5-15-2 [FUTURE]: Roof solar reflectance in Proposed RMR equals User RMR
  * 5-16-1 [FUTURE]: Baseline RMR roof surface thermal emittance equals 0.9
  * 5-16-2 [FUTURE]: Roof surface thermal emmittance in Proposed RMR equals User RMR
  * 5-17-1 [FUTURE]: Baseline RMR roof reflectivity equals 0.3
  * 5-17-2 [FUTURE]: Roof reflectivity in Proposed RMR equals User RMR
  * 5-18 [FUTURE]: Infiltration air leakage rate and schedule equal for Baseline RMR and Proposed RMR
  * 5-19-1 [FUTURE]: Infiltration rate in Baseline RMR equals 1 cfm/ft2
  * 5-19-2 [FUTURE]: Infiltration rate in Proposed RMR equals 0.6 cfm/ft2
  * 5-20-1 [FUTURE]: Shading from adjacent structures and terrain is equal for Baseline RMR and Proposed RMR
  * 5-20-2 [FUTURE]: Shading from adjacent structures and terrain is equal for Proposed RMR and User RMR
  * 5-21-1 [FUTURE]: Monthly or average annual ground temperatures are equal for Baseline RMR and Proposed RMR
  * 5-21-2 [FUTURE]: Monthly or average annual ground temperatures are equal for Proposed RMR and User RMR
  * 5-22-1 [FUTURE]: Area of each opaque surface in Proposed RMR equals Baseline RMR
  * 5-22-2 [FUTURE]: Area of each opaque surface in Proposed RMR equals User RMR
  * 5-23 [FUTURE]: Manual operation schedules are equal for Baseline RMR and Proposed RMR

## Section 12 - Receptacles
  * 12-1 [FUTURE]: Number of spaces modeled in User RMR and Baseline RMR are equal
  * 12-2 [FUTURE]: Number of spaces modeled in User RMR and Proposed RMR are equal
  * 12-3 [FUTURE]: User RMR space name in Proposed RMR 
  * 12-4 [FUTURE]: User RMR space name in Baseline RMR 
  * 12-5 [FUTURE]: User RMR receptacle power matches Proposed RMR
  * 12-6 [FUTURE]: User RMR receptacle schedule matches Proposed RMR
  * 12-7 [FUTURE]: User RMR receptacle power matches Baseline RMR
  * 12-8 [FUTURE]: Receptacle control credit modeled correctly
  * 12-9 [FUTURE]: User RMR receptacle schedule matches Baseline RMR

## Section 15 - Transformers
  * [15-1](section15/Rule15-1.md): Number of transformers modeled in User RMR and Baseline RMR are the same
  * [15-2](section15/Rule15-2.md): Number of transformers modeled in User RMR and Baseline RMR are the same
  * [15-3](section15/Rule15-3.md): User RMR transformer Name in Proposed RMR  
  * [15-4](section15/Rule15-4.md): User RMR transformer Name in Baseline RMR   
  * [15-5](section15/Rule15-5.md): Transformer efficiency reported in Baseline RMR equals Table 8.4.4  
  * [15-6](section15/Rule15-6.md): Transformer efficiency reported in User RMR equals Table 8.4.4  
  * 15-7 [FUTURE]: Transformer efficiency reported in Baseline RMR equals User RMR  
  * 15-8 [FUTURE]: Transformer efficiency reported in Proposed RMR equals User RMR  
  * 15-9 [FUTURE]: Transformer capacity ratio reported in Baseline RMR equals User RMR  
  * 15-10 [FUTURE]: Transformer capacity ratio reported in Proposed RMR equals User RMR  