## get_SHW_equipment_associated_with_each_SWH_bat

Description: This function gets all the SHW equipment connected to a particular SHW use type.  The information is stored in a dictionary where the keys are the ServiceWaterHeatingSpaceOptions2019ASHRAE901 and values are a dictionary giving the ServiceWaterHeatingDistributionSystem, ServiceWaterHeatingEquipment, and Pumps connected to the particular use type  

Inputs:
- **RMD**

Returns:
- **shw_and_equip_dict**: A dictionary containing where the keys are the ServiceWaterHeatingSpaceOptions2019ASHRAE901 in the RMD and values are dictionaries where keys are the type of SWH equipment and values are the ids of the connected equipment.  Example:  
{"DORMITORY":{"SHWDistribution":["shwd1","shwd2"], "SHWHeatingEq":["shw_eq1","shw_eq2"], "Pumps":["p1"], "Tanks":["t1"], "Piping":["piping1"], "SolarThermal":[]}}

Function Call:

- get_SHW_types_and_spaces
- get_obj_by_id
- get_all_child_SHW_piping_ids

Data Lookup: None

Logic:
- get the dictionary of SHW types and space ids from the function get_SHW_types_and_spaces: `shw_types_and_uses_dict = shw_and_SHW_use_dict(RMD)`
- create a blank dictionary: `shw_and_equip_dict = {}`
- look at space type in shw_types_and_uses_dict: `for shw_use_type in shw_types_and_uses_dict:`
    - create the blank list for the shw_use_type: `shw_and_equip_dict[shw_use_type] = {"SHWDistribution":[],"SHWHeatingEq":[],"Pumps":[],"Tanks":[], "Piping":[], "SolarThermal":[]}`
    - look at SHW use: `for use_id in shw_types_and_uses_dict[shw_use_type]:`
        - get the shw_use using get_obj_by_id: `shw_use = get_obj_by_id(RMD, use_id)`
        - get the distribution id: `distribution_id = shw_use.served_by_distribution_system`
        - add the distribution id to the list: `shw_and_equip_dict[shw_use_type]["SHWDistribution"].append(distribution_id)`
        - get the distribution using get_obj_by_id: `distribution = get_obj_by_id(RMD, distribution_id)`
        - now we need to get all of the equipment connected to this distribution system.
        - get the tanks: `tanks = distribution.tanks`
        - append the tank ids to the dictionary: `for t in tanks:  shw_and_equip_dict[shw_use_type]["Tanks"].append(t.id)`
        - get the id of the SHW pipings: `for piping_id in distribution.service_water_piping`
            - get all the ids of all of the children of the piping: `piping_ids = get_all_child_SHW_piping_ids(RMD, piping_id)`
            - append all of the piping ids to the list: `shw_and_equip_dict[shw_use_type]["Piping"].extend(piping_ids)`
    - to figure out which pumps are connected, go through each pump in the rmd: `for pump in RMD.pumps:`
        - check if the pump.loop_or_piping is in the piping list: `if pump.loop_or_piping in shw_and_equip_dict[shw_use_type]["Piping"]:`
            - this pump is connected to the SHW that serves this space type, append it to the list: `shw_and_equip_dict[shw_use_type]["Pumps"].append(pump.id)`
    - to figure out which shw_equipment is connected, go through each service_water_heating_equipment in the rmd: `for shw_equip in RMD.service_water_heating_equipment:`
        - check if the id of the ServiceWaterHeatingDistributionSystem connected to the shw_equip is in the list of SHWDistribution: `if shw_equip.distribution_system in shw_and_equip_dict[shw_use_type]["SHWDistribution"]:`
            - this shw equipment is connected, append it to the list: `shw_and_equip_dict[shw_use_type]["SHWHeatingEq"].append(shw_equip.id)`
            - this also means that any solarthermal attached to this shw_equip is connected, append the SolarThermal ids: `for solar_t in shw_equip.solar_thermal_systems: shw_and_equip_dict[shw_use_type]["SolarThermal"].append(solar_t.id)`



**Returns** shw_and_equip_dict

**[Back](../_toc.md)**

**Notes:**
