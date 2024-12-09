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
  1. The proposed and baseline buildings have an elevator.  

**Function Call:**  
compare_schedules

**Applicability Check 1:**
- Rule is applicable if the proposed and baseline RMD contain at least 1 elevator: `if find_all("$.buildings[*].elevators[*]", rmd_b) and find_all("$.buildings[*].elevators[*]", rmd_p):`

## Rule Logic:
- Determine if the project schedule uses a leap year: `is_leap_year = RPD.schedule.is_leap_year`
- If the project schedule uses a leap year, set total hours to 8784, else 8760: `total_hours = 8784 if is_leap_year else 8760`
- Create a continuous schedule to compare against, and also to use as the mask schedule for the function: `continuous_schedule = [1]*total_hours`
- For each elevator in the baseline RMD: `for elevator in B_RMD...elevators`
  - Get the modeled schedule for the baseline elevator cab ventilation fan: `cab_ventilation_schedule_b = elevator.cab_ventilation_fan_multiplier_schedule`
  - Get the modeled schedule for the baseline elevator cab lighting: `cab_lighting_schedule_b = elevator.cab_lighting_multiplier_schedule`
  - Compare the cab ventilation schedule with the continuous schedule: `vent_sched_compare_data = compare_schedules(cab_ventilation_schedule_b, continuous_schedule, continuous_schedule, is_leap_year)`
  - Compare the cab lighting schedule with the continuous schedule: `light_sched_compare_data = compare_schedules(cab_lighting_schedule_b, continuous_schedule, continuous_schedule, is_leap_year)`

  **Rule Assertion:**  
    - Case 1: If the schedules for lighting and ventilation are identical and continuous for all hours: `if vent_sched_compare_data["total_hours_matched"] == light_sched_compare_data["total_hours_matched"] == total_hours: PASS`
    - Case 2: Else: `FAIL`

**Notes/Questions:**
None

 **[Back](../_toc.md)**