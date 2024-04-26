# Elevators – Rule 16-5  
**Schema Version:** 0.0.36        
**Mandatory Rule:** True          
**Rule ID:** 16-5  
**Rule Description:** When included in the proposed design, the baseline elevator cab ventilation fan and lights shall operate continuously  
**Rule Assertion:** B-RMD = Expected Value                                           
**Appendix G Section:** G3.1  
**Appendix G Section Reference:** Table G3.1-16 Baseline Building Performance  
**Data Lookup:** None  
**Evaluation Context:** Each elevator  

**Applicability Checks:**  
  1. The proposed building has an elevator.  

**Function Call:**  
N/A

**Applicability Check 1:**
- Rule is applicable if any building in the proposed RMD has an elevator: `if any(len(building.elevators) > 0 for building in P_RMD...buildings:`

## Rule Logic:
- If the project schedule uses a leap year, set total hours to 8784, else 8760: `total_hours = 8784 if RPD.schedule.is_leap_year else 8760`
- For each elevator in the baseline RMD: `for elevator in B_RMD...elevators`
  - Get the modeled schedule for the baseline elevator cab ventilation fan: `cab_ventilation_schedule_b = elevator.cab_ventilation_fan_multiplier_schedule`
  - Get the modeled schedule for the baseline elevator cab lighting: `cab_lighting_schedule_b = elevator.cab_lighting_multiplier_schedule`

  **Rule Assertion:**  
    - Case 1: If the schedules for lighting and ventilation are identical and continuous for all hours: `if sum(cab_ventilation_schedule_b) == sum(cab_lighting_schedule_b) == total_hours: PASS`
    - Case 2: Else: `FAIL`

**Notes/Questions:**
None

 **[Back](../_toc.md)**