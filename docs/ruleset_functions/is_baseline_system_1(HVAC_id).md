# is_baseline_system_1  

**Description:** Get either Sys-1, Sys-1a, Sys-1b, Sys-1c, or Not_Sys_1 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 1 (PTAC), system 1a (system 1 with purchased heating), system 1b (system 1 with purchased CHW), system 1c (system 1 with purchased CHW and purchased HW).  

**Inputs:**  
- **B-RMR**: To evaluate if the hvac system is modeled as either Sys-1, Sys-1a, Sys-1b, Sys-1c, or Not_Sys_1 in the B_RMR.   
- **hvac_b.id**: The id of the hvac system to evaluate.  

**Returns:**  
- **is_baseline_system_1**: The function returns either Sys-1, Sys-1a, Sys-1b, Sys-1c, or Not_Sys_1 string output which indicates whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 1 (PTAC), system 1a (system 1 with purchased heating), system 1b (system 1 with purchased CHW), system 1c (system 1 with purchased CHW and purchased HW)  
 
**Function Call:** 
1. get_hvac_zone_list_w_area()  
2. is_heating_type_fluid_loop()
3. is_cooling_type_DX()
4. serves_single_zone()  
5. is_fan_CV()  
6. is_fluid_loop_attached_to_boiler()
7. is_fluid_loop_purchased_heating()
8. is_fluid_loop_purchased_CHW()

## Logic:    
- Create an object associated with the hvac system: `hvac_b = hvac_b.id`  
- Check that there is no preheat system (it equals Null), if there is none then carry on: `if Len(hvac_b.preheat_system) == Null:`  
    - Check if heatingsystem is a fluid_loop, if it is then carry on: `if is_heating_type_fluid_loop(B_RMR, hvac_b.id) == TRUE:`     
        - Check if fansystem is constant volume, if yes then carry on: `if is_fan_CV(B_RMR, hvac_b.id) == TRUE:`  
            - Check if the hvac system serves a single zone, if yes carry on: `if serves_single_zone(B_RMR, hvac_b.id) == TRUE:`   
                - Get dictionary list of baseline zones and the associated HVAC systems: `hvac_zone_list_w_area_dict_b = get_hvac_zone_list_w_area (B_RMR)`  
                - Get list of zones that the HVAC system serves (should only be one): `zone_list_b = hvac_zone_list_w_area_dict_b[hvac_b.id]["ZONE_LIST"]`  
                - Create an object for the zone associated with the HVAC system: `zone_b = zone_list_b[0]`
                - Check that there is only one terminal unit associated with the zone, if yes then carry on with remaining logic: `if len(zone_b.terminals) == 1:`  
                    - Create an object for the terminal unit associated with the zone: `terminal_b = zone_b.terminals[0]`  
                    - Check that the data elements associated with the terminal unit align with system 1: `if (terminal_b.heating_source == "None" or terminal_b.heating_source == Null) AND (terminal_b.cooling_source == "None" or terminal_b.cooling_source == Null) And terminal_b.fan == Null AND terminal_b.type == "CONSTANT_AIR_VOLUME":`    
                        - if coolingsystem is DX and the fluid loop serves a boiler then SYS-1: `if is_cooling_type_DX(B_RMR, hvac_b.id) == TRUE AND is_fluid_loop_attached_to_boiler(B_RMR, hvac_b.id) : is_baseline_system_1 = "SYS-1"`
                        - elif


**Returns** `is_baseline_system_1`  

**Notes**
1. To limit redundant coding. I am thinking that we should also check to see if it is Sys-1, Sys-1a, Sys-1b, or Sys-1c in the same function and return strings of either Sys-1, Sys-1a, Sys-1b, Sys-1c, or Not_Sys_1.

**[Back](../_toc.md)**