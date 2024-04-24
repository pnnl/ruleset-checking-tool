# Elevators – Rule 16-3  
**Schema Version:** 0.0.36        
**Mandatory Rule:** True          
**Rule ID:** 16-3  
**Rule Description:** The elevator cab ventilation fan shall be modeled with the same schedule as the elevator motor.  
**Rule Assertion:** P-RMD = Expected Value                                          
**Appendix G Section:** G3.1  
**Appendix G Section Reference:** Table G3.1-16  
**Data Lookup:** None  
**Evaluation Context:** Each elevator  

**Applicability Checks:**  
  1. The proposed building has an elevator.  

**Function Call:**  
N/A

**Applicability Check 1:**
- Rule is applicable if any building in the proposed RMD has an elevator: `if any(len(building.elevators) > 0 for building in P_RMD...buildings:`

## Rule Logic:
- For each elevator in the proposed RMD: `for elevator in P_RMD...elevators`
  - Get the modeled schedule for the elevator motor use in the proposed: `motor_use_schedule_p = elevator_p.cab_motor_multiplier_schedule`
  - Get the modeled schedule for the elevator cab ventilation use in the proposed: `cab_ventilation_schedule_p = elevator_p.cab_ventilation_fan_multiplier_schedule`
  - Compare the schedules: `comparison_data = compare_schedules(cab_ventilation_schedule_p, motor_use_schedule_p):`  
  
  **Rule Assertion:**  
    - Case 1: If the schedules match for all hours: `if comparison_data['TOTAL_HOURS_MATCH'] == len(cab_ventilation_schedule_p) == len(motor_use_schedule_p): PASS`
    - Case 2: Else: `FAIL`

**Notes/Questions:**
None

 **[Back](../_toc.md)**