# Envelope - Rule 5-38  
**Schema Version** 0.0.29  
**Primary Rule:** False  
**Rule ID:** 5-38  
**Rule Description:** It is acceptable to use either an annual average ground temperature or monthly average ground temperatures for calculation of heat loss through below-grade walls and basement floors.  
**Appendix G Section:** Section 5 Envelope  
**Appendix G Section Reference:** Section G3.1-14(b) Building Envelope Modeling Requirements for the Proposed design and Baseline  

**Applicability:** All required data elements exist for B_RMD  
**Applicability Checks:**  
  1. B_RMD contains at least 1 basement floor or below grade wall surface 
 
**Evaluation Context:** RMD  
**Data Lookup:** None  
**Function Calls:**
get_opaque_surface_type()

## Rule Logic:  
**Applicability Check 1**  
- If for-loop completes and no below-grade wall surfaces were found, rule is not applicable. (no below-grade walls also means no basement floors) : `is_applicable = false`  
- For each surface in the B_RMD: `for surface in B_RMD...Surface:`  
  - If the surface is a below-grade wall rule is applicable and continue to rule assertion: `if get_opaque_surface_type(surface) == "BELOW-GRADE WALL": is_applicable = true; break`  

**Rule Assertion:**  
- Case 1: If B_RMD has no below-grade wall surfaces and therefore also no basement floor surfaces: `if not is_applicable: NOT_APPLICABLE`  
- Case 2: If RPD includes a ground temperature schedule: `if RPD.weather.ground_temperature_schedule: UNDETERMINED and raise_message: "It cannot be determined if the ground temperature schedule for the project is representative of the project climate."`  
- Case 3: Else: `else: UNDETERMINED and raise_message: "The project has below-grade wall and/or basement floor surfaces, but a ground temperature schedule was not found."`  


**Notes:**
1. Update Rule ID from 5-52 to 5-39 on 10/26/2023  
2. Update Rule ID from 5-39 to 5-38 on 12/22/2023

**[Back](../_toc.md)**

**Notes:**
