# Elevators – Rule 16-1  
**Schema Version:** 0.0.36        
**Mandatory Rule:** True          
**Rule ID:** 16-1  
**Rule Description:** The elevator peak motor power shall be calculated according to the equation in Table G3.1-16  
**Rule Assertion:** B-RMR = expected value                                           
**Appendix G Section:** G3.1  
**Appendix G Section Reference:** Table G3.1-16 Baseline Building Performance  
**Data Lookup:** Table G3.9.1, Table G3.9.2, Table G3.9.3  
**Evaluation Context:** Each elevator  

**Applicability Checks:**  
  1. The proposed and baseline buildings have an elevator.  

**Function Call:**  
data_lookup

**Applicability Check 1:**
- Rule is applicable if the proposed and baseline RMD contain at least 1 elevator: `if find_all("$.buildings[*].elevators[*]", rmd_b) and find_all("$.buildings[*].elevators[*]", rmd_p):`

## Rule Logic:
- For each elevator in the building: `for elevator in B_RMD...elevators`
  - Get the number of floors served by the elevator: `total_floors_served_b = elevator.number_of_floors_served` 
  - Get the elevator motor power: `elevator_motor_power_b = elevator.motor_power`
  - Get the elevator cab weight: `elevator_cab_weight_b = elevator.cab_weight`
  - Get the elevator cab counterweight: `elevator_cab_counterweight_b = elevator.cab_counterweight`
  - Get the elevator design load: `elevator_design_load_b = elevator.design_load`
  - Get the elevator speed: `elevator_speed_b = elevator.speed`
  - If any detailed elevator data parameters are not defined: `if any(param == Null for param in [total_floors_served_b, elevator_motor_power_b, elevator_cab_weight_b, elevator_cab_counterweight_b, elevator_design_load_b, elevator_speed_b]): has_undetermined = true`
  - Get the elevator mechanical efficiency: `elevator_mechanical_efficiency_b = data_lookup('table_g3.9.2', total_floors_served_b)['mechanical_efficiency']`
  - Calculate the motor brake horsepower: `motor_brake_horsepower_b = (elevator_cab_weight_b + elevator_design_load_b - elevator_cab_counterweight_b) * elevator_speed_b / 33000 / elevator_mechanical_efficiency_b`
  - If the total number of floors is greater than 4: `if total_floors_served_b > 4:`
    - Get the elevator motor efficiency associated with the next shaft input power greater than the bhp from Table G3.9.1: `elevator_motor_efficiency_b = data_lookup('table_g3.9.1', motor_brake_horsepower_b)['motor_efficiency']`
  - Else:
    - Get the elevator motor efficiency associated with the next shaft input power greater than the bhp from Table G3.9.3: `elevator_motor_efficiency_b = data_lookup('table_g3.9.3', motor_brake_horsepower_b)['motor_efficiency']`
  - Calculate the expected peak motor power: `expected_peak_motor_power = motor_brake_horsepower_b * 745.7 / elevator_motor_efficiency_b`
    
  **Rule Assertion:**  
  - Case 1: If the number of floors in the building could not be determined or any detailed elevator data parameters are not defined, outcome = UNDETERMINED: `if has_undetermined: UNDETERMINED`
  - Case 2: If the calculated peak motor power is equal to the expected value: `if elevator_motor_power_b == expected_peak_motor_power: PASS`
  - Case 3: Else: `else: FAIL`

**Notes/Questions:**
1. The schema says that "The motor power can be provided either together with or, instead of, the detailed elements used to calculate it." Rule outcome will be undetermined if any of the detailed elements are not provided.
2. The Elevator.number_of_floors_served data element is not yet defined in the schema. This will need to be added. An issue has been created.

 **[Back](../_toc.md)**