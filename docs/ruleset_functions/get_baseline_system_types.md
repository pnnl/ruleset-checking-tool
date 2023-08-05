
# get_baseline_system_types

**Schema Version:** 0.0.23
**Description:**  Identify all the baseline system types modeled in a B-RMR.

**Inputs:**
- **B-RMR**: The B-RMR that needs to get the list of all HVAC system types.

**Returns:**  
- **baseline_hvac_system_dictionary**: A dictionary that saves all baseline HVAC system types in B-RMR with their IDs, i.e. {"SYS-3": ["hvac_id_1", "hvac_id_10"], "SYS-7A": ["hvac_id_3", "hvac_id_17", "hvac_id_6], "SYS-9": ["hvac_id_2"]}

**Function Call:** 
1. get_dict_of_zones_and_terminal_units_served_by_hvac_sys()      
2. is_baseline_system_1()  
3. is_baseline_system_2()  
4. is_baseline_system_3()  
5. is_baseline_system_4()  
6. is_baseline_system_5()  
7. is_baseline_system_6()  
8. is_baseline_system_7()  
9. is_baseline_system_8()  
10. is_baseline_system_9()  
11. is_baseline_system_10()  
12. is_baseline_system_11.1()  
13. is_baseline_system_11.2()  
14. is_baseline_system_12() 
15. is_baseline_system_13()
16. get_dict_with_terminal_units_and_zones ()
 

## Logic:   
Below is so that the looping associated with get_dict_of_zones_and_terminal_units_served_by_hvac_sys() does not have to be repeated for each relevant function which would be highly inefficient since it loops through all zones in the B_RMR.
- Get dictionary of zones and terminal unit IDs associated with each HVAC system in the RMR to pass to the sub functions: `dict_of_zones_and_terminal_units_served_by_hvac_sys  = get_dict_of_zones_and_terminal_units_served_by_hvac_sys(B_RMR)`  
- Get dictionary of zones associated with each terminal unit: `dict_with_terminal_units_and_zones = get_dict_with_terminal_units_and_zones(B_RMR)`  
Declare empty lists of the hvac_b.id associated with each system type in the B_RMR (This declaration is not needed but it helps to identify everything needed to make sure its all been covered) 
- Declare a list for SYS-1, Packaged Terminal Air Conditioner : `SYS-1 = []`  
- Declare a list for SYS-1a, PCHW with HW boiler: `SYS-1a = []` 
- Declare a list for SYS-1b, DX cooling with PHW: `SYS-1b = []` 
- Declare a list for SYS-1c, PCHW and PHW: `SYS-1c = []` 
- Declare a list for SYS-2,  Packaged Terminal Heat Pump (all SYS-2 scenarios with purchased CHW or HW (PCHW/PHW) turn into one of the 3 SYS-1s with PCHW/PHW): `SYS-2 = []` 
- Declare a list for SYS-3, Packaged Rooftop Air Conditioner: `SYS-3 = []`  
- Declare a list for SYS-3a, PCHW with furnace: `SYS-3a = []`  
- Declare a list for SYS-3b, DX cooling with PHW: `SYS-3b = []`  
- Declare a list for SYS-3c, PCHW and PHW: `SYS-3c = []`  
- Declare a list for SYS-4, Packaged Rooftop Heat Pump (all SYS-4 scenarios with PCHW/PHW turn into one of the 3 SYS-3s with PCHW/PHW ): `SYS-4 = []`  
- Declare a list for SYS-5, Packaged Rooftop VAV with Reheat: `SYS-5 = []`  
- Declare a list for SYS-5b, DX and PHW: `SYS-5b = []`  
- Declare a list for SYS-6, Packaged Rooftop VAV with Parallel Fan-Powered Boxes and Reheat: `SYS-6 = []`  
- Declare a list for SYS-6b, DX and PHW: `SYS-6b = []`  
- Declare a list for SYS-7, VAV with reheat: `SYS-7 = []`  
- Declare a list for SYS-7a, PCHW with HW boiler: `SYS-7a = []`  
- Declare a list for SYS-7b, CHW with PHW: `SYS-7b = []`  
- Declare a list for SYS-7c, PCHW and PHW: `SYS-7c = []`  
- Declare a list for SYS-8, VAV with Parallel Fan-Powered Boxes and Reheat: `SYS-8 = []`  
- Declare a list for SYS-8a, PCHW with Electric Resistance: `SYS-8a = []`  
- Declare a list for SYS-8b, CHW with PHW: `SYS-8b = []`  
- Declare a list for SYS-8c, CHW with PHW: `SYS-8c = []`  Change made by CML because 7c does not have fan power boxes
- Declare a list for SYS-9, Heating and Ventilation w/Furnace: `SYS-9 = []`  
- Declare a list for SYS-9b, PHW: `SYS-9b = []`  
- Declare a list for SYS-10, Heating and Ventilation w/Electric: `SYS-10 = []`  
- Declare a list for SYS-11_1, Single Zone VAV System with CHW and Electric Heat : `SYS-11_1 = []`  
- Declare a list for SYS-11_1a, Single Zone VAV System with PCHW and Electric Heat : `SYS-11_1a = []`  
- Declare a list for SYS-11b, Single Zone VAV System with CHW and PHW : `SYS-11b = []`  
- Declare a list for SYS-11c, Single Zone VAV System with PCHW and PHW : `SYS-11c = []`  
- Declare a list for SYS-11_2, Single Zone VAV System with CHW and HW boiler : `SYS-11_2 = []`  
- Declare a list for SYS-11_2a, Single Zone VAV System with PCHW and HW boiler : `SYS-11_2a = []`  
- Declare a list for SYS-12, Single Zone Constant Volume System with CHW and HW boiler : `SYS-12 = []`  
- Declare a list for SYS-12a, PCHW with HW boiler: `SYS-12a = []`  
- Declare a list for SYS-12b, CHW with PHW: `SYS-12b = []`  
- Declare a list for SYS-12c, PCHW and PHW: `SYS-12c = []`  
- Declare a list for SYS-13, Single Zone Constant Volume System with CHW and Electric Heat : `SYS-13 = []`  
- Declare a list for SYS-13a, PCHW with and Electric Heat: `SYS-13a = []`  


- For each HVAC system in the B_RMR: `hvac_b in B_RMR..HeatingVentilatingAirConditioningSystem:`   
    - Get list of terminal units associated with the hvac system from the dictionary input to the function: `terminal_unit_id_list = dict_of_zones_and_terminal_units_served_by_hvac_sys[hvac_b.id]["Terminal_Unit_List"]`  
    - Get list of zone ids associated with the hvac system from the dictionary input to the function: `zone_id_list = dict_of_zones_and_terminal_units_served_by_hvac_sys[hvac_b.id]["Zone_List"]` 
    - Reset HVAC system type found boolean variable to FALSE: `hvac_sys_type_found = FALSE`  
    - Reset terminal_units_serve_one_zone boolean variable to TRUE: `terminal_units_serve_one_zone = TRUE` 
    - Loop through each terminal to ensure each terminal serves one zone: `for terminal in terminal_unit_id_list:` 
        - Check if the terminal unit serves 1 zone: `if len(list(dict_with_terminal_units_and_zones[terminal]["Zone_List"])) != 1`  
        - Set boolean variable to false: `terminal_units_serve_one_zone = FALSE`   
    - Check if all the terminal units serve one zone via the boolean variable: `if terminal_units_serve_one_zone == TRUE:`  
        - Call system type 1 function which will return a string of either SYS-1, SYS-1a, SYS-1b, SYS-1c, or Not_Sys_1: `sys_1_type = is_baseline_system_1(B_RMR, hvac_b.id,terminal_unit_id_list,zone_id_list)`  
        - Check if SYS-1, if it is then add to list of SYS-1s: `if sys_1_type == "SYS-1": SYS-1 = SYS-1.append(hvac_b.id)` 
        - Check elif SYS-1a, if it is then add to list of SYS-1as: `elif sys_1_type == "SYS-1a": SYS-1a = SYS-1a.append(hvac_b.id)`
        - Check elif SYS-1b, if it is then add to list of SYS-1bs: `elif sys_1_type == "SYS-1b": SYS-1b = SYS-1b.append(hvac_b.id)`
        - Check elif SYS-1c, if it is then add to list of SYS-1cs: `elif sys_1_type == "SYS-1c": SYS-1c = SYS-1c.append(hvac_b.id)`
        - Else, do nothing: `Else:`
        - Check if sys_1_type does not equal Not_Sys_1: `if sys_1_type != "Not_Sys_1": hvac_sys_type_found = TRUE`  
        - Check if hvac_sys_type_found = FALSE, if it does carry on if it equals TRUE then loop to the next hvac system: `if hvac_sys_type_found == FALSE:` 
            - Call system type 2 function which will return a string of either SYS-2 or Not_Sys_2: `sys_2_type = is_baseline_system_2(B_RMR, hvac_b.id,terminal_unit_id_list,zone_id_list)`  
            - Check if SYS-2, if it is then add to list of SYS-2s: `if sys_2_type == "SYS-2": SYS-2 = SYS-2.append(hvac_b.id)` 
            - Check if sys_2_type does not equal Not_Sys_2: `if sys_2_type != "Not_Sys_2": hvac_sys_type_found = TRUE`  
            - Check if hvac_sys_type_found = FALSE, if it does carry on if it equals TRUE then loop to the next hvac system: `if hvac_sys_type_found == FALSE:` 
                - Call system type 3 function which will return a string of either SYS-3, SYS-3a, SYS-3b, SYS-3c, or Not_Sys_3: `sys_3_type = is_baseline_system_3(B_RMR, hvac_b.id,terminal_unit_id_list,zone_id_list)`  
                - Check if SYS-3, if it is then add to list of SYS-3s: `if sys_3_type == "SYS-3": SYS-3 = SYS-3.append(hvac_b.id)` 
                - Check elif SYS-3a, if it is then add to list of SYS-3as: `elif sys_3_type == "SYS-3a": SYS-3a = SYS-3a.append(hvac_b.id)`
                - Check elif SYS-3b, if it is then add to list of SYS-3bs: `elif sys_3_type == "SYS-3b": SYS-3b = SYS-3b.append(hvac_b.id)`
                - Check elif SYS-3c, if it is then add to list of SYS-3cs: `elif sys_3_type == "SYS-3c": SYS-3c = SYS-3c.append(hvac_b.id)`
                - Else, do nothing: `Else:`
                - Check if sys_3_type does not equal Not_Sys_3: `if sys_3_type != "Not_Sys_3": hvac_sys_type_found = TRUE`  
                - Check if hvac_sys_type_found = FALSE, if it does carry on if it equals TRUE then loop to the next hvac system: `if hvac_sys_type_found == FALSE:` 
                    - Call system type 4 function which will return a string of either SYS-4 or Not_Sys_4: `sys_4_type = is_baseline_system_4(B_RMR, hvac_b.id,terminal_unit_id_list,zone_id_list)`  
                    - Check if SYS-4, if it is then add to list of SYS-4s: `if sys_4_type == "SYS-4": SYS-4 = SYS-4.append(hvac_b.id)` 
                    - Check if sys_4_type does not equal Not_Sys_4: `if sys_4_type != "Not_Sys_4": hvac_sys_type_found = TRUE`  
                    - Check if hvac_sys_type_found = FALSE, if it does carry on if it equals TRUE then loop to the next hvac system: `if hvac_sys_type_found == FALSE:` 
                        - Call system type 5 function which will return a string of either SYS-5, SYS-5b, or Not_Sys_5: `sys_5_type = is_baseline_system_5(B_RMR, hvac_b.id,terminal_unit_id_list,zone_id_list)`  
                        - Check if SYS-5, if it is then add to list of SYS-5s: `if sys_5_type == "SYS-5": SYS-5 = SYS-5.append(hvac_b.id)` 
                        - Check elif SYS-5b, if it is then add to list of SYS-5bs: `elif sys_5_type == "SYS-5b": SYS-5b = SYS-5b.append(hvac_b.id)`
                        - Else, do nothing: `Else:`
                        - Check if sys_5_type does not equal Not_Sys_5: `if sys_5_type != "Not_Sys_5": hvac_sys_type_found = TRUE`  
                        - Check if hvac_sys_type_found = FALSE, if it does carry on if it equals TRUE then loop to the next hvac system: `if hvac_sys_type_found == FALSE:` 
                            - Call system type 6 function which will return a string of either SYS-6, SYS-6b, or Not_Sys_6: `sys_6_type = is_baseline_system_6(B_RMR, hvac_b.id,terminal_unit_id_list,zone_id_list)`  
                            - Check if SYS-6, if it is then add to list of SYS-6s: `if sys_6_type == "SYS-6": SYS-6 = SYS-6.append(hvac_b.id)` 
                            - Check elif SYS-6b, if it is then add to list of SYS-6bs: `elif sys_6_type == "SYS-6b": SYS-6b = SYS-6b.append(hvac_b.id)`
                            - Else, do nothing: `Else:`
                            - Check if sys_6_type does not equal Not_Sys_6: `if sys_6_type != "Not_Sys_6": hvac_sys_type_found = TRUE`  
                            - Check if hvac_sys_type_found = FALSE, if it does carry on if it equals TRUE then loop to the next hvac system: `if hvac_sys_type_found == FALSE:` 
                                - Call system type 7 function which will return a string of either SYS-7, SYS-7a, SYS-7b, SYS-7c, or Not_Sys_7: `sys_7_type = is_baseline_system_7(B_RMR, hvac_b.id,terminal_unit_id_list,zone_id_list)`  
                                - Check if SYS-7, if it is then add to list of SYS-7s: `if sys_7_type == "SYS-7": SYS-7 = SYS-7.append(hvac_b.id)` 
                                - Check elif SYS-7a, if it is then add to list of SYS-7as: `elif sys_7_type == "SYS-7a": SYS-7a = SYS-7a.append(hvac_b.id)`
                                - Check elif SYS-7b, if it is then add to list of SYS-7bs: `elif sys_7_type == "SYS-7b": SYS-7b = SYS-7b.append(hvac_b.id)`
                                - Check elif SYS-7c, if it is then add to list of SYS-7cs: `elif sys_7_type == "SYS-7c": SYS-7c = SYS-7c.append(hvac_b.id)`
                                - Else, do nothing: `Else:`
                                - Check if sys_7_type does not equal Not_Sys_7: `if sys_7_type != "Not_Sys_7": hvac_sys_type_found = TRUE`  
                                - Check if hvac_sys_type_found = FALSE, if it does carry on if it equals TRUE then loop to the next hvac system: `if hvac_sys_type_found == FALSE:` 
                                    - Call system type 8 function which will return a string of either SYS-8, SYS-8a, SYS-8b, SYS-8c, or Not_Sys_8: `sys_8_type = is_baseline_system_8(B_RMR, hvac_b.id,terminal_unit_id_list,zone_id_list)`  
                                    - Check if SYS-8, if it is then add to list of SYS-8s: `if sys_8_type == "SYS-8": SYS-8 = SYS-8.append(hvac_b.id)` 
                                    - Check elif SYS-8a, if it is then add to list of SYS-8as: `elif sys_8_type == "SYS-8a": SYS-8a = SYS-8a.append(hvac_b.id)`
                                    - Check elif SYS-8b, if it is then add to list of SYS-8bs: `elif sys_8_type == "SYS-8b": SYS-8b = SYS-8b.append(hvac_b.id)`
                                    - Check elif SYS-8c, if it is then add to list of SYS-8cs: `elif sys_8_type == "SYS-8c": SYS-8c = SYS-8c.append(hvac_b.id)`
                                    - Else, do nothing: `Else:`
                                    - Check if sys_8_type does not equal Not_Sys_8: `if sys_8_type != "Not_Sys_8": hvac_sys_type_found = TRUE`  
                                    - Check if hvac_sys_type_found = FALSE, if it does carry on if it equals TRUE then loop to the next hvac system: `if hvac_sys_type_found == FALSE:` 
                                        - Call system type 9 function which will return a string of either SYS-9, SYS-9b, or Not_Sys_9: `sys_9_type = is_baseline_system_9(B_RMR, hvac_b.id,terminal_unit_id_list,zone_id_list)`  
                                        - Check if SYS-9, if it is then add to list of SYS-9s: `if sys_9_type == "SYS-9": SYS-9 = SYS-9.append(hvac_b.id)` 
                                        - Check elif SYS-9b, if it is then add to list of SYS-9bs: `elif sys_9_type == "SYS-9b": SYS-9b = SYS-9b.append(hvac_b.id)`
                                        - Else, do nothing: `Else:`
                                        - Check if sys_9_type does not equal Not_Sys_9: `if sys_9_type != "Not_Sys_9": hvac_sys_type_found = TRUE`  
                                        - Check if hvac_sys_type_found = FALSE, if it does carry on if it equals TRUE then loop to the next hvac system: `if hvac_sys_type_found == FALSE:` 
                                            - Call system type 10 function which will return a string of either SYS-10 or Not_Sys_10: `sys_10_type = is_baseline_system_10(B_RMR, hvac_b.id,terminal_unit_id_list,zone_id_list)`  
                                            - Check if SYS-10, if it is then add to list of SYS-10s: `if sys_10_type == "SYS-10": SYS-10 = SYS-10.append(hvac_b.id)` 
                                            - Check if sys_10_type does not equal Not_Sys_10: `if sys_10_type != "Not_Sys_10": hvac_sys_type_found = TRUE`  
                                            - Check if hvac_sys_type_found = FALSE, if it does carry on if it equals TRUE then loop to the next hvac system: `if hvac_sys_type_found == FALSE:` 
                                                - Call system type 11.1 function which will return a string of either SYS-11.1, SYS-11.1a, SYS-11b, SYS-11c, or Not_Sys_11.1: `sys_11.1_type = is_baseline_system_11.1(B_RMR, hvac_b.id,terminal_unit_id_list,zone_id_list)`  
                                                - Check if SYS-11.1, if it is then add to list of SYS-11.1s: `if sys_11.1_type == "SYS-11.1": SYS-11_1 = SYS-11_1.append(hvac_b.id)` 
                                                - Check elif SYS-11.1a, if it is then add to list of SYS-11.1as: `elif sys_11.1_type == "SYS-11.1a": SYS-11_1a = SYS-11_1a.append(hvac_b.id)`
                                                - Check elif SYS-11b, if it is then add to list of SYS-11bs: `elif sys_11.1_type == "SYS-11b": SYS-11b = SYS-11b.append(hvac_b.id)`
                                                - Check elif SYS-11c, if it is then add to list of SYS-11cs: `elif sys_11.1_type == "SYS-11c": SYS-11c = SYS-11c.append(hvac_b.id)`
                                                - Else, do nothing: `Else:`
                                                - Check if sys_11.1_type does not equal Not_Sys_11.1: `if sys_11.1_type != "Not_Sys_11.1": hvac_sys_type_found = TRUE`  
                                                - Check if hvac_sys_type_found = FALSE, if it does carry on if it equals TRUE then loop to the next hvac system: `if hvac_sys_type_found == FALSE:` 
                                                    - Call system type 11.2 function which will return a string of either SYS-11.2, SYS-11.2a, or Not_Sys_11.2: `sys_11.2_type = is_baseline_system_11.2(B_RMR, hvac_b.id,terminal_unit_id_list,zone_id_list)`  
                                                    - Check if SYS-11.2, if it is then add to list of SYS-11.2s: `if sys_11.2_type == "SYS-11.2": SYS-11_2 = SYS-11_2.append(hvac_b.id)` 
                                                    - Check elif SYS-11.2a, if it is then add to list of SYS-11.2as: `elif sys_11.2_type == "SYS-11.2a": SYS-11_2a = SYS-11_2a.append(hvac_b.id)`
                                                    - Else, do nothing: `Else:`
                                                    - Check if sys_11.2_type does not equal Not_Sys_11.2: `if sys_11.2_type != "Not_Sys_11.2": hvac_sys_type_found = TRUE`  
                                                    - Check if hvac_sys_type_found = FALSE, if it does carry on if it equals TRUE then loop to the next hvac system: `if hvac_sys_type_found == FALSE:` 
                                                        - Call system type 12 function which will return a string of either SYS-12, SYS-12a, SYS-12b, SYS-12c, or Not_Sys_12: `sys_12_type = is_baseline_system_12(B_RMR, hvac_b.id,terminal_unit_id_list,zone_id_list)`  
                                                        - Check if SYS-12, if it is then add to list of SYS-12s: `if sys_12_type == "SYS-12": SYS-12 = SYS-12.append(hvac_b.id)` 
                                                        - Check elif SYS-12a, if it is then add to list of SYS-12as: `elif sys_12_type == "SYS-12a": SYS-12a = SYS-12a.append(hvac_b.id)`
                                                        - Check elif SYS-12b, if it is then add to list of SYS-12bs: `elif sys_12_type == "SYS-12b": SYS-12b = SYS-12b.append(hvac_b.id)`
                                                        - Check elif SYS-12c, if it is then add to list of SYS-12cs: `elif sys_12_type == "SYS-12c": SYS-12c = SYS-12c.append(hvac_b.id)`
                                                        - Else, do nothing: `Else:`
                                                        - Check if sys_12_type does not equal Not_Sys_12: `if sys_12_type != "Not_Sys_12": hvac_sys_type_found = TRUE`  
                                                        - Check if hvac_sys_type_found = FALSE, if it does carry on if it equals TRUE then loop to the next hvac system: `if hvac_sys_type_found == FALSE:` 
                                                            - Call system type 12 function which will return a string of either SYS-13, SYS-13a, or Not_Sys_13: `sys_13_type = is_baseline_system_13(B_RMR, hvac_b.id,terminal_unit_id_list,zone_id_list)`  
                                                            - Check if SYS-13, if it is then add to list of SYS-13s: `if sys_13_type == "SYS-13": SYS-13 = SYS-13.append(hvac_b.id)` 
                                                            - Check elif SYS-13a, if it is then add to list of SYS-13as: `elif sys_13_type == "SYS-13a": SYS-13a = SYS-13a.append(hvac_b.id)`  
                                                            - Else, do nothing: `Else:`
                                                            - Check if sys_13_type does not equal Not_Sys_13: `if sys_13_type != "Not_Sys_13": hvac_sys_type_found = TRUE`  
                                                            - Check if hvac_sys_type_found = FALSE, if it does carry on if it equals TRUE then loop to the next hvac system: `if hvac_sys_type_found == FALSE:` 


- Create dictionary after looping through each HVAC system from lists:`baseline_hvac_system_dictionary = {"SYS-1": [SYS-1], "SYS-1a": [SYS-1a],"SYS-1b": [SYS-1b],"SYS-1c": [SYS-1c],"SYS-2": [SYS-2],"SYS-3",[SYS-3], "SYS-3a": [SYS-3a],"SYS-3b": [SYS-3b],"SYS-1c": [SYS-3c],"SYS-4": [SYS-4],"SYS-5": [SYS-5],"SYS-5b": [SYS-5b],"SYS-6": [SYS-6],"SYS-6b": [SYS-6b], "SYS-7": [SYS-7], "SYS-7a": [SYS-7a],"SYS-7b": [SYS-7b],"SYS-1c": [SYS-7c],"SYS-8": [SYS-8], "SYS-8a": [SYS-1a],"SYS-8b": [SYS-8b],"SYS-8c": [SYS-8c],"SYS-9": [SYS-9], "SYS-9b": [SYS-9b],"SYS-10": [SYS-10], "SYS-11.1": [SYS-11_1], "SYS-11.1a": [SYS-11_1a],"SYS-11b": [SYS-11b],"SYS-11c", [SYS-11c],"SYS-11.2": [SYS-11_2], "SYS-11.2a": [SYS-11_2a], "SYS-12": [SYS-12], "SYS-12a": [SYS-12a],"SYS-12b": [SYS-12b],"SYS-12c": [SYS-12c], "SYS-13": [SYS-13], "SYS-13a": [SYS-13a],"SYS-13b": [SYS-13b],"SYS-13c": [SYS-13c]}`

**Returns** `return baseline_hvac_system_dictionary`  

**Notes:**


1. Standard Baseline HVAC Types:
|                                  | Air-side System                                                 | Cooling Type | Heating Type | Air-side System with PCHW Only          | Air-side System with PHHW Only                    | Air-side System with PCHW & PHHW          |
|----------------------------------|-----------------------------------------------------------------|--------------|--------------|-----------------------------------------|---------------------------------------------------|-------------------------------------------|
| Sys-1 PTAC                       | Packaged Terminal Air Conditioner                               | DX           | Boiler       | Sys-1a: CV FCU, PCHW w/ Boiler          | Sys-1b: PTAC w/ DX and PHW                        | Sys-1c: CV FCU with PHW and PCHW          |
| Sys-2 PTHP                       | Packaged Terminal Heat Pump                                     | DX           | HP           | Sys-1a: CV FCU, PCHW w/ Boiler          | Sys-1b: PTAC w/ DX and PHW                        | Sys-1c: CV FCU with PHW and PCHW          |
| Sys-3 PSZ-AC                     | Packaged Rooftop Air Conditioner                                | DX           | Furnace      | Sys-3a: CV SZ AHU, PCHW w/ Furnace      | Sys-3b: PSZ w/ DX and PHW                         | Sys-3c: CV SZ AHU with PHW and PCHW       |
| Sys-4 PSZ-HP                     | Packaged Rooftop Heat Pump                                      | DX           | HP           | Sys-3a: CV SZ AHU, PCHW w/ Furnace      | Sys-3b: PSZ w/ DX and PHW                         | Sys-3c: CV SZ AHU with PHW and PCHW       |
| Sys-5 Package VAV with Reheat    | Packaged Rooftop VAV with Reheat                                | DX           | Boiler       | Sys-7a: VAV with Reheat, PCHW w/ Boiler | Sys-5b: Packaged VAV with Reheat, w/ DX and PHW   | Sys-7c: VAV with Reheat with PHW and PCHW |
| Sys-6 Package VAV with PFP Boxes | Packaged Rooftop VAV with Parallel Fan-Powered Boxes and Reheat | DX           | ER           | Sys-8a: VAV with PFP Boxes, PCHW w/ ER  | Sys-6b: Package VAV with PFP Boxes, w/ DX and PHW | Sys-8c: VAV with PFP Boxes, with PHW and PCHW |
| Sys-7 VAV with Reheat            | VAV with Reheat                                                 | CHW          | Boiler       | Sys-7a: VAV with Reheat, PCHW w/ Boiler | Sys-7b: VAV with Reheat, w/ CHW and PHW           | Sys-7c: VAV with Reheat with PHW and PCHW |
| Sys-8 VAV with PFP Boxes         | VAV with Parallel Fan-Powered Boxes and Reheat                  | CHW          | ER           | Sys-8a: VAV with PFP Boxes, PCHW w/ ER  | Sys-8b: VAV with PFP Boxes, w/ CHW and PHW        | Sys-8c: VAV with PFP Boxes, with PHW and PCHW |
| Sys-9 HV gas-fired               | Heating and Ventilation                                         | None         | Furnace      | Sys-9: HV (No Changes)                  | Sys-9b: HV (PHW)                                  | Sys-9b: HV (PHW)                          |
| Sys-10 HV electrical             | Heating and Ventilation                                         | None         | ER           | Sys-10: HV (No Changes)                  | Sys-9b: HV (PHW)                                  | Sys-9b: HV (PHW)                          |
| Sys-11.1 SZ-VAV                    | Single Zone VAV System                                          | CHW          | ER | Sys-11.1a: SZ-VAV w/ PCHW and ER    | Sys-11b SZ-VAV, w/ CHW and PHW                    | Sys-11c: SZ-VAV with PHW and PCHW         |
| Sys-11.2 SZ-VAV                    | Single Zone VAV System                                          | CHW          | Boiler | Sys-11.2a: SZ-VAV w/ PCHW and Boiler    | Sys-11b SZ-VAV, w/ CHW and PHW                    | Sys-11c: SZ-VAV with PHW and PCHW         |
| Sys-12 SZ-CV-HW                  | Single Zone Constant Volume System                              | CHW          | Boiler       | Sys-12a: SZ-CV, w/ PCHW + Boiler        | Sys-12b SZ-CV-HW, w/ CHW and PHW                  | Sys-12c: SZ-CV with PHW and PCHW          |
| Sys-13 SZ-CV-ER                  | Single Zone Constant Volume System                              | CHW          | ER           | Sys-13a: SZ-CV, PCHW w/ ER              | Sys-12b SZ-CV-ER, w/ CHW and PHW                  | Sys-12c: SZ-CV with PHW and PCHW          |





**[Back](../_toc.md)**
