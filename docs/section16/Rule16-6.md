# Elevators – Rule 16-6  
**Schema Version:** 0.0.36        
**Mandatory Rule:** True          
**Rule ID:** 16-6  
**Rule Description:** When included in the proposed design, the baseline elevator cab ventilation fan power shall be 0.33 W/cfm  
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
  - Get the elevator cab ventilation fan power: `elevator_cab_ventilation_fan_power_b = elevator.cab_ventilation_fan_power`
  - Get the elevator cab ventilation fan airflow: `elevator_cab_ventilation_fan_flow_b = elevator.cab_ventilation_fan_flow`

  **Rule Assertion:**  
    - Case 1: Elevator cab ventilation fan power is equal to 0.33 W/cfm: PASS `if elevator_cab_ventilation_fan_power_b / elevator_cab_ventilation_fan_flow_b == 0.33 W/CFM: PASS`
    - Case 2: Else: FAIL `Else: FAIL`

**Notes/Questions:**
None

 **[Back](../_toc.md)**