# Envelope - Rule 5-39  
**Schema Version** 0.0.29
**Primary Rule:** False  
**Rule ID:** 5-39  
**Rule Description:** It is acceptable to use either an annual average ground temperature or monthly average ground temperatures for calculation of heat loss through basement floors.
**Appendix G Section:** Section 5 Envelope  
**Appendix G Section Reference:** Section G3.1-14(b) Building Envelope Modeling Requirements for the Proposed design and Baseline  

**Applicability:** All required data elements exist for B_RMD
**Applicability Checks:**  
  1. B_RMD contains at least 1 basement floor
 
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  
**Function Call:** None  

## Rule Logic:  
- If for-loop completes and no floor surfaces were found adjacent to ground, rule is not applicable: `is_applicable = false`
- For each surface in the B_RMD: `for surface in B_RMD...Surface:` 
  - If the surface is a floor and adjacent to ground, rule is applicable and continue to rule assertion: `if surface.classification == FLOOR and surface.adjacent_to == GROUND: is_applicable = true; break`

**Rule Assertion:**
- Case 1: If RPD includes annual average or monthly average ground temperature: `if RPD.weather.monthly_ground_temperature: UNDETERMINED`
- Case 2: Else: `else: FAIL`


**Notes:**
1. Why was below grade wall removed from rule? G3.1-14(b) - It is acceptable to use either an annual average ground temperature or monthly average ground temperatures for calculation of heat loss through ***below-grade walls and*** basement floors
2. Update Rule ID from 5-52 to 5-39 on 10/26/2023

**[Back](../_toc.md)**

**Notes:**
