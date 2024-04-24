# Elevators – Rule 16-1  
**Schema Version:** 0.0.36        
**Mandatory Rule:** True          
**Rule ID:** 16-1  
**Rule Description:** The elevator peak motor power shall be calculated according to the equation in Table G3.1-16  
**Rule Assertion:** B-RMR = expected value                                           
**Appendix G Section:** G3.1  
**Appendix G Section Reference:** Table G3.1-16  
**Data Lookup:** Table G3.9.1, Table G3.9.2, Table G3.9.3  
**Evaluation Context:** Each elevator  

**Applicability Checks:**  
  1. The proposed building has an elevator.  

**Function Call:**  
N/A

**Applicability Check 1:**
- Rule is applicable if any building in the proposed RMD has an elevator: `if any(len(building.elevators) > 0 for building in P_RMD...buildings:`

## Rule Logic:
- For each building in the baseline RMD: `for building in B_RMD...buildings`
  - Get the number of floors above grade in the building: `floors_above_grade_b = building.number_of_floors_above_grade`
  - Get the number of floors below grade in the building: `floors_below_grade_b = building.number_of_floors_above_grade`
  - If both floors above grade and floors below grade are null: `if floors_above_grade_b == Null and floors_below_grade_b == Null: is_undetermined = true`
  - Elif floors above grade is null: `elif floors_above_grade_b == Null: total_floors_b = floors_below_grade_b`
  - Elif floors below grade is null: `elif floors_below_grade_b == Null: total_floors_b = floors_above_grade_b`
  - Else, calculate the total number of floors in the building: `else: total_floors_b = floors_above_grade_b + floors_below_grade_b`
  - For each elevator in the building: `for elevator in B_RMD...elevators`
    - Get the elevator motor power: `elevator_motor_power_b = elevator.motor_power`
    - Get the elevator cab weight: `elevator_cab_weight_b = elevator.cab_weight`
    - Get the elevator cab counterweight: `elevator_cab_counterweight_b = elevator.cab_counterweight`
    - Get the elevator design load: `elevator_design_load_b = elevator.design_load`
    - Get the elevator speed: `elevator_speed_b = elevator.speed`
    - If any detailed elevator data parameters are not defined: `if any(param == Null for param in [elevator_motor_power_b, elevator_cab_weight_b, elevator_cab_counterweight_b, elevator_design_load_b, elevator_speed_b]): is_undetermined = true`
    - Get the elevator mechanical efficiency: `elevator_mechanical_efficiency_b = data_lookup('table_g3.9.2', total_floors_b)['mechanical_efficiency']`
    - Calculate the motor brake horsepower: `motor_brake_horsepower_b = (elevator_cab_weight_b + elevator_design_load_b - elevator_cab_counterweight_b) * elevator_speed_b / 33000 / elevator_mechanical_efficiency_b`
    - If the total number of floors is greater than 4: `if total_floors_b > 4:`
      - Get the elevator motor efficiency associated with the next shaft input power greater than the bhp from Table G3.9.1: `elevator_motor_efficiency_b = data_lookup('table_g3.9.1', motor_brake_horsepower_b)['motor_efficiency']`
    - Else:
      - Get the elevator motor efficiency associated with the next shaft input power greater than the bhp from Table G3.9.3: `elevator_motor_efficiency_b = data_lookup('table_g3.9.3', motor_brake_horsepower_b)['motor_efficiency']`
    - Calculate the expected peak motor power: `expected_peak_motor_power = motor_brake_horsepower_b * 746 / elevator_motor_efficiency_b`
    
    **Rule Assertion:**  
    - Case 1: If the number of floors in the building could not be determined or any detailed elevator data parameters are not defined, outcome = UNDETERMINED: `if is_undetermined: UNDETERMINED`
    - Case 2: If the calculated peak motor power is equal to the expected value: `if elevator_motor_power_b == expected_peak_motor_power: PASS`
    - Case 3: Else: `else: FAIL`

**Notes/Questions:**
1. The schema says that "The motor power can be provided either together with or, instead of, the detailed elements used to calculate it." Rule outcome will be undetermined if any of the detailed elements are not provided.


 **[Back](../_toc.md)**