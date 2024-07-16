# Elevators – Rule 16-7  
**Schema Version:** 0.0.36        
**Mandatory Rule:** True          
**Rule ID:** 16-7  
**Rule Description:** When included in the proposed design, the baseline elevator cab lighting power density shall be 3.14 W/ft2  
**Rule Assertion:** B-RMD = Expected Value                                           
**Appendix G Section:** G3.1  
**Appendix G Section Reference:** Table G3.1-16 Baseline Building Performance  
**Data Lookup:** None  
**Evaluation Context:** Each elevator  

**Applicability Checks:**  
  1. The proposed and baseline buildings have an elevator.  

**Function Call:**  
N/A

**Applicability Check 1:**
- Rule is applicable if the proposed and baseline RMD contain at least 1 elevator: `if find_all("$.buildings[*].elevators[*]", rmd_b) and find_all("$.buildings[*].elevators[*]", rmd_p):`

## Rule Logic:
- For each elevator in the baseline RMD: `for elevator in B_RMD...elevators`
  - Get the elevator cab lighting power: `cab_lighting_power_b = elevator.cab_lighting_power`
  - Get the elevator cab area: `cab_area_b = elevator.cab_area`

  **Rule Assertion:**  
    - Case 1: Elevator cab lighting power is equal to 3.14 W/ft2: PASS `if cab_lighting_power_b / cab_area_b == 3.14 W/ft2: PASS`
    - Case 2: Else: FAIL `Else: FAIL`

**Notes/Questions:**
None

 **[Back](../_toc.md)**