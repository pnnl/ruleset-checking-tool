# Rule Definition Development Strategy

### Introduction
The following documentation provides a technical description of ASHRAE 90.1-2019 Appendix G rules as defined in the ASHRAE 229P Test Case Descriptions (TCD) based on the construct of the Ruleset Checking Tool (RCT) Rule Definitions.  This document serves as a bridge between the ASHRAE 229 TCDs, which are in the form of the ruleset, and the RCT Rule Definitions, which are in the form of Python classes.  Each Rule Definition Development Strategy document seeks to describe a TCD Rule in pseudocode that can be understood by ASHRAE 90.1 professionals and Python developers alike.  The documents are organized based on 90.1 section and TCD Rule.  Front matter is included that describes any standard conventions, nomenclature or use of pseudocode functions.  The purpose of this document is not to provide direct Python code, rather to convey the logic necessary to develop code that meets the intent of the 229 TCDs.

## Reference Material
  * [Rule Template](_rule_template.md): Template file for creating a new Rule Definition Development Strategy document
  * [Functions](_functions.md): A list of functions used within the Rule Definition Development Strategy documents

## Data Tables
  * [8.4.4](data_tables/Table8-4-4.md): Minimum Nominal Efficiency Levels for Low-Voltage Dry-Type Distribution Transformers  
  * [G3.1.1-1](data_tables/Table3-1-1-1.md): Baseline Building Vertical Fenestration Percentage of Gross Above-Grade-Wall Area  

## Section 4 - Schedules
  * 4-1 [FUTURE]: User RMR has same number of Schedules as Baseline RMR - test Annual, Week and Day Schedules    
  * 4-2 [FUTURE]: User RMR has same number of Schedules as Proposed RMR - test Annual, Week and Day Schedules    
  * 4-3 [FUTURE]: User RMR Annual Schedules have corresponding Annual Schedule in Baseline RMR (using name)    
  * 4-4 [FUTURE]: Count of assigned weeks in an Annual Sch is the same in Base RMR and User RMR     
  * 4-5 [FUTURE]: Week names are same in Baseline RMR and in User RMR  

## Section 5 - Envelope
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
  * 5-10 [FUTURE]: Fenestration is flush with the exterior wall and has no shading projections

## Section 12 - Receptacles
  * 12-1 [FUTURE]: Number of spaces modeled in User RMR and Baseline RMR are equal
  * 12-2 [FUTURE]: Number of spaces modeled in User RMR and Proposed RMR are equal
  * 12-3 [FUTURE]: User RMR space name in Proposed RMR 
  * 12-4 [FUTURE]: User RMR space name in Baseline RMR 
  * 12-5 [FUTURE]: User RMR receptacle power matches Proposed RMR

## Section 15 - Transformers
  * [15-1](section15/Rule15-1.md): Number of transformers modeled in User RMR and Baseline RMR are the same
  * [15-2](section15/Rule15-2.md): Number of transformers modeled in User RMR and Baseline RMR are the same
  * [15-3](section15/Rule15-3.md): User RMR transformer Name in Proposed RMR  
  * [15-4](section15/Rule15-4.md): User RMR transformer Name in Baseline RMR   
  * [15-5](section15/Rule15-5.md): Transformer efficiency reported in Baseline RMR equals Table 8.4.4  
  * [15-6](section15/Rule15-6.md): Transformer efficiency reported in User RMR equals Table 8.4.4  
