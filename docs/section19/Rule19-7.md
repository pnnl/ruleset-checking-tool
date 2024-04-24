# Section 19 - Rule 19-7               
**Schema Version:** 0.0.24      
**Mandatory Rule:** True    
**Rule ID:** 19-7                 
**Rule Description:**  Minimum ventilation system outdoor air intake flow shall be the same for the proposed design and baseline building design except when any of the 4 exceptions defined in Section G3.1.2.5 are met.  
Exceptions included in this RDS:
2. When designing systems in accordance with Standard 62.1, Section 6.2, “Ventilation Rate Procedure,” reduced ventilation airflow rates may be calculated for each HVAC zone in the proposed design with a zone air distribution effectiveness (Ez) > 1.0 as defined by Standard 62.1, Table 6-2. Baseline ventilation airflow rates in those zones shall be calcu-lated using the proposed design Ventilation Rate Procedure calculation with the following change only. Zone air distribution effectiveness shall be changed to (Ez) = 1.0 in each zone having a zone air distribution effectiveness (Ez) > 1.0. Proposed design and baseline build-ing design Ventilation Rate Procedure calculations, as described in Standard 62.1, shall be submitted to the rating authority to claim credit for this exception. M


**Rule Assertion:** Options are Pass/Fail/UNDETERMINED/NOT_APPLICABLE      
**Appendix G Section:** G3.1.2.5 and Exception 2           
**90.1 Section Reference:** None  

**Data Lookup:** None    

**Evaluation Context:** Each HeatingVentilatingAirConditioningSystem  

**Applicability Checks:**  
1. Not applicable to hvac systems only serving labs (G3.1.2.5 and Exception 4)
   
**Function Calls:**  
1. get_dict_of_zones_and_terminal_units_served_by_hvac_sys()    
2. match_data_element()  
3. get_component_by_id()  
4. get_list_hvac_systems_associated_with_zone()  
5. get_min_OA_CFM_sch_zone()  
6. aggregate_min_OA_schedule_across_zones()  


## Rule Logic:   
- Create dictionary of hvac systems and associated zones and terminal units for the baseline: `dict_of_zones_and_terminal_units_served_by_hvac_sys_b = get_dict_of_zones_and_terminal_units_served_by_hvac_sys(B_RMI)`   
- For each hvac system in the B_RMI: `for hvac in B_RMI...HeatingVentilatingAirConditioningSystem:`  
    - Reset was_DCV_modeled_baseline boolean variable to false: `was_DCV_modeled_baseline = false`  
    - Reset was_DCV_modeled_proposed boolean variable to false: `was_DCV_modeled_proposed = false`  
    - Reset zone_air_distribution_effectiveness_greater_than_1 boolean to false: `zone_air_distribution_effectiveness_greater_than_1 = false`  
    - Reset hvac_system_serves_only_labs boolean variable to true: `hvac_system_serves_only_labs = true`  
    - Reset all_lighting_space_types_defined boolean variable to true: `all_lighting_space_types_defined = true`  
    - Reset are_any_lighting_space_types_defined boolean variable to true: `are_any_lighting_space_types_defined = false`  
    - Check if demand controlled ventilation was modeled at the fan_system: `if hvac.fan_system.demand_control_ventilation_control == true: was_DCV_modeled_baseline= true`  
    - **Applicability Check 1** - Check that the HVAC system does not only serve labs (covered by 19-39)
    - Get list of zones served by the hvac system: `zones_list_hvac_sys_b = dict_of_zones_and_terminal_units_served_by_hvac_sys_b[hvac.id]["ZONE_LIST"]`  
        - For each space associated with the zone, check if any spaces are NOT labs or if any lighting space types are not defined: `for space in zone.spaces:`
            - Check if hvac_system_serves_only_labs = true (no need to keep looping through space types if it equals false): `if hvac_system_serves_only_labs == true:`  
                - Check if the lighting space type is defined: `if space.lighting_space_type == Null: all_lighting_space_types_defined = false`    
                - if the lighting space type is not defined: `else:`   
                    - Set are_any_lighting_space_types_defined = true: `are_any_lighting_space_types_defined = true`  
                    - Check if the lighting space type is NOT a lab: `if space.lighting_space_type not in [LABORATORY_EXCEPT_IN_OR_AS_A_CLASSROOM]: hvac_system_serves_only_labs = false`    
                - Else (i.e., space.lighting_space_type = Null), set all_lighting_space_types_defined = true: `all_lighting_space_types_defined = false`   

    - Check if hvac_system_serves_only_labs = false or if hvac_system_serves_only_labs = false but not all (or any) space types are defined, if false carry on, if true then NOT_APPLICABLE outcome for this HVAC system: `if hvac_system_serves_only_labs == false or (hvac_system_serves_only_labs == true and all_lighting_space_types_defined == false):`        
        - Set counter equal to 0: `counter = 0`  
        - For each zone associated with the HVAC system: `for zone in zones_list_hvac_sys_b:`  
            - Add each zone's OA CFM schedule to the list of zone OA CFM schedules for the baseline: `zone_OA_CFM_list_of_schedules_b[counter] = get_min_OA_CFM_sch_zone(B_RMI, zone.id)`  
            - Get the analogous zone object from the proposed RMD (if this is not strictly the correct syntax please advise Weili): `zone_p = get_component_by_id(P_RMI,match_data_element(P_RMI,Zone,zone.id))`    
            - Add each zone's OA CFM schedule to the list of zone OA CFM schedules for the proposed: `zone_OA_CFM_list_of_schedules_p[counter] = get_min_OA_CFM_sch_zone(P_RMI, zone_p.id)`  

            - For each terminal unit serving the zone, check if DCV was modeled: `for terminal in zone.terminals:`  
                - Check if DCV was modeled: `if terminal.has_demand_control_ventilation == true: was_DCV_modeled_baseline = true`  
            
            - Check if the air distribution effectiveness is greater than 1 in the proposed: `if zone_p.air_distribution_effectiveness >1: zone_air_distribution_effectiveness_greater_than_1 = true`  

            - For each terminal unit serving the zone in the proposed, check if DCV was modeled: `for terminal in zone_p.terminals:`  
                - Check if DCV was modeled: `if terminal.has_demand_control_ventilation == true: was_DCV_modeled_proposed = true`  
                - Check if the hvac system serving the terminal unit has dcv modeled (weili may have to include some logic to get the hvac object from the id): `if terminal.served_by_heating_ventilating_air_conditioning_system.fan_system.demand_control_ventilation_control != "None": was_DCV_modeled_proposed`  
            
            - Add to counter: `counter = counter + 1`  

        - Create aggregated OA CFM schedule for the baseline for the zones served by the hvac system: `aggregated_min_OA_schedule_across_zones_b = aggregate_min_OA_schedule_across_zones(B_RMI,zone_OA_CFM_list_of_schedules_b)`  
        - Create aggregated OA CFM schedule for the proposed for the zones served by the baseline hvac system: `aggregated_min_OA_schedule_across_zones_p = aggregate_min_OA_schedule_across_zones(P_RMI,zone_OA_CFM_list_of_schedules_p)`  

        - Reset OA_CFM_schedules_match boolean variable to True: `OA_CFM_schedules_match = True`  
        - Check if schedules mismatch for any hours of the year, if so set boolean to false: `for p to Range(8760):`  
            - Check if the baseline and proposed schedules mismatch: `if aggregated_min_OA_schedule_across_zones_b[p] != aggregated_min_OA_schedule_across_zones_p[p]: OA_CFM_schedule_match = false`   

        - Sum OA CFM across baseline schedule to get the total for comparison purposes in the rule assertions: `modeled_baseline_total_zone_min_OA_CFM = sum(aggregated_min_OA_schedule_across_zones_b)`  
        - Sum OA CFM across proposed schedule to get the total for comparison purposes in the rule assertions: `modeled_proposed_total_zone_min_OA_CFM = sum(aggregated_min_OA_schedule_across_zones_p)`  


        - **Rule Assertion:** 
        - Case 1: If the modeled baseline and proposed minimum OA cfm values are identical (OA CFM values match all hours of the year) and hvac_system_serves_only_labs == false then pass: `if OA_CFM_schedule_match == true and hvac_system_serves_only_labs == false: outcome = "PASS"`  
        - Case 2: Elif the modeled baseline and proposed minimum OA cfm values are identical (OA CFM values match all hours of the year) and some space types are labs but not all space types are defined then pass: `elif OA_CFM_schedule_match == true and (hvac_system_serves_only_labs == true and are_any_lighting_space_types_defined == true): outcome = "PASS" and raise_message "<insert hvac.id> passes this check unless it only serves labs. This hvac system serves some labs but it could not be determined from the RMD if it only serves labs. Outcome is UNDETERMINED if the HVAC system only serves lab spaces due to G3.1.2.5 Exception 4."`  
        - Case 3: Elif the modeled baseline and proposed minimum OA cfm values are identical (OA CFM values match all hours of the year) and and all space types are undefined then pass: `elif OA_CFM_schedule_match == true and are_any_lighting_space_types_defined == false: outcome = "PASS" and raise_message "<insert hvac.id> passes this check unless it only serves lab spaces (no space types were defined in the RMD so this could not be determined). Outcome is UNDETERMINED if the HVAC system only serves lab spaces due to G3.1.2.5 Exception 4."`  
        - Case 4: Else if the modeled baseline minimum OA cfm are greater than the modeled proposed minimum OA cfm and a zone served by the HVAC in the baseline has demand controlled ventilation modeled in the proposed (Exception 1) and the hvac system does not only serve labs then the outcome is Fail: `elif modeled_baseline_total_zone_min_OA_CFM > modeled_proposed_total_zone_min_OA_CFM and was_DCV_modeled_baseline == false and was_DCV_modeled_proposed == true and zone_air_distribution_effectiveness_greater_than_1 == false and hvac_system_serves_only_labs == false: outome = "FAIL" and raise_message "For <insert hvac.id> the baseline modeled minimum ventilation system outdoor air intake flow CFM is higher than the minimum ventilation system outdoor air intake flow CFM modeled in the proposed design. Demand-controlled ventilation was modeled in the proposed and not the baseline model and demand-controlled ventilation may be double accounted for in the model (per the HVAC controls and via reduced OA CFM rates in the proposed)."`  
        - Case 5: Else if the modeled baseline minimum OA cfm are greater than the modeled proposed minimum OA cfm and a zone served by the HVAC in the baseline has demand controlled ventilation modeled in the proposed (Exception 1) and it is unknown if the hvac system only serve labs then the outcome is Fail: `elif modeled_baseline_total_zone_min_OA_CFM > modeled_proposed_total_zone_min_OA_CFM and was_DCV_modeled_baseline == false and was_DCV_modeled_proposed == true and zone_air_distribution_effectiveness_greater_than_1 == false: outome = "FAIL" and raise_message "For <insert hvac.id> the baseline modeled minimum ventilation system outdoor air intake flow CFM is higher than the minimum ventilation system outdoor air intake flow CFM modeled in the proposed design. Demand-controlled ventilation was modeled in the proposed and not the baseline model and demand-controlled ventilation may be double accounted for in the model (per the HVAC controls and via reduced OA CFM rates in the proposed). Alternatively, the hvac system may only serve labs in which case G3.1.2.5 Exception 4 may be applicable and leading to allowed higher modeled rates in the baseline."`  
        - Case 6: Else if the modeled baseline minimum OA cfm are greater than the modeled proposed minimum OA cfm and a zone served by the HVAC in the baseline has an air distribution effectivenss of greater than 1 in the proposed (Exception 2) and the hvac system does not only serve labs then the outcome is UNDETERMINED: `elif modeled_baseline_total_zone_min_OA_CFM > modeled_proposed_total_zone_min_OA_CFM and zone_air_distribution_effectiveness_greater_than_1 == true and hvac_system_serves_only_labs == false: outome = "UNDETERMINED" and raise_message "For <insert hvac.id> the modeled baseline minimum ventilation system outdoor air intake flow CFM is higher than the minimum ventilation system outdoor air intake flow CFM modeled in the proposed design. It appears as though G3.1.2.5 Exception 2 may be applicable. A manual check for this exception is recommended otherwise fail."`  
        - Case 7: Else if the modeled baseline minimum OA cfm are greater than the modeled proposed minimum OA cfm and a zone served by the HVAC in the baseline has an air distribution effectivenss of greater than 1 in the proposed (Exception 2) and it is unknown whether the hvac system serves all labs then the outcome is UNDETERMINED: `elif modeled_baseline_total_zone_min_OA_CFM > modeled_proposed_total_zone_min_OA_CFM and zone_air_distribution_effectiveness_greater_than_1 == true: outome = "UNDETERMINED" and raise_message "For <insert hvac.id> the modeled baseline minimum ventilation system outdoor air intake flow CFM is higher than the minimum ventilation system outdoor air intake flow CFM modeled in the proposed design. It appears as though G3.1.2.5 Exception 2 may be applicable because the air distribution effectiveness was modeled as greater than 1. Alternatively, the system may only serves lab spaces and G3.1.2.5 Exception 4 may be applicable. A manual check for these exceptions is recommended otherwise fail."`          
        - Case 8: Else if the modeled baseline minimum OA cfm are less than the modeled proposed minimum OA cfm the outcome is UNDETERMINED: `elif modeled_baseline_total_zone_min_OA_CFM < modeled_proposed_total_zone_min_OA_CFM: outome = "UNDETERMINED" and raise_message "For <insert hvac.id> the modeled minimum ventilation system outdoor air intake flow CFM is lower than the minimum ventilation system outdoor air intake flow CFM modeled in the proposed design. Check if G3.1.2.5 Exception 3 is applicable. This exception states that where the minimum outdoor air intake flow in the proposed design is provided in excess of the amount required by the building code or the rating authority, the baseline building design shall be modeled to reflect the greater of that required by either the rating authority or the building code and will be less than the proposed design. "`  
        - Case 9: Else if, the hvac system does not only serve labs fail: `elif hvac_system_serves_only_labs == false: outcome = "Fail" and raise_message "For <insert hvac.id> the modeled baseline minimum ventilation system outdoor air intake flow CFM is higher than the minimum ventilation system outdoor air intake flow CFM modeled in the proposed design which does not meet the requirements of Section G3.1.2.5."`  
        - Case 10: Else if, the modeled baseline and proposed minimum OA cfm values are NOT identical (OA CFM values match all hours of the year) and the modeled baseline minimum OA cfm are equal to the modeled proposed minimum OA cfm: `OA_CFM_schedule_match == false and modeled_baseline_total_zone_min_OA_CFM == modeled_proposed_total_zone_min_OA_CFM: outcome = "Fail" and raise_message "Fail because the outdoor air schedules do not appear to match between the baseline and proposed."`   
        - Case 11: Else, its unknown if the hvac system only serves labs fail: `Else: outcome = "Fail" and raise_message "For <insert hvac.id> the modeled baseline minimum ventilation system outdoor air intake flow CFM is higher than the minimum ventilation system outdoor air intake flow CFM modeled in the proposed design which does not meet the requirements of Section G3.1.2.5. Fail unless the hvac system only serves labs and G3.1.2.5 Exception 4 is applicable."`  


**Notes/Questions:**   
1. Labs now covered by RDS 19-39. 

**[Back](_toc.md)**