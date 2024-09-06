# Elevators – Rule 16-2  
**Schema Version:** 0.0.36        
**Mandatory Rule:** True          
**Rule ID:** 16-2  
**Rule Description:** The baseline elevator motor use shall be modeled with the same schedule as the proposed design.  
**Rule Assertion:** B-RMD = P-RMD                                           
**Appendix G Section:** G3.1  
**Appendix G Section Reference:** Table G3.1-16 Baseline Building Performance  
**Data Lookup:** None  
**Evaluation Context:** Each elevator  

**Applicability Checks:**  
  1. The proposed and baseline buildings have an elevator.  

**Function Call:**  
match_data_element, compare_schedules

**Applicability Check 1:**
- Rule is applicable if the proposed and baseline RMD contain at least 1 elevator: `if find_all("$.buildings[*].elevators[*]", rmd_b) and find_all("$.buildings[*].elevators[*]", rmd_p):`

## Rule Logic:
- Determine if the project schedule uses a leap year: `is_leap_year = RPD.calendar.is_leap_year`
- If it is a leap year, set the schedule comparison mask to 8784 hours, else set it to 8760 hours: `mask_schedule = [1] * 8784 if is_leap_year else [1] * 8760`
- For each elevator in the baseline RMD: `for elevator_b in B_RMD...elevators`
  - Get the associated elevator object in the proposed RMD: `elevator_p = match_data_element(P_RMD, Elevator, elevator_b.id)` 
  - Get the modeled schedule for the elevator motor use in the baseline: `motor_use_schedule_b = elevator_b.cab_motor_multiplier_schedule`
  - Get the modeled schedule for the elevator motor use in the proposed: `motor_use_schedule_p = elevator_p.cab_motor_multiplier_schedule`
  - Compare the schedules: `comparison_data = compare_schedules(motor_use_schedule_b, motor_use_schedule_p, mask_schedule, is_leap_year):`  
  
  **Rule Assertion:**  
    - Case 1: If the schedules match for all hours: `if comparison_data['total_hours_matched'] == len(motor_use_schedule_b) == len(motor_use_schedule_p): PASS`
    - Case 2: Else: `FAIL`

**Notes/Questions:**
None

 **[Back](../_toc.md)**