# Section 19 - Rule 19-8        
**Schema Version:** 0.0.24  
**Mandatory Rule:** True  
**Rule ID:** 19-8         
**Rule Description:** Demand control ventilation is modeled in the baseline design in systems with outdoor air capacity greater than 3000 cfm serving areas with an average occupant design capacity greater than 100 people per 1000 ft^2.     
**Rule Assertion:** Options are Pass/Fail     
**Appendix G Section:** Section G3.1.2.5 Excetion #1      
**90.1 Section Reference:** None  

**Data Lookup:** None  

**Evaluation Context:** Each HeatingVentilationAirConditioningSystem Data Group  

**Applicability Checks:** None  

**Function Calls:**  
1. get_hvac_zone_list_w_area()  


## Rule Logic:  
- Get dictionary with hvac systems and associated zones and areas: `hvac_zone_list_w_area_dict_b  = get_hvac_zone_list_w_area(B_RMR)`  
- For each hvac_b system in B_RMI: `for hvac_b in hvac_zone_list_w_area_dict_b.keys():`  
    - Reset is_DCV_modeled to FALSE: `is_DCV_modeled = FALSE`  
    - Reset avg_occ_density to 0: `avg_occ_density = 0`  
    - Get the hvac system minimum OA flow: `hvac_min_OA_flow = hvac_b.fan_system.minimum_outdoor_airflow`  
    - Check whether DCV was modeled: `if hvac_b.fan_system.demand_control_ventilation_control != Null AND hvac_b.fan_system.demand_control_ventilation_control != "NONE": is_DCV_modeled_b = TRUE`  
    - Check whether the outdoor air capacity (i.e., minimum OA CFM) is greater than 3,000 cfm, if yes then carry on: `if hvac_min_OA_flow > 3000:`  
        - Get list of zones served: `zone_list_b = list(hvac_zone_list_w_area_dict_b[hvac_b.id]["Zone_List"].values())`  
        - Get area served by the the HVAC system: `hvac_area_b = hvac_zone_list_w_area_dict_b[hvac_b.id]["TOTAL_AREA"]`  
        - Reset total_hvac_sys_occupants_b to zero: `total_hvac_sys_occupants_b = 0`  
        - For each zone associated with the HVAC system, get the number of occupants associated with the hvac system by looping through all the associated zones and spaces: `for zone_b in zone_list_b:`         
            - Reset total_occ_num_across_spaces_b: `total_occ_num_across_spaces_b = 0`  
            - For each space associated with the zone, get the number of occupants associated with the space: `for space_b in zone_b.spaces:`  
                - Get number of occupants: `max_number_occ_b = space_b.number_of_occupants`   
                - Add to the total occupants across all spaces: `total_occ_num_across_spaces_b = total_occ_num_across_spaces_b + max_number_occ_b`  
            - Add to the total number of occs associated with the HVAC system: `total_hvac_sys_occupants_b = total_hvac_sys_occupants_b + total_occ_num_across_spaces_b`  
        - Calculate the average occupant density associated with the HVAC system: `avg_occ_density = total_hvac_sys_occupants_b/hvac_area_b`  
    - **Rule Assertion:** 
    - Case 1: If hvac_min_OA_flow > 3000 AND occupant density > 0.1 AND is_DCV_modeled_b == TRUE then pass: `If hvac_min_OA_flow > 3000 AND avg_occ_density > 0.1 AND is_DCV_modeled_b == TRUE: outcome = "PASS"`  
    - Case 2: Else If hvac_min_OA_flow <= 3000 OR occupant density <= 0.1 AND is_DCV_modeled_b == FALSE then pass: `elif hvac_min_OA_flow <= 3000 OR avg_occ_density >= 0.1 AND is_DCV_modeled_b == FALSE: outcome = "PASS"`
    - Case 3: Else, fail: `Else: outcome = "Fail"`  


**Notes/Questions:**  
1. On 1/11/2023 modified average design (occupant) capacity to equal the sum of the design # of occs across spaces divided by the total area served. I drafted an interpretation request to be submitted to 90.1 to get a definitive answer as to how this should be determined. 
2. Rule changed from 19-12 to 19-8 on 10/18/2022.
3. Modified on 11/19/2022 such that Space.number_of_occupants equals the design number of occupants (i.e., removed schedule multiplier)  .

**[Back](../_toc.md)**