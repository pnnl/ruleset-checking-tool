# get_hvac_system_with_longest_fan_schedule_p

**Description:** Returns the HeatingVentilationAirAconditioningSystem.id associated with a zone (function input) in the proposed that has the longest fan schedule for the purposes of comparing schedules across the baseline and proposed.

**Inputs:**
- **zone_p.id..P_RMR.**: A zone id associated with the P_RMR to determine the HeatingVentilationAirAconditioningSystem.id that has the longest fan schedule for the purposes of comparing schedules across the baseline and proposed for the zone.

**Returns:**
- **hvac_system_with_longest_fan_schedule_p**: the HeatingVentilationAirAconditioningSystem.id of the hvac system with the longest fan schedule serving a specific zone.
 
**Function Call:** None

**Logic:**
# Create list of hvac system associated with the zone
- For each terminal unit associated with zone_p.id (input to this function): `for terminal_p in zone_p.id:`
    - Get the served_py_heating_ventilation_air_conditioning_systems for each terminal: `heating_ventilation_air_conditioning_systems_p = terminal_p.served_py_heating_ventilation_air_conditioning_systems`
    - Add to list of heating_ventilation_air_conditioning_systems_list_p as the code loops through the terminal units: `heating_ventilation_air_conditioning_systems_list_p = heating_ventilation_air_conditioning_systems_list_p.append(heating_ventilation_air_conditioning_systems_p)`                
- Convert the list of heating_ventilation_air_conditioning_systems_list_p associated with the zone to a set and the back to a list to eliminate duplicates after looping through terminal units: `heating_ventilation_air_conditioning_systems_list_p = list(set(heating_ventilation_air_conditioning_systems_list_p))`

# Determine which of the hvac systems has the longest fan schedule
- For each hvac_p in heating_ventilation_air_conditioning_systems_list_p: `for hvac_p in heating_ventilation_air_conditioning_systems_list_p:`
    - Set fan_schedule_p to zero: `fan_schedule_p =0`       
    - For each value in the fan_schedule associated with the fan system associated with the hvac system: `for x in range(8760):`
        - Sum value for each hour in the fan operating schedule: `fan_schedule_p = fan_schedule_p + hvac_p.fan_systems[0].operating_schedule(x)` Assumes one fan system per hvac system as recently discussed 2/11/2022
    - Add sum to dictionary with the hvac system id as key and fan_schedule_p as value: `hvac_fan_schedule_dict[hvac_p.ID] = fan_schedule_p`
- Find the key for the hvac system with the longest schedule associated with zone_p: `hvac_system_with_longest_fan_schedule_p = max(hvac_fan_schedule_dict, key = hvac_fan_schedule_dict.get())`

 **Returns** `return hvac_system_with_longest_fan_schedule_p`  

**[Back](../_toc.md)**
