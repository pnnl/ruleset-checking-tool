# Section 1 - Rule 1-5
**Schema Version:** 0.0.29  
**Mandatory Rule:** True  
**Rule ID:** 1-5
**Rule Description:** The Performance Cost Index (PCI) shall be less than or equal to the Performance Cost Index Target (PCIt) when calculated in accordance with Standard 90.1 2019, Section 4.2.1.1
**Rule Assertion:** Options are Pass/Fail/IN_APPLICABLE     
**Appendix G Section:** Section 4.2.1.1  
**90.1 Section Reference:** None  

**Data Lookup:** None 

**Evaluation Context:** 

**Applicability Checks:** 

**Function Calls:**


## Rule Logic:
**Rule Assertion**
- Case 1: If the PCI is less than or equal to the PCIt; PASS: `if Output2019ASHRAE901.performance_cost_index <= Output2019ASHRAE901.performance_cost_index_target`
- Case 2: Else; FAIL: `else: FAIL`


**Notes/Questions:** None


**[Back](../_toc.md)**