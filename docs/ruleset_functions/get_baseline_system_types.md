
# get_baseline_system_types


**Description:**  Identify all the baseline system types modeled in a B-RMR.

**Inputs:**
- **B-RMR**: The B-RMR that needs to get the list of all HVAC system types.

**Returns:**  
- **baseline_hvac_system_dictionary**: A dictionary that saves all baseline HVAC system types in B-RMR with their IDs, i.e. {"SYS-3": ["hvac_id_1", "hvac_id_10"], "SYS-7A": ["hvac_id_3", "hvac_id_17", "hvac_id_6], "SYS-9": ["hvac_id_2"]}

**Function Call:** 
1. is_baseline_system_1()  


## Logic:  
- For each HVAC system in the B_RMR: `hvac_b in B_RMR..HeatingVentilationAirConditioningSystem:`    
    Declare empty lists of the hvac_b.id associated with each system type in the B_RMR. 
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
    - Declare a list for SYS-5b, DX and PHW: `SYS-5 = []`  
    - Declare a list for SYS-6, Packaged Rooftop VAV with Parallel Fan-Powered Boxes and Reheat: `SYS-6 = []`  
    - Declare a list for SYS-6b, DX and PHW: `SYS-6 = []`  
    - Declare a list for SYS-7, VAV with reheat: `SYS-7 = []`  
    - Declare a list for SYS-7a, PCHW with HW boiler: `SYS-7a = []`  
    - Declare a list for SYS-7b, CHW with PHW: `SYS-7b = []`  
    - Declare a list for SYS-7c, PCHW and PHW: `SYS-7c = []`  
    - Declare a list for SYS-8, VAV with Parallel Fan-Powered Boxes and Reheat: `SYS-8 = []`  
    - Declare a list for SYS-8a, PCHW with Electric Resistance: `SYS-8a = []`  
    - Declare a list for SYS-8b, CHW with PHW: `SYS-8b = []`  
    - Declare a list for SYS-9, Heating and Ventilation w/Furnace: `SYS-9 = []`  
    - Declare a list for SYS-9b, PHW: `SYS-9b = []`  
    - Declare a list for SYS-10, Heating and Ventilation w/Electric: `SYS-10 = []`  
    - Declare a list for SYS-11.1, Single Zone VAV System with CHW and Electric Heat : `SYS-11.1 = []`  
    - Declare a list for SYS-11.1a, Single Zone VAV System with PCHW and Electric Heat : `SYS-11.1a = []`  
    - Declare a list for SYS-11b, Single Zone VAV System with CHW and PHW : `SYS-11b = []`  
    - Declare a list for SYS-11c, Single Zone VAV System with PCHW and PHW : `SYS-11c = []`  
    - Declare a list for SYS-11.2, Single Zone VAV System with CHW and HW boiler : `SYS-11.2 = []`  
    - Declare a list for SYS-11.2a, Single Zone VAV System with PCHW and HW boiler : `SYS-11.2a = []`  
    - Declare a list for SYS-12, Single Zone Constant Volume System with CHW and HW boiler : `SYS-12 = []`  
    - Declare a list for SYS-12a, PCHW with HW boiler: `SYS-12a = []`  
    - Declare a list for SYS-12b, CHW with PHW: `SYS-12b = []`  
    - Declare a list for SYS-12c, PCHW and PHW: `SYS-12c = []`  
    - Declare a list for SYS-13, Single Zone Constant Volume System with CHW and Electric Heat : `SYS-13 = []`  
    - Declare a list for SYS-13a, PCHW with and Electric Heat: `SYS-13a = []`  
    - Declare a list for SYS-13b, CHW with PHW: `SYS-13b = []`  How does this differ from 12b?
    - Declare a list for SYS-13c, PCHW and PHW: `SYS-13c = []`  How does this difffer from 12c?


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
| Sys-6 Package VAV with PFP Boxes | Packaged Rooftop VAV with Parallel Fan-Powered Boxes and Reheat | DX           | ER           | Sys-8a: VAV with PFP Boxes, PCHW w/ ER  | Sys-6b: Package VAV with PFP Boxes, w/ DX and PHW | Sys-7c: VAV with Reheat with PHW and PCHW |
| Sys-7 VAV with Reheat            | VAV with Reheat                                                 | CHW          | Boiler       | Sys-7a: VAV with Reheat, PCHW w/ Boiler | Sys-7b: VAV with Reheat, w/ CHW and PHW           | Sys-7c: VAV with Reheat with PHW and PCHW |
| Sys-8 VAV with PFP Boxes         | VAV with Parallel Fan-Powered Boxes and Reheat                  | CHW          | ER           | Sys-8a: VAV with PFP Boxes, PCHW w/ ER  | Sys-8b: VAV with PFP Boxes, w/ CHW and PHW        | Sys-7c: VAV with Reheat with PHW and PCHW |
| Sys-9 HV gas-fired               | Heating and Ventilation                                         | None         | Furnace      | Sys-9: HV (No Changes)                  | Sys-9b: HV (PHW)                                  | Sys-9b: HV (PHW)                          |
| Sys-10 HV electrical             | Heating and Ventilation                                         | None         | ER           | Sys-9: HV (No Changes)                  | Sys-9b: HV (PHW)                                  | Sys-9b: HV (PHW)                          |
| Sys-11.1 SZ-VAV                    | Single Zone VAV System                                          | CHW          | ER | Sys-11.1a: SZ-VAV w/ PCHW and ER    | Sys-11b SZ-VAV, w/ CHW and PHW                    | Sys-11c: SZ-VAV with PHW and PCHW         |
| Sys-11.2 SZ-VAV                    | Single Zone VAV System                                          | CHW          | Boiler | Sys-11.2a: SZ-VAV w/ PCHW and Boiler    | Sys-11b SZ-VAV, w/ CHW and PHW                    | Sys-11c: SZ-VAV with PHW and PCHW         |
| Sys-12 SZ-CV-HW                  | Single Zone Constant Volume System                              | CHW          | Boiler       | Sys-12a: SZ-CV, w/ PCHW + Boiler        | Sys-12b SZ-CV-HW, w/ CHW and PHW                  | Sys-12c: SZ-CV with PHW and PCHW          |
| Sys-13 SZ-CV-ER                  | Single Zone Constant Volume System                              | CHW          | ER           | Sys-13a: SZ-CV, PCHW w/ ER              | Sys-13b SZ-CV-ER, w/ CHW and PHW                  | Sys-13c: SZ-CV with PHW and PCHW          |


2. We can use multiple functions, one for each baseline HVAC system type as shown below. The return values will be TRUE or FALSE. :
is_baseline_system_1(HVAC_id)
is_baseline_system_2(HVAC_id)

Then "get_baseline_HVAC_system_types" would call these sub-functions to come up with the baseline system library.


**[Back](../_toc.md)**