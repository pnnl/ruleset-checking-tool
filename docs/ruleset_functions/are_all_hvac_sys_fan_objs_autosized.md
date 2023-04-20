# are_all_hvac_sys_fan_objs_autosized  

**Description:** Returns true or false. The function returns true if all supply fan objects associated with an hvac system are autosized.  

**Inputs:**  
- **U,P,or B-RMI**: The RMD in which the fan system object is defined. 
- **hvac_sys_obj**: The hvac object in which the associated fan objects will be assessed.

**Returns:**  
- **are_all_hvac_sys_fan_objs_autosized**: Returns true or false. The function returns true if all supply fan objects associated with an hvac system are autosized.   
 
**Function Call:** 
1. get_dict_of_zones_and_terminal_units_served_by_hvac_sys()    

## Logic:  
- Create dictionary of hvac systems and associated zones and terminal units: `dict_of_zones_and_terminal_units_served_by_hvac_sys_x = get_dict_of_zones_and_terminal_units_served_by_hvac_sys(RMI)`  
- Set are_all_hvac_sys_fan_objs_autosized = true: `are_all_hvac_sys_fan_objs_autosized = true`  
- Check if there is a fan system associated with the hvac system (if not then assume it is defined at the terminal unit like it is for a four-pipe fan coil unit): `if hvac.fan_system != Null:`
    - For each supply fan associated with the fan system: `for supp_fan in hvac.fan_system.supply_fans:`   
        - Check if the fan was NOT autosized: `if supp_fan.is_airflow_autosized = false: are_all_hvac_sys_fan_objs_autosized =  false`  
- Else, the fan system is defined at the terminal unit (like for a four pipe fan coil unit): `Else:`  
    - Get list of terminal units served by the hvac system: `terminal_list_hvac_sys_x = dict_of_zones_and_terminal_units_served_by_hvac_sys_x[hvac.sys_obj.id]["ZONE_LIST"]["Terminal_Unit_List"]`
    - For each terminal unit associated with the hvac system (should only be one): `for terminal in terminal_list_hvac_sys_x:`  
        - Check if the fan is NOT autosized, if not then set are_all_hvac_sys_fan_objs_autosized equal to false: `if terminal.fan.is_airflow_autosized = false: are_all_hvac_sys_fan_objs_autosized = false`      

**Returns** `return are_all_hvac_sys_fan_objs_autosized`  

**Comments/Questions**  None   


**[Back](../_toc.md)**
