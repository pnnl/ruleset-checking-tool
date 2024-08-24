## get_swh_components_associated_with_each_swh_distribution_system

Description: This function gets all the SWH equipment connected to a SWH distribution system.  The information is stored in a dictionary where the keys are the SWH Distribution System Ids and values are a dictionary giving the ServiceWaterHeatingEquipment, and Pumps connected to the particular SWH distribution system  

Inputs:
- **RMD**

Returns:
- **swh_and_equip_dict**: A dictionary containing where the keys are the SWH Distribution System IDs and values are dictionaries where keys are the type of SWH equipment and values are the ids of the connected equipment.  Example:  
{"swh_distribution1":{"swh_heating_eq":["swh_eq1","swh_eq2"], "pumps":["p1"], "tanks":["t1"], "piping":["piping1"], "solar_thermal":[], "uses":["sp1_use","sp2_use"], "spaces_served":[sp1,sp2]}}

Function Call:

- get_obj_by_id
- get_all_child_swh_piping_ids
- get_spaces_served_by_swh_use

Data Lookup: None

Logic:
- create a blank dictionary: `swh_and_equip_dict = {}`
- for each swh distribution system in the RMD: `for distribution in RMD.service_water_heating_distribution_systems:`
    - add the blank dictionary for the distribution system id: `swh_and_equip_dict.set_default(distribution.id, {"swh_heating_eq":[],"pumps":[],"tanks":[], "piping":[], "solar_thermal":[], "uses":[], "spaces_served":[]})`
    - now we need to get all of the equipment connected to this distribution system.
    - get the tanks: `tanks = distribution.tanks`
    - append the tank ids to the dictionary: `for tank in tanks:  swh_and_equip_dict[distribution.id]["tanks"].append(tank.id)`
    - get the id of the SWH pipings: `for piping_id in distribution.service_water_piping`
        - get all the ids of all of the children of the piping: `piping_ids = get_all_child_swh_piping_ids(RMD, piping_id)`
        - append all of the piping ids to the list: `swh_and_equip_dict[distribution.id]["piping"].extend(piping_ids)`
    - to figure out which pumps are connected, go through each pump in the rmd: `for pump in RMD.pumps:`
        - check if the pump.loop_or_piping is in the piping list: `if pump.loop_or_piping in swh_and_equip_dict[distribution.id]["piping"]:`
            - this pump is connected to the SWH distribution system, append it to the list: `swh_and_equip_dict[distribution.id]["pumps"].append(pump.id)`
    - to figure out which swh_equipment is connected, go through each service_water_heating_equipment in the rmd: `for swh_equip in RMD.service_water_heating_equipment:`
        - check if the distribution system referenced is the same as the distribution system we're currently looking at: `if swh_equip.distribution_system == distribution.id:`
            - this swh equipment is connected, append it to the list: `swh_and_equip_dict[distribution.id]["swh_heating_eq"].append(swh_equip.id)`
            - this also means that any solarthermal attached to this swh_equip is connected, append the SolarThermal ids: `for solar_t in swh_equip.solar_thermal_systems: swh_and_equip_dict[distribution.id]["solar_thermal"].append(solar_t.id)`
- now go through each SWH Use in the RMD: `for swh_use in RMD...service_water_heating_uses:`
    - find the distribution system: `distribution_id = swh_use.served_by_distribution_system`
    - add the swh_use id to the dictionary for the distribution: `swh_and_equip_dict[distribution_id]["uses"].append(swh_use.id)`
    - now get the ids of spaces served by this SWH Use by using the function get_spaces_served_by_swh_use, and add all of them to the list: `swh_and_equip_dict[distribution.id]["spaces_served"].append(space.id for space in get_spaces_served_by_swh_use(RMD,swh_use))

**Returns** swh_and_equip_dict

**[Back](../_toc.md)**

**Notes:**
