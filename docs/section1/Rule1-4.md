# Section 1 - Rule 1-4
**Schema Version:** 0.0.29  
**Mandatory Rule:** True  
**Rule ID:** 1-4
**Rule Description:** The performance of the proposed design is calculated in accordance with provisions of Standard 90.1-2019 Appendix G, where Performance Cost Index = Proposed building performance/Baseline building performance, where both  the  proposed  building  performance  and  the  baseline  building  performance include all end-use load components associated with the building when calculating the Performance Cost Index.
**Rule Assertion:** Options are Pass/Fail/IN_APPLICABLE     
**Appendix G Section:** G1.2.2 
**90.1 Section Reference:** None  

**Data Lookup:** None  

**Evaluation Context:** 

**Applicability Checks:** 

**Function Calls:**


## Rule Logic:
**Rule Assertion**
- Case 1: If the PCI is the correct ratio between proposed and baseline building performance; PASS: `if Output2019ASHRAE901.performance_cost_index == Output2019ASHRAE901.total_proposed_building_energy_cost_including_renewable_energy/Output2019ASHRAE901.baseline_building_performance_energy_cost`
- Case 2: Else; FAIL: `else: FAIL`

**Notes/Questions:** None


**[Back](../_toc.md)**