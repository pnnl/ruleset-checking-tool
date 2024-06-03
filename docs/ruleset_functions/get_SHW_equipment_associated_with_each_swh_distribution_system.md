## get_SWH_equipment_associated_with_each_swh_distribution_system

Description: This function gets all the SWH equipment connected to a SWH distribution system.  The information is stored in a dictionary where the keys are the SWH Distribution System Ids and values are a dictionary giving the ServiceWaterHeatingEquipment, and Pumps connected to the particular use type  

Inputs:
- **RMD**

Returns:
- **swh_and_equip_dict**: A dictionary containing where the keys are the SWH Distribution System and values are dictionaries where keys are the type of SWH equipment and values are the ids of the connected equipment.  Example:  
{"SWH_Distribution1":{"SWHHeatingEq":["swh_eq1","swh_eq2"], "Pumps":["p1"], "Tanks":["t1"], "Piping":["piping1"], "SolarThermal":[], "SPACE_USES":["sp1_use","sp2_use"], "SPACES_SERVED":[sp1,sp2]}}

Function Call:

- get_obj_by_id
- get_all_child_SWH_piping_ids

Data Lookup: None

Logic:
- create a blank dictionary: `swh_and_equip_dict = {}`
- for each swh distribution system in the RMD: `for distribution in RMD.service_water_heating_distribution_systems:`
    - add the blank dictionary for the distribution system id: `swh_and_equip_dict.set_default(distribution.id, {"SWHHeatingEq":[],"Pumps":[],"Tanks":[], "Piping":[], "SolarThermal":[], "SPACE_USES":[], "SPACES_SERVED":[]})`
    - now we need to get all of the equipment connected to this distribution system.
    - get the tanks: `tanks = distribution.tanks`
    - append the tank ids to the dictionary: `for t in tanks:  swh_and_equip_dict[distribution.id]["Tanks"].append(t.id)`
    - get the id of the SWH pipings: `for piping_id in distribution.service_water_piping`
        - get all the ids of all of the children of the piping: `piping_ids = get_all_child_SWH_piping_ids(RMD, piping_id)`
        - append all of the piping ids to the list: `swh_and_equip_dict[distribution.id]["Piping"].extend(piping_ids)`
    - to figure out which pumps are connected, go through each pump in the rmd: `for pump in RMD.pumps:`
        - check if the pump.loop_or_piping is in the piping list: `if pump.loop_or_piping in swh_and_equip_dict[distribution.id]["Piping"]:`
            - this pump is connected to the SWH distribution system, append it to the list: `swh_and_equip_dict[distribution.id]["Pumps"].append(pump.id)`
    - to figure out which swh_equipment is connected, go through each service_water_heating_equipment in the rmd: `for swh_equip in RMD.service_water_heating_equipment:`
        - check if the distribution system referenced is the same as the distribution system we're currently looking at: `if swh_equip.distribution_system == distribution:`
            - this swh equipment is connected, append it to the list: `swh_and_equip_dict[distribution.id]["SWHHeatingEq"].append(swh_equip.id)`
            - this also means that any solarthermal attached to this swh_equip is connected, append the SolarThermal ids: `for solar_t in swh_equip.solar_thermal_systems: swh_and_equip_dict[distribution.id]["SolarThermal"].append(solar_t.id)`
- now go through each space in the RMD: `for space in RMD...spaces:`
    - go through each swh space use: `for swh_use in space.service_water_heating_uses:`
        - find the distribution system: `distribution = swh_use.served_by_distribution_system`
        - add the swh_use id to the dictionary for the distribution: `swh_and_equip_dict[distribution.id]["SPACE_USES"].append(swh_use.id)`
        - add the space id to the dictionary for the distribution: `swh_and_equip_dict[distribution.id]["SPACES_SERVED"].append(space.id)`

**Returns** swh_and_equip_dict

**[Back](../_toc.md)**

**Notes:**
