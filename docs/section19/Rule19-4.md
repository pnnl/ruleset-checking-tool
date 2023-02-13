# Section 19 - Rule 19-4             
**Schema Version:** 0.0.24      
**Mandatory Rule:** True    
**Rule ID:** 19-4               
**Rule Description:**  For baseline cooling sizing runs in residential dwelling units, the infiltration, occupants, lighting, gas and electricity using equipment hourly schedule shall be the same as the most used hourly weekday schedule from the annual simulation.  

**Rule Assertion:** Options are Pass/Fail/NOT_APPLICABLE     
**Appendix G Section:** Exception to G3.1.2.2.1          
**90.1 Section Reference:** None  

**Data Lookup:** None    

**Evaluation Context:** Each Space  

**Applicability Checks:**  
1. Applies to residential dwelling unit spaces only.  
  
   
**Function Calls:**  
1. get_component_by_id()  I think this is supposed to return the object associated with an ID?
2. get_most_used_weekday_hourly_schedule()  To be developed by RCT team. I created a shell for this so they know what we need.  



## Rule Logic:   
**Applicability Check 1 - Check if the space is a residential dwelling unit**  
- For each space in the B_RMI: `for space in B_RMI...Space:`   
    - Reset bldg_type to "": `bldg_type = ""`  
    - Reset the building area defined boolean variable to false: `bldg_area_is_defined = false`  
    - Reset the building_area_is_MF_dormitory_or_hotel boolean variable to false: `building_area_is_MF_dormitory_or_hotel = false`  
    - Reset space_lighting_or_vent_space_type_is_defined to true: `space_lighting_or_vent_space_type_is_defined = true`  
    - Reset space type is dwelling unit boolean variable to false: `space_lighting_space_type_is_dwelling_unit = false` 

    - Get the zone that the space is part of by looping through zones and checking is the space is associated with the zone: `for zone in B_RMI...Zone:`  
        - Check if the space is associated with the zone, if it is then set is equal to the applicable_zone: `if space in zone.spaces: applicable_zone = zone`  
    
    - Check if the lighting and ventilation space types are both NOT defined: `if space.lighting_space_type == Null and space._ventilation_space_type == Null: ` 
        - Set space_lighting_or_vent_space_type_is_defined = false: `space_lighting_or_vent_space_type_is_defined = false`  
        - Loop through the building segments to determine which building segment the zone is apart of: `for bldg_seg in B_RMI...Building.building_segments:`  
            - Check if the zone is in bldg_seg.zones, if yes then set the bldg_type to the building area lighting type associated with the building segment: `if applicable_zone in bldg_seg.zones: bldg_type = bldg_seg.lighting_building_area_type`
            - Check if the lighting building area type was defined: `if bldg_type != Null: bldg_area_is_defined = true`  
            - Check if the lighting building area type is multifamily, dormitory, or hotel/motel: `if bldg_type in ["DORMITORY","HOTEL_MOTEL","MULTIFAMILY"]: building_area_is_MF_dormitory_or_hotel = true`  
    
    - Check if space_lighting_or_vent_space_type_is_defined = True, if yes carry on with logic, if not go to rule assertions: `if space_lighting_or_vent_space_type_is_defined = true:`  
        - Check if the lighting or ventilation space type is of a residential dwelling unit type, if yes carry on, if not then outcome for this space is NOT_APPLICABLE: `if space.lighting_space_type in ["DWELLING_UNIT"] or space._ventilation_space_type in ["TRANSIENT_RESIDENTIAL_DWELLING_UNIT"]:`       
            - Set space_lighting_space_type_is_dwelling_unit to true: `space_lighting_space_type_is_dwelling_unit = true`  
            Infiltration schedule check:
            - Reset inf_pass_cooling boolean variable: `inf_pass_cooling = true` 
            - Get the infiltration object associated with the zone: `infiltration_obj = applicable_zone.infiltration`  
            - Get the multiplier schedule: `multiplier_sch = get_component_by_id(B_RMI,infiltration_obj.multiplier_schedule)`  
            - Get the design_cooling_multiplier_schedule: `design_cooling_multiplier_sch = multiplier_sch.cooling_design_day_sequence`  
            - Get the get_most_used_weekday_hourly_schedule (this will be a list with 24 values for each hour of a day): `most_used_weekday_hourly_schedule = get_most_used_weekday_hourly_schedule(B_RMI, ASHRAE229,multiplier_sch)`  
            - Reset y = 0: `y = 0`
            - Check if each value in the design_cooling_multiplier_sch matches the corresponding hourly value in the get_most_used_weekday_hourly_schedule: `for x in list(design_cooling_multiplier_sch):`
                - Check if the hourly values are equal between the design_cooling_multiplier_sch and the get_most_used_weekday_hourly_schedule : `if most_used_weekday_hourly_schedule[y] != x: inf_pass_cooling = false`  
                - Add 1 to y: `y = y +1`  

            Occupany schedule check:  
            - Reset occ_pass_cooling boolean variable: `occ_pass_cooling = true` 
            - Get the multiplier schedule: `multiplier_sch = get_component_by_id(B_RMI,space.occupant_multiplier_schedule)`    
            - Get the design_cooling_multiplier_schedule: `design_cooling_multiplier_sch = multiplier_sch.cooling_design_day_sequence`  
            - Get the get_most_used_weekday_hourly_schedule (this will be a list with 24 values for each hour of a day): `most_used_weekday_hourly_schedule = get_most_used_weekday_hourly_schedule(B_RMI, ASHRAE229,multiplier_sch)`  
            - Reset y = 0: `y = 0`
            - Check if each value in the design_cooling_multiplier_sch matches the corresponding hourly value in the get_most_used_weekday_hourly_schedule: `for x in list(design_cooling_multiplier_sch):`
                - Check if the hourly values are equal between the design_cooling_multiplier_sch and the get_most_used_weekday_hourly_schedule : `if most_used_weekday_hourly_schedule[y] != x: occ_pass_cooling = false`  
                - Add 1 to y: `y = y +1`  

            Conduct checks for the interior lighting objects:  
            - Get list of interior lighting objects: `lgting_obj_list = list(space.interior_lighting)`  
            - Reset int_lgt_pass_cooling boolean variable: `int_lgt_pass_cooling = true`  
            - For each interior lighting object: `for int_lgt in lgting_obj_list:`  
                - Get the multiplier schedule: `multiplier_sch = get_component_by_id(B_RMI,int_lgt.lighting_multiplier_schedule)`  
                - Get the design_cooling_multiplier_schedule: `design_cooling_multiplier_sch = multiplier_sch.cooling_design_day_sequence`  
                - Get the get_most_used_weekday_hourly_schedule (this will be a list with 24 values for each hour of a day): `most_used_weekday_hourly_schedule = get_most_used_weekday_hourly_schedule(B_RMI, ASHRAE229,multiplier_sch)`  
                - Reset y = 0: `y = 0`
                - Check if each value in the design_cooling_multiplier_sch matches the corresponding hourly value in the get_most_used_weekday_hourly_schedule: `for x in list(design_cooling_multiplier_sch):`
                    - Check if the hourly values are equal between the design_cooling_multiplier_sch and the get_most_used_weekday_hourly_schedule : `if most_used_weekday_hourly_schedule[y] != x: int_lgt_pass_cooling = false`  
                    - Add 1 to y: `y = y +1`  

            Conduct checks for the miscellaneous objects:  
            - Get list of misc equipment objects: `misc_obj_list = list(space.miscellaneous_equipment)`      
            - Reset misc_pass_cooling boolean variable: `misc_pass_cooling = true`   
            - For each misc equipment object: `for misc in misc_obj_list:`  
                - Get the multiplier schedule: `multiplier_sch = get_component_by_id(B_RMI,misc.multiplier_schedule)`  
                - Get the design_cooling_multiplier_schedule: `design_cooling_multiplier_sch = multiplier_sch.cooling_design_day_sequence`  
                - Get the get_most_used_weekday_hourly_schedule (this will be a list with 24 values for each hour of a day): `most_used_weekday_hourly_schedule = get_most_used_weekday_hourly_schedule(B_RMI, ASHRAE229,multiplier_sch)`  
                - Reset y = 0: `y = 0`
                - Check if each value in the design_cooling_multiplier_sch matches the corresponding hourly value in the get_most_used_weekday_hourly_schedule: `for x in list(design_cooling_multiplier_sch):`
                    - Check if the hourly values are equal between the design_cooling_multiplier_sch and the get_most_used_weekday_hourly_schedule : `if most_used_weekday_hourly_schedule[y] != x: misc_pass_cooling = false`  
                    - Add 1 to y: `y = y +1`  

        - **Rule Assertion:** 
        - Case 1: If lighting or ventilation space type is dwelling unit and all schedules pass per above then pass: `if space_lighting_space_type_is_dwelling_unit = true and all(inf_pass_cooling,occ_pass_cooling,int_lgt_pass_cooling,misc_pass_cooling) == true: outcome = "PASS"`  
        - Case 2: elif the lighting or ventilation space type is NOT defined and (the building area type was not defined or the building area type is multifamily, dormitory, or hotel/motel) then outcome is UNDETERMINED: `elif space_lighting_or_vent_space_type_is_defined == false and (bldg_area_is_defined == false or building_area_is_MF_dormitory_or_hotel == true): outcome = "UNDETERMINED" and raise_message "It is not clear from the RMD if <insert space.id> is a dwelling unit. If it is a dwelling unit it is required that it be modeled following the rule that for baseline cooling sizing runs in residential dwelling units, the infiltration, occupants, lighting, gas and electricity design day cooling schedules shalled be modeled using an equipment hourly schedule that is the same as the most used hourly weekday schedule from the annual simulation. This rule <insert "was" if all(inf_pass_cooling,occ_pass_cooling,int_lgt_pass_cooling,misc_pass_cooling) == true and insert "was not" if all(inf_pass_cooling,occ_pass_cooling,int_lgt_pass_cooling,misc_pass_cooling) == false> followed for this space if applicable."` ` 
        - Case 3: elif lighting or ventilation space type is dwelling unit and not all schedules do not pass per above then Fail: `elif space_lighting_space_type_is_dwelling_unit = true and all(inf_pass_cooling,occ_pass_cooling,int_lgt_pass_cooling,misc_pass_cooling) == false: outcome = "FAIL" and raise_message "<insert space.id> does not appear to have been modeled following the rule that for baseline cooling sizing runs in residential dwelling units hourly schedules shall be the same as the most used hourly weekday schedule from the annual simulation for the following schedules: <include "infiltration" if inf_pass_cooling == false> , <include "occupants" if occ_pass_cooling == false>, <include "lighting" if int_lgt_pass_cooling == false>, <include "gas and/or electricity miscellaneous" if misc_pass_cooling ==  false>."` 
        - Case 4: Else, outcome is NOT_APPLICABLE: `Else: outcome = "NOT_APPLICABLE"`  


**Notes/Questions:**  
1. Jason plans to add .cooling_design_day_sequence to the schema.  

**[Back](../_toc.md)**