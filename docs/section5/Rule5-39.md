# Envelope - Rule 5-39  
**Schema Version** 0.0.29  
**Primary Rule:** False  
**Rule ID:** 5-39  
**Rule Description:** It is acceptable to use either an annual average ground temperature or monthly average ground temperatures for calculation of heat loss through basement floors.  
**Appendix G Section:** Section 5 Envelope  
**Appendix G Section Reference:** Section G3.1-14(b) Building Envelope Modeling Requirements for the Proposed design and Baseline  

**Applicability:** All required data elements exist for B_RMD  
**Applicability Checks:**  
  1. B_RMD contains at least 1 floor surface adjacent to ground  
 
**Evaluation Context:** RMD  
**Data Lookup:** None  
**Function Call:** None  

## Rule Logic:  
**Applicability Check 1**  
- If for-loop completes and no floor surfaces were found adjacent to ground, rule is not applicable: `is_applicable = false`  
- For each surface in the B_RMD: `for surface in B_RMD...Surface:`  
  - If the surface is a floor and adjacent to ground, rule is applicable and continue to rule assertion: `if surface.classification == FLOOR and surface.adjacent_to == GROUND: is_applicable = true; break`  

**Rule Assertion:**  
- Case 1: If B_RMD has no floor surfaces adjacent to ground: `if not is_applicable: NOT_APPLICABLE`  
- Case 2: If RPD includes a ground temperature schedule: `if RPD.weather.ground_temperature_schedule: UNDETERMINED`  
- Case 3: Else: `else: FAIL`  


**Notes:**
1. Are slab-on-grade floors different from basement floors - Can we tell the difference from the schema?  
2. Why was below grade wall removed from rule? G3.1-14(b) - It is acceptable to use either an annual average ground temperature or monthly average ground temperatures for calculation of heat loss through ***below-grade walls and*** basement floors  
3. Update Rule ID from 5-52 to 5-39 on 10/26/2023  

**[Back](../_toc.md)**

**Notes:**
