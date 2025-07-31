# get_fan_system_object_supply_return_exhaust_relief_total_power_flow

**Description:** Get the supply, return, exhaust, and relief total fan power, CFM, quantity, and information about whether the pressure drop is consistent across the fans if more than one for a fan system object.   The function returns a dictionary that saves the supply, return, exhaust, and relief fan power, saves the supply, return, exhaust, and relief cfm, saves the supply, return, exhaust, and relief quantity, and saves for each fan whether the pressure drop is undefined, identical, or different across fans (if only one it will return undefined or identical) {"{fan_type}_fans_Power": value, "{fan_type}_fans_airflow": value, "{fan_type}_fans_qty": value, "{fan_type}_pressure": enums of ("IDENTICAL", "UNDEFINED", "DIFFERENT"). Values will be equal to zero where not defined for a fan system or as otherwise specified above. For airflow values this function assumes that all fans associated with the supply_fans object are in parallel (i.e., if multiple fans the cfm is additive.) but returns the quantity and information about the pressure drop across fans to help assess whether series or parallel.

**Inputs:**  
- **fan_system_obj**: The fan system object sent to this function.  

**Returns:**  
- **get_fan_system_object_supply_return_exhaust_relief_total_power_flow**: The function calculates and returns the supply, return, exhaust, and relief total fan power, airflow, quantity, and information about whether the pressure drop is consistent across the fans if more than one for a fan system object. The function returns a dictionary that saves the supply, return, exhaust, and relief fan power, saves the supply, return, exhaust, and relief airflow, saves the supply, return, exhaust, and relief quantity, and saves for each fan whether the pressure drop is undefined, identical, or different across fans (if only one it will return undefined or identical){"{fan_type}_fans_Power": value, "{fan_type}_fans_airflow": value, "{fan_type}_fans_qty": value, "{fan_type}_pressure": enums of ("IDENTICAL", "UNDEFINED", "DIFFERENT"). Values will be equal to zero where not defined for a fan system or as otherwise specified above. For airflow values this function assumes that all fans associated with the supply_fans object are in parallel (i.e., if multiple fans the cfm is additive.) but returns the quantity and information about the pressure drop across fans to help assess whether series or parallel.
 
**Function Call:**  
1. get_fan_object_electric_power 


## Logic:    
Supply:
- Reset total fan power to zero: `total_fan_power = 0`  
- Reset total cfm to zero: `total_fan_cfm = 0`  
- Reset fan_qty equal to 0 (counts the quantity of fans): `fan_qty = 0`  
- Reset pressure drop identical across fans: `pressure_drop_identical = true`  
- Reset pressure drop defined for all fans: `pressure_drop_defined_for_all_fans = true`  
- Check if there are any fan objects associated with the fan system's supply fans:`if len(fan_system_obj.supply_fans) != 0 and fan_system_obj.supply_fans != Null:`   
  - Loop through the supply fan: `for fan_obj in fan_system_obj.supply_fans:`  
    - Set the fan_elec_power equal to zero: `fan_elec_power = 0`
    - Set the fan_cfm equal to zero: `fan_cfm = 0`
    - Get the fan objects total kW: `fan_elec_power = get_fan_object_electric_power(RMD, fan_obj)`  
    - Add to the total associated with this fan system: `total_fan_power = total_fan_power + fan_elec_power`  
    - Get the fan cfm: `fan_cfm = fan_obj.design_airflow`  
    - Add to the total associated with this fan system: `total_fan_cfm = total_fan_cfm + fan_cfm`   
    - Check if the fan should be added to the quantity: `if fan_cfm > 0: fan_qty = fan_qty + 1`  
    - Check if the fan pressure drop is defined, if yes then get the fan pressure drop: `if fan_obj.design_pressure_rise != Null: fan_pressure_drop = fan_obj.design_pressure_rise`  
    - Else, pressure drop not defined: `Else: pressure_drop_defined_for_all_fans = false`  
    - Check if pressure_drop_defined_for_all_fans = true: `if pressure_drop_defined_for_all_fans == true and pressure_drop_identical == true:`  
      - Check if this is the first fan: `If fan_qty <= 1: pressure_to_compare = fan_pressure_drop`  
      - Else if (not the first fan and pressure does not equal working pressure) then set pressure_drop_identical to false: `elif pressure_to_compare != fan_pressure_drop: pressure_drop_identical = false`

- Fan system supply cfm equals total_fan_cfm: `fan_sys_supply_cfm = total_fan_cfm` 
- Fan system electric power kW equals total_fan_power: `fan_sys_supply_kW = total_fan_power` 
- Fan quantity equals fan_qty: `fan_supply_qty = fan_qty`
Set pressure drop information:
- If pressure_drop_defined_for_all_fans == false: `if pressure_drop_defined_for_all_fans == false: fan_sys_supply_pressure_drop = "UNDEFINED"`  
- Elif pressure_drop_defined_for_all_fans == true and pressure_drop_identical == true: `elif pressure_drop_defined_for_all_fans == true and pressure_drop_identical == true: fan_sys_supply_pressure_drop = "IDENTICAL"`    
- Else (pressure_drop_defined_for_all_fans == true and pressure_drop_identical == false): `Else: fan_sys_supply_pressure_drop = "DIFFERENT"`  

Return:
- Reset total fan power to zero: `total_fan_power = 0`  
- Reset total cfm to zero: `total_fan_cfm = 0`  
- Reset fan_qty equal to 0 (counts the quantity of fans): `fan_qty = 0` 
- Reset pressure drop identical across fans: `pressure_drop_identical = true`  
- Reset pressure drop defined for all fans: `pressure_drop_defined_for_all_fans = true`  
- Check if there are any fan objects associated with the fan system's return fans:`if len(fan_system_obj.return_fans) != 0 and fan_system_obj.return_fans != Null:`  
  - Loop through the return fan: `for fan_obj in fan_system_obj.return_fans:`  
    - Set the fan_elec_power equal to zero: `fan_elec_power = 0`
    - Set the fan_cfm equal to zero: `fan_cfm = 0`
    - Get the fan objects total kW: `fan_elec_power = get_fan_object_electric_power(RMI, fan_obj)`  
    - Add to the total associated with this fan system: `total_fan_power = total_fan_power + fan_elec_power`  
    - Get the fan cfm: `fan_cfm = fan_obj.design_airflow`  
    - Add to the total associated with this fan system: `total_fan_cfm = total_fan_cfm + fan_cfm`   
    - Check if the fan should be added to the quantity: `if fan_cfm > 0: fan_qty = fan_qty + 1`  
    - Check if the fan pressure drop is defined, if yes then get the fan pressure drop: `if fan_obj.design_pressure_rise != Null: fan_pressure_drop = fan_obj.design_pressure_rise`  
    - Else, pressure drop not defined: `Else: pressure_drop_defined_for_all_fans = false`  
    - Check if pressure_drop_defined_for_all_fans = true: `if pressure_drop_defined_for_all_fans == true and pressure_drop_identical == true:`  
      - Check if this is the first fan: `If fan_qty <= 1: pressure_to_compare = fan_pressure_drop`  
      - Else if (not the first fan and pressure does not equal working pressure) then set pressure_drop_identical to false: `elif pressure_to_compare != fan_pressure_drop: pressure_drop_identical = false`  
    
- Fan system return cfm equals total_fan_cfm: `fan_sys_return_cfm = total_fan_cfm` 
- Fan system electric power kW equals total_fan_power: `fan_sys_return_kW = total_fan_power` 
- Fan quantity equals fan_qty: `fan_return_qty = fan_qty`  
Set pressure drop information:
- If pressure_drop_defined_for_all_fans == false: `if pressure_drop_defined_for_all_fans == false: fan_sys_return_pressure_drop = "UNDEFINED"`  
- Elif pressure_drop_defined_for_all_fans == true and pressure_drop_identical == true: `elif pressure_drop_defined_for_all_fans == true and pressure_drop_identical == true: fan_sys_return_pressure_drop = "IDENTICAL"`    
- Else (pressure_drop_defined_for_all_fans == true and pressure_drop_identical == false): `Else: fan_sys_return_pressure_drop = "DIFFERENT"`  

Exhaust:
- Reset total fan power to zero: `total_fan_power = 0`  
- Reset total cfm to zero: `total_fan_cfm = 0`  
- Reset fan_qty equal to 0 (counts the quantity of fans): `fan_qty = 0`  
- Reset pressure drop identical across fans: `pressure_drop_identical = true`  
- Reset pressure drop defined for all fans: `pressure_drop_defined_for_all_fans = true`  
- Check if there are any fan objects associated with the fan system's exhaust fans:`if len(fan_system_obj.exhaust_fans) != 0 and fan_system_obj.exhaust_fans != Null:`  
  - Loop through the exhaust fan: `for fan_obj in fan_system_obj.exhaust_fans:`  
    - Set the fan_elec_power equal to zero: `fan_elec_power = 0`
    - Set the fan_cfm equal to zero: `fan_cfm = 0`
    - Get the fan objects total kW: `fan_elec_power = get_fan_object_electric_power(RMI, fan_obj)`  
    - Add to the total associated with this fan system: `total_fan_power = total_fan_power + fan_elec_power`  
    - Get the fan cfm: `fan_cfm = fan_obj.design_airflow`  
    - Add to the total associated with this fan system: `total_fan_cfm = total_fan_cfm + fan_cfm`   
    - Check if the fan should be added to the quantity: `if fan_cfm > 0: fan_qty = fan_qty + 1`  
    - Check if the fan pressure drop is defined, if yes then get the fan pressure drop: `if fan_obj.design_pressure_rise != Null: fan_pressure_drop = fan_obj.design_pressure_rise`  
    - Else, pressure drop not defined: `Else: pressure_drop_defined_for_all_fans = false`  
    - Check if pressure_drop_defined_for_all_fans = true: `if pressure_drop_defined_for_all_fans == true and pressure_drop_identical == true:`  
      - Check if this is the first fan: `If fan_qty <= 1: pressure_to_compare = fan_pressure_drop`  
      - Else if (not the first fan and pressure does not equal working pressure) then set pressure_drop_identical to false: `elif pressure_to_compare != fan_pressure_drop: pressure_drop_identical = false`    

- Fan system exhaust cfm equals total_fan_cfm: `fan_sys_exhaust_cfm = total_fan_cfm` 
- Fan system electric power kW equals total_fan_power: `fan_sys_exhaust_kW = total_fan_power` 
- Fan quantity equals fan_qty: `fan_exhaust_qty = fan_qty`  
Set pressure drop information:
- If pressure_drop_defined_for_all_fans == false: `if pressure_drop_defined_for_all_fans == false: fan_sys_exhaust_pressure_drop = "UNDEFINED"`  
- Elif pressure_drop_defined_for_all_fans == true and pressure_drop_identical == true: `elif pressure_drop_defined_for_all_fans == true and pressure_drop_identical == true: fan_sys_exhaust_pressure_drop = "IDENTICAL"`    
- Else (pressure_drop_defined_for_all_fans == true and pressure_drop_identical == false): `Else: fan_sys_exhaust_pressure_drop = "DIFFERENT"`  

Relief:
- Reset total fan power to zero: `total_fan_power = 0`  
- Reset total cfm to zero: `total_fan_cfm = 0`  
- Reset fan_qty equal to 0 (counts the quantity of fans): `fan_qty = 0`  
- Reset pressure drop identical across fans: `pressure_drop_identical = true`  
- Reset pressure drop defined for all fans: `pressure_drop_defined_for_all_fans = true`   
- Check if there are any fan objects associated with the fan system's relief fans:`if len(fan_system_obj.relief_fans) != 0 and fan_system_obj.relief_fans != Null:`  
  - Loop through the relief fan: `for fan_obj in fan_system_obj.relief_fans:`  
    - Set the fan_elec_power equal to zero: `fan_elec_power = 0`
    - Set the fan_cfm equal to zero: `fan_cfm = 0`
    - Get the fan objects total kW: `fan_elec_power = get_fan_object_electric_power(RMI, fan_obj)`  
    - Add to the total associated with this fan system: `total_fan_power = total_fan_power + fan_elec_power`  
    - Get the fan cfm: `fan_cfm = fan_obj.design_airflow`  
    - Add to the total associated with this fan system: `total_fan_cfm = total_fan_cfm + fan_cfm`   
    - Check if the fan should be added to the quantity: `if fan_cfm > 0: fan_qty = fan_qty + 1`  
    - Check if the fan pressure drop is defined, if yes then get the fan pressure drop: `if fan_obj.design_pressure_rise != Null: fan_pressure_drop = fan_obj.design_pressure_rise`  
    - Else, pressure drop not defined: `Else: pressure_drop_defined_for_all_fans = false`  
    - Check if pressure_drop_defined_for_all_fans = true: `if pressure_drop_defined_for_all_fans == true and pressure_drop_identical == true:`  
      - Check if this is the first fan: `If fan_qty <= 1: pressure_to_compare = fan_pressure_drop`  
      - Else if (not the first fan and pressure does not equal working pressure) then set pressure_drop_identical to false: `elif pressure_to_compare != fan_pressure_drop: pressure_drop_identical = false`    

- Fan system relief cfm equals total_fan_cfm: `fan_sys_relief_cfm = total_fan_cfm` 
- Fan system electric power kW equals total_fan_power: `fan_sys_relief_kW = total_fan_power` 
- Fan quantity equals fan_qty: `fan_relief_qty = fan_qty`
Set pressure drop information:
- If pressure_drop_defined_for_all_fans == false: `if pressure_drop_defined_for_all_fans == false: fan_sys_relief_pressure_drop = "UNDEFINED"`  
- Elif pressure_drop_defined_for_all_fans == true and pressure_drop_identical == true: `elif pressure_drop_defined_for_all_fans == true and pressure_drop_identical == true: fan_sys_relief_pressure_drop = "IDENTICAL"`    
- Else (pressure_drop_defined_for_all_fans == true and pressure_drop_identical == false): `Else: fan_sys_relief_pressure_drop = "DIFFERENT"`

- Create dictionary: `get_fan_system_object_supply_return_exhaust_relief_total_power_flow = {"supply_fans_power": fan_sys_supply_kW, "return_fans_power": fan_sys_return_kW,"exhuast_fans_power": fan_sys_exhaust_kW,"relief_fans_power": fan_sys_relief_kW,"supply_fans_airflow": fan_sys_supply_cfm, "exhaust_fans_airflow": fan_sys_exhaust_cfm, "return_fans_airflow": fan_sys_return_cfm, "relief_fans_airflow": fan_sys_relief_cfm, "supply_fans_qty": fan_supply_qty, "exhaust_fans__qty": fan_return_qty, "return_fans_qty": fan_exhaust_qty, "relief_fans_qty": fan_relief_qty, "supply_fans_pressure": fan_sys_supply_pressure_drop, "return_fans_pressure": fan_sys_return_pressure_drop,
"exhuast_fans_pressure": fan_sys_exhaust_pressure_drop, "relief_fans_pressure": fan_sys_relief_pressure_drop}`    
**Returns** `get_fan_system_object_supply_return_exhaust_relief_total_power_flow`  

**Questions:**  
1. For CFM values this function assumes that all fans associated with the supply_fans object are in parallel (i.e., if multiple fans the cfm is additive.).  

**[Back](../_toc.md)**
