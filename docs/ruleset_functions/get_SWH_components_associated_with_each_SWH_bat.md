## get_SWH_components_associated_with_each_SWH_bat

Description: This function gets all the SWH equipment connected to a particular SWH use type.  The information is stored in a dictionary where the keys are the ServiceWaterHeatingSpaceOptions2019ASHRAE901 and values are a dictionary giving the ServiceWaterHeatingDistributionSystem, ServiceWaterHeatingEquipment, and Pumps connected to the particular use type.  There is also an entry for the total energy required to heat all SWH uses for a year: "EnergyRequired"   

Inputs:
- **RMD**

Returns:
- **swh_and_equip_dict**: A dictionary containing where the keys are the ServiceWaterHeatingSpaceOptions2019ASHRAE901 in the RMD and values are dictionaries where keys are the type of SWH equipment and values are the ids of the connected equipment.  Example:  
{"DORMITORY":{"SWHDistribution":["swhd1","swhd2"], "SWHHeatingEq":["swh_eq1","swh_eq2"], "Pumps":["p1"], "Tanks":["t1"], "Piping":["piping1"], "SolarThermal":[], "SWH_Uses":["swh_use1","swh_use2"], "EnergyRequired": 100000}}

Function Call:

- get_obj_by_id   
- get_all_child_SWH_piping_ids  
- get_building_segment_swh_bat  
- get_energy_required_to_heat_swh_use  
- get_SWH_uses_associated_with_each_building_segment  

Data Lookup: None

Logic:

- create a blank dictionary: `swh_and_equip_dict = {}`
- look at each building segment in the RMD: `for building_segment in RMD...building_segments:`
    - get the SWH BAT for this building segment using the function get_building_segment_swh_bat: `swh_bat = get_building_segment_swh_bat(RMD,building_segment)`
    - create the blank list for the swh_bat, if it doesn't exist yet: `swh_and_equip_dict[swh_bat].set_default({"SWHDistribution":[],"SWHHeatingEq":[],"Pumps":[],"Tanks":[], "Piping":[], "SolarThermal":[], "SWH_Uses":[], "EnergyRequired":0})`
    - get the service water heating uses in the building segment `service_water_heating_use_ids = get_SWH_uses_associated_with_each_building_segment(RMD, building_segment.id)`
    - look at each service water heating use id: `for swh_use_id in service_water_heating_use_ids:`
        - get the swh_use using get_obj_by_id : `swh_use = get_obj_by_id (RMD, swh_use_id)`
        - get the energy required to heat the water using the function get_energy_required_to_heat_swh_use: `energy_required = get_energy_required_to_heat_swh_use(swh_use, RMD, building_segment)`
        - add the energy required to heat the swh use, to "EnergyRequired" for this bat: `swh_and_equip_dict[swh_bat]["EnergyRequired"] += energy_required`
        - add the id for the swh_use to the "SWH_Uses" list: `swh_and_equip_dict[swh_bat]["SWH_Uses"].append(swh_use.id)`
        - get the distribution id: `distribution_id = swh_use.served_by_distribution_system`
        - check if the distribution system is already in the list.  If it is not we'll add it and all associated equipment: `if !distribution_id in swh_and_equip_dict[swh_bat]["SWHDistribution"]:`
            - add the distribution id to the list: `swh_and_equip_dict[swh_bat]["SWHDistribution"].append(distribution_id)`
            - get the distribution using get_obj_by_id : `distribution = get_obj_by_id (RMD, distribution_id)`
            - now we need to get all of the equipment connected to this distribution system.
            - get the tanks: `tanks = distribution.tanks`
            - append the tank ids to the dictionary: `for t in tanks:  swh_and_equip_dict[swh_bat]["Tanks"].append(t.id)`
            - get the id of the SWH pipings: `for piping_id in distribution.service_water_piping`
                - get all the ids of all of the children of the piping: `piping_ids = get_all_child_SWH_piping_ids(RMD, piping_id)`
                - append all of the piping ids to the list: `swh_and_equip_dict[swh_bat]["Piping"].extend(piping_ids)`

- there is still other equipment that needs to be added, but we don't want to add it more than once, so we go back out to the top level and look through each of the swh_use_types again: `for swh_bat in swh_and_equip_dict:`
    - to figure out which pumps are connected, go through each pump in the rmd: `for pump in RMD.pumps:`
        - check if the pump.loop_or_piping is in the piping list: `if pump.loop_or_piping in swh_and_equip_dict[swh_bat]["Piping"]:`
            - this pump is connected to the SWH that serves this space type, append it to the list: `swh_and_equip_dict[swh_bat]["Pumps"].append(pump.id)`
    - to figure out which swh_equipment is connected, go through each service_water_heating_equipment in the rmd: `for swh_equip in RMD.service_water_heating_equipment:`
        - check if the id of the ServiceWaterHeatingDistributionSystem connected to the swh_equip is in the list of SWHDistribution: `if swh_equip.distribution_system in swh_and_equip_dict[swh_bat]["SWHDistribution"]:`
            - this swh equipment is connected, append it to the list: `swh_and_equip_dict[swh_bat]["SWHHeatingEq"].append(swh_equip.id)`
            - this also means that any solarthermal attached to this swh_equip is connected, append the SolarThermal ids: `for solar_t in swh_equip.solar_thermal_systems: swh_and_equip_dict[swh_bat]["SolarThermal"].append(solar_t.id)`


**Returns** swh_and_equip_dict

**[Back](../_toc.md)**

**Notes:**
