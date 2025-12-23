# Rule Definition Development Strategy

### Introduction
This documentation provides a technical description of ASHRAE Appendix G rules as defined in the ASHRAE 229P Test Case Descriptions (TCD). It serves as a bridge between the ruleset described by ASHRAE 229 TCDs and the Ruleset Checking Tool (RCT) Rule Definitions, which are presented as Python classes. The goal is to outline each rule in pseudocode that can be interpreted by professionals familiar with ASHRAE standards as well as Python developers.

The documents are organized systematically to facilitate understanding and implementation, with a focus on translating building energy standards into actionable logic. Front matter is included to clarify conventions, nomenclature, and the usage of pseudocode functions. Rather than providing direct Python code, the documentation aims to convey the conceptual structure and logic necessary for rule development.

### Notes on Evaluating Rules Separately for Buildings
Most rules documented in the RDS apply to data groups that are located within the *buildings* array.  It is typical that an RMD will only include a single *building* object.  In the case where multiple *building* objects exists in an RMD, each rule will be evaluated independently for each *building* object.  The following is a list of sections that will be evaluated for each *building* object in the RMD per the previous description: 
 - 5  
 - 6  
 - 12  
 - 16  
 - 17

These conventions are used in all RDS below, and the logic of evaluating rules for each *building* or *transformer* are not described in the individual RDS document.

## Reference Material
  * [Rule Template](_rule_template.md): Template file for creating a new Rule Definition Development Strategy document
  * [Functions](_functions.md): A list of functions used within the Rule Definition Development Strategy documents

## Rulesets
  *[ASHRAE 90.1 2019](ashrae_90p1_2019/_toc.md): ASHRAE 90.1 2019 ruleset document
