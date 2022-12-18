# get_fan_system_object_supply_return_exhaust_relief_total_kW_CFM

**Description:** Get the supply, return, exhaust, and relief total fan power and CFM associated with a fan system object.   The function returns a dictionary that saves the supply, return, exhaust, and relief fan power has a list and the saves the supply, return, exhaust, and relief cfm as a list {"Fan_Power": [supply fan power kW, return fan power kW, exhaust fan power kW, relief fan power kW], "Fan_CFM": [supply fan power CFM, return fan power CFM, exhaust fan power CFM, relief fan power CFM]}. Values will be equal to zero where not defined for a fan system.

**Inputs:**  
- **B-RMI,P-RMI**: To calculate the supply, return, exhaust, and relief total fan power and CFM associated with a fan system object sent to this function.   
- **fan_system_obj**: The fan system object sent to this function.  

**Returns:**  
- **get_fan_system_object_supply_return_exhaust_relief_total_kW_CFM**: The function calculates and return the supply, return, exhaust, and relief total fan power and CFM associated with the fan system object sent to this function. The function returns a dictionary that saves the supply, return, exhaust, and relief fan power has a list and the saves the supply, return, exhaust, and relief cfm as a list {"Fan_Power": [supply fan power kW, return fan power kW, exhaust fan power kW, relief fan power kW], "Fan_CFM": [supply fan power CFM, return fan power CFM, exhaust fan power CFM, relief fan power CFM]}. Values will be equal to zero where not defined for a fan system.
 
**Function Call:**  
1. get_fan_object_electric_power 


## Logic:    
- Reset total fan power to zero: `total_fan_power = 0`  
- Reset total cfm to zero: `total_fan_cfm = 0`  
- Check if there are any fan objects associated with the fan system's supply fans:`if len(fan_system_obj.supply_fans) != 0 and fan_system_obj.supply_fans != Null:`  
  - Loop through the supply fan: `for fan_obj in fan_system_obj.supply_fans:`  
    - Set the fan_elec_power equal to zero: `fan_elec_power = 0`
    - Set the fan_cfm equal to zero: `fan_cfm = 0`
    - Get the fan objects total kW: `fan_elec_power = get_fan_object_electric_power(P_RMI, fan_obj)`  
    - Add to the total associated with this fan system: `total_fan_power = total_fan_power + fan_elec_power`  
    - Get the fan cfm: `fan_cfm = fan_obj.design_airflow`  
    - Add to the total associated with this fan system: `total_fan_cfm = total_fan_cfm + fan_cfm`   
- Fan system supply cfm equals total_fan_cfm: `fan_sys_supply_cfm = total_fan_cfm` 
- Fan system electric power kW equals total_fan_power: `fan_sys_supply_kW = total_fan_power` 

- Reset total fan power to zero: `total_fan_power = 0`  
- Reset total cfm to zero: `total_fan_cfm = 0`  
- Check if there are any fan objects associated with the fan system's return fans:`if len(fan_system_obj.return_fans) != 0 and fan_system_obj.return_fans != Null:`  
  - Loop through the return fan: `for fan_obj in fan_system_obj.return_fans:`  
    - Set the fan_elec_power equal to zero: `fan_elec_power = 0`
    - Set the fan_cfm equal to zero: `fan_cfm = 0`
    - Get the fan objects total kW: `fan_elec_power = get_fan_object_electric_power(P_RMI, fan_obj)`  
    - Add to the total associated with this fan system: `total_fan_power = total_fan_power + fan_elec_power`  
    - Get the fan cfm: `fan_cfm = fan_obj.design_airflow`  
    - Add to the total associated with this fan system: `total_fan_cfm = total_fan_cfm + fan_cfm`   
- Fan system return cfm equals total_fan_cfm: `fan_sys_return_cfm = total_fan_cfm` 
- Fan system electric power kW equals total_fan_power: `fan_sys_return_kW = total_fan_power` 

- Reset total fan power to zero: `total_fan_power = 0`  
- Reset total cfm to zero: `total_fan_cfm = 0`  
- Check if there are any fan objects associated with the fan system's exhaust fans:`if len(fan_system_obj.exhaust_fans) != 0 and fan_system_obj.exhaust_fans != Null:`  
  - Loop through the exhaust fan: `for fan_obj in fan_system_obj.exhaust_fans:`  
    - Set the fan_elec_power equal to zero: `fan_elec_power = 0`
    - Set the fan_cfm equal to zero: `fan_cfm = 0`
    - Get the fan objects total kW: `fan_elec_power = get_fan_object_electric_power(P_RMI, fan_obj)`  
    - Add to the total associated with this fan system: `total_fan_power = total_fan_power + fan_elec_power`  
    - Get the fan cfm: `fan_cfm = fan_obj.design_airflow`  
    - Add to the total associated with this fan system: `total_fan_cfm = total_fan_cfm + fan_cfm`   
- Fan system exhaust cfm equals total_fan_cfm: `fan_sys_exhaust_cfm = total_fan_cfm` 
- Fan system electric power kW equals total_fan_power: `fan_sys_exhaust_kW = total_fan_power` 

- Reset total fan power to zero: `total_fan_power = 0`  
- Reset total cfm to zero: `total_fan_cfm = 0`  
- Check if there are any fan objects associated with the fan system's relief fans:`if len(fan_system_obj.relief_fans) != 0 and fan_system_obj.relief_fans != Null:`  
  - Loop through the relief fan: `for fan_obj in fan_system_obj.relief_fans:`  
    - Set the fan_elec_power equal to zero: `fan_elec_power = 0`
    - Set the fan_cfm equal to zero: `fan_cfm = 0`
    - Get the fan objects total kW: `fan_elec_power = get_fan_object_electric_power(P_RMI, fan_obj)`  
    - Add to the total associated with this fan system: `total_fan_power = total_fan_power + fan_elec_power`  
    - Get the fan cfm: `fan_cfm = fan_obj.design_airflow`  
    - Add to the total associated with this fan system: `total_fan_cfm = total_fan_cfm + fan_cfm`   
- Fan system relief cfm equals total_fan_cfm: `fan_sys_relief_cfm = total_fan_cfm` 
- Fan system electric power kW equals total_fan_power: `fan_sys_relief_kW = total_fan_power` 

- Create dictionary: `get_fan_system_object_supply_return_exhaust_relief_total_kW_CFM = {"Fan_Power": [fan_sys_supply_kW,fan_sys_return_kW,fan_sys_exhaust_kW,fan_sys_relief_kW], "Fan_CFM": [fan_sys_supply_cfm,fan_sys_return_cfm,fan_sys_exhaust_cfm,fan_sys_relief_cfm]}` 

**Returns** `get_fan_system_object_supply_return_exhaust_relief_total_kW_CFM`  

**Questions:**  None  

**[Back](../_toc.md)**
