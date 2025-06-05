# is_baseline_system_1  

**Description:** Get either Sys-1, Sys-1a, Sys-1b, Sys-1c, or Not_Sys_1 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 1 (PTAC), system 1a (system 1 with purchased CHW), system 1b (system 1 with purchased heating), system 1c (system 1 with purchased CHW and purchased HW).  

**Inputs:**  
- **B-RMR**: To evaluate if the hvac system is modeled as either Sys-1, Sys-1a, Sys-1b, Sys-1c, or Not_Sys_1 in the B_RMR.   
- **hvac_b.id**: The id of the hvac system to evaluate.  

**Returns:**  
- **is_baseline_system_1**: The function returns either Sys-1, Sys-1a, Sys-1b, Sys-1c, or Not_Sys_1 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 1 (PTAC), system 1a (system 1 with purchased CHW), system 1b (system 1 with purchased heating), system 1c (system 1 with purchased CHW and purchased HW).  
 
**Function Call:** 
2. is_heating_type_fluid_loop()
3. is_cooling_type_DX()
4. serves_single_zone()  
5. is_fan_CV()  
6. is_fluid_loop_attached_to_boiler()
7. is_fluid_loop_purchased_heating()
8. is_fluid_loop_purchased_CHW()
9. is_cooling_type_fluid_loop()
10. are_all_terminal_heat_sources_none_or_null()  
11. are_all_terminal_cool_sources_none_or_null() 
12. are_all_terminal_fans_null()  
13. are_all_terminal_types_CAV()  
14. are_all_terminal_types_four_pipe()  
15. are_all_terminal_supplies_ducted()  
16. get_terminal_unit_for_SZ_baseline_HVAC()  
17. are_all_terminal_heat_sources_hot_water()  
18. are_all_terminal_cool_sources_chilled_water()  

I deleted the first function and didn't think it was crucial to update the subsequent numbering. 
 

## Logic:    
- Create an object associated with the hvac system: `hvac_b = hvac_b.id`  
- Check that there is no preheat system (it equals Null), if there is none then carry on: `if Len(hvac_b.preheat_system) == Null:`  
    - Check if heatingsystem is a fluid_loop, if it is then carry on: `if is_heating_type_fluid_loop(B_RMR, hvac_b.id) == TRUE:`     
        - Check if fansystem is constant volume, if yes then carry on: `if is_fan_CV(B_RMR, hvac_b.id) == TRUE:`  
            - Check if the hvac system serves a single zone, if yes carry on: `if serves_single_zone(B_RMR, hvac_b.id) == TRUE:`   
                - Get and create an object for the terminal unit associated with the zone: `terminal_b = get_terminal_unit_for_SZ_baseline_HVAC(B_RMR,hvac_b.id)`  
                - Check that the terminal unit object does not equal Null: `if terminal_b != Null:`  
                    
                    - Check that the data elements associated with the terminal unit align with system 1: `if are_all_terminal_heat_sources_none_or_null(B_RMR,terminal_b.id) ==  TRUE AND is_terminal_cool_source_none(B_RMR,terminal_b.id) == TRUE And are_all_terminal_fans_null(B_RMR,terminal_b.id) == TRUE AND are_all_terminal_supplies_ducted(B_RMR,terminal_b.id) == FALSE :`      
                        - if coolingsystem is DX and the heating fluid loop serves a boiler and the terminal type is constant volume then SYS-1: `if is_cooling_type_DX(B_RMR, hvac_b.id) == TRUE AND is_fluid_loop_attached_to_boiler(B_RMR, hvac_b.id) == TRUE AND are_all_terminal_types_CAV(B_RMR, terminal_b.id) ==  TRUE: is_baseline_system_1 = "SYS-1"`
                        - elif coolingsystem is DX and the fluid loop is purchased heating and the terminal type is constant volume then SYS-1b: `elif is_cooling_type_DX(B_RMR, hvac_b.id) == TRUE AND is_fluid_loop_purchased_heating(B_RMR, hvac_b.id) == TRUE AND are_all_terminal_types_CAV(B_RMR, terminal_b.id) ==  TRUE: is_baseline_system_1 = "SYS-1b"`
                        - elif the cooling system is a fluid loop and terminal type is four pipe: `elif is_cooling_type_fluid_loop(B_RMR, hvac_b.id) == TRUE AND are_all_terminal_types_four_pipe(B_RMR, terminal_b.id) == TRUE:` 
                            - if the cooling system is purchased CHW and heating fluid loop serves a boiler then SYS-1a: `if is_fluid_loop_purchased_CHW(B_RMR, hvac_b.id) == TRUE AND is_fluid_loop_attached_to_boiler(B_RMR, hvac_b.id) == TRUE: is_baseline_system_1 = "SYS-1a"`
                            - elif the cooling system is purchased CHW and heating system is purchased heating then SYS-1c: `if is_fluid_loop_purchased_CHW(B_RMR, hvac_b.id) == TRUE AND is_fluid_loop_purchased_heating(B_RMR, hvac_b.id) == TRUE: is_baseline_system_1 = "SYS-1c"`
                            - Else, is_baseline_system_1 = "Not_Sys_1": `is_baseline_system_1 = Not_Sys_1`  
                    - Else, is_baseline_system_1 = "Not_Sys_1": `is_baseline_system_1 = Not_Sys_1`
            - Else, is_baseline_system_1 = "Not_Sys_1": `is_baseline_system_1 = Not_Sys_1`
        - Else, is_baseline_system_1 = "Not_Sys_1": `is_baseline_system_1 = Not_Sys_1`
    - Else, is_baseline_system_1 = "Not_Sys_1": `is_baseline_system_1 = Not_Sys_1`
- Else, is_baseline_system_1 = "Not_Sys_1": `is_baseline_system_1 = Not_Sys_1`


**Returns** `is_baseline_system_1`  



**[Back](../_toc.md)**