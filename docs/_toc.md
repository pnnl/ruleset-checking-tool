# Rule Definition Development Strategy

### Introduction
The following documentation provides a technical description of ASHRAE 90.1-2019 Appendix G rules as defined in the ASHRAE 229P Test Case Descriptions (TCD) based on the construct of the Ruleset Checking Tool (RCT) Rule Definitions.  This document serves as a bridge between the ASHRAE 229 TCDs, which are in the form of the ruleset, and the RCT Rule Definitions, which are in the form of Python classes.  Each Rule Definition Development Strategy document seeks to describe a TCD Rule in pseudocode that can be understood by ASHRAE 90.1 professionals and Python developers alike.  The documents are organized based on 90.1 section and TCD Rule.  Front matter is included that describes any standard conventions, nomenclature or use of pseudocode functions.  The purpose of this document is not to provide direct Python code, rather to convey the logic necessary to develop code that meets the intent of the 229 TCDs.

## Reference Material
  * [Rule Template](_rule_template.md): Template file for creating a new Rule Definition Development Strategy document.
  * [Functions](_functions.md): A list of functions used within the Rule Definition Development Strategy documents.

## Data Tables
  * [8.4.4](data_tables/Table8-4-4.md): Minimum Nominal Efficiency Levels for Low-Voltage Dry-Type Distribution Transformers  

## Section 5 - Envelope
  * [5-7-1](section5/Rule5-7-1.md): Baseline WWR should be equal to User WWR or 40%, whichever is smaller.

## Section 15 - Transformers
  * [15-1](section15/Rule15-1.md): Number of transformers modeled in User RMR and Baseline RMR are the same
  * [15-2](section15/Rule15-2.md): Number of transformers modeled in User RMR and Baseline RMR are the same
  * [15-3](section15/Rule15-3.md): User RMR transformer Name in Proposed RMR  
  * [15-4](section15/Rule15-4.md): User RMR transformer Name in Baseline RMR   
  * [15-5](section15/Rule15-5.md): Transformer efficiency reported in Baseline RMR equals Table 8.4.4  
  * [15-6](section15/Rule15-6.md): Transformer efficiency reported in User RMR equals Table 8.4.4  
