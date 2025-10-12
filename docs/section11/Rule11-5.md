# Service Water Heating - Rule 11-5

**Schema Version:** 0.0.37  
**Mandatory Rule:** True  
**Rule ID:** 11-5  
**Rule Description:** Piping losses shall not be modeled.   
**Rule Assertion:** Options are PASS/FAIL/NOT_APPLICABLE/UNDETERMINED  
**Appendix G Section Reference:** Table G3.1 #11, proposed column, f  

**Evaluation Context:** Each SWH Distribution System  
**Data Lookup:**    
**Function Call:**  

**Applicability Checks:**
- Every Proposed distribution system is applicable  


## Rule Logic:
- Get to the `service_water_heating_distribution_systems` level
    - Define a list that stores the pipe data: `piping_losses_modeled = []`  
    - Loop over the `service_water_piping` object: `for service_water_piping in swh_dist_sys_p["service_water_piping"]:`
    - Store the current piping obj: `queue = deque([service_water_piping])`
    - Check the `are_thermal_losses_modeled` value including all the child pipes: 
    -    `while queue:`  
        -   `current_piping = queue.popleft()`  
        -    `children_piping = current_piping.get("child", [])`  
        -    `queue.extend(children_piping)`  
        -    `piping_losses_modeled_p.append(current_piping.get("are_thermal_losses_modeled"))`  


- **Rule Assertion - Zone:**  
- Case1: piping losses are not modeled, PASS: `if not any(piping_losses_modeled_p): PASS`
- Case2: piping losses are modeled, FAIL: `else: FAIL`


**Notes:**

**[Back](../_toc.md)**
