
## get_spaces_associated_with_each_SWH_bat

Description: This function gets all the spaces and the SHW space types and sorts them into a dictionary where the keys are the ServiceWaterHeatingSpaceOptions2019ASHRAE901 and values are a list if space.ids  

Inputs:
- **RMD**

Returns:
- **shw_and_spaces_dict**: A dictionary where the keys are the ServiceWaterHeatingSpaceOptions2019ASHRAE901 in the RMD and values are lists of space ids.  Example:  
{"DORMITORY":["sp1","sp2","sp3"], "AUTOMOTIVE_FACILITY":["sp4","sp5","sp6"]}

Function Call:

- get_energy_required_to_heat_swh_use

Data Lookup: None

Logic:

- create a blank dictionary: `shw_and_spaces_dict = {}`
- look at each building segment in the RMD: `for building_segment in RMD...building_segments:`
    - set the building_segment_shw_bat to nil: `building_segment_shw_bat = "UNDETERMINED"`
    - if the building_segment.service_water_heating_area_type exists, include all of the spaces in this building segment in this area type: `if building_segment.service_water_heating_area_type:`
        - set the building_segment_shw_bat to the building_segment.service_water_heating_area_type: `building_segment_shw_bat = building_segment.service_water_heating_area_type`

    - otherwise, if the building segment doesn't have service_water_heating_area_type, we need to determine the type, we need to determine the building segment SHW type: `else:`
        - create a dictionary that will hold the different types of swh_use_bat_types and the total service water used for the year: `swh_use_dict = {}`
        - look at each space in the building segment: `for space in building_segment.spaces:`
            - check to see if the space has service_water_heating_area_type: `if space.service_water_heating_area_type:`
                - add the SWH building area type to the shw_use_dict and set the value to 0: `swh_use_dict.set_default(space.service_water_heating_area_type, 0)`
                - look at each swh use for the space: `for swh_use in space.service_water_heating_uses:`
                    - calculate the total hot water used using the function get_energy_required_to_heat_swh_use and add it to the shw_use_dict: `swh_use_dict[space.service_water_heating_area_type] += get_energy_required_to_heat_swh_use(swh_use, space)`
            - otherwise, need to look at the individual swh uses: `else:`
                - look at each swh use for the sapce: `for swh_use in space.service_water_heating_uses:`
                    - calculate the total hot water used using the function get_energy_required_to_heat_swh_use: `total_energy_used = get_energy_required_to_heat_swh_use(swh_use, space)`
                    - if the shw_use has an area type, add it to the swh_use_dict: `if swh_use.area_type:`
                        - add the shw_use area type to the swh_use_dict, if it doesn't exist yet: `swh_use_dict.set_default(swh_use.area_type, 0)`
                        - add the total energy used to the dict: `swg_use_dict[swh_use.area_type] += get_energy_required_to_heat_swh_use(swh_use, space)`
                    - otherwise: `else:`
                        - add the energy use to type "UNDETERMINED": `swh_use_dict.set_default("UNDETERMINED", 0)`
                        - add the total energy used to the dict: `swh_use_dict["UNDETERMINED"] += get_energy_required_to_heat_swh_use(swh_use, space)`
        - now we need to determine the building_segment swh_use_type based on the following rules:
        -     1. At least 50% of the SWH uses needs to be assigned a use type
        -     2. All SWH needs to be assigned to the same use type
        - if there is only one element in swh_use_dict, the building_segment_shw_bat is the only key in swh_use_dict: `if(len(swh_use_dict)==1): building_segment_shw_bat = list(swh_use_dict.keys())[0]`
        - otherwise, if swh_use_dict has two elements: `elsif(len(swh_use_dict)) == 2:`
            - this should be "UNDETERMINED" and one other area use type: `if "UNDETERMINED" in swh_use_dict:`
                - get the other key.  First get a list of all keys: `all_keys = list(swh_use_dict.keys())`
                - remove "UNDETERMINED": `all_keys.remove("UNDETERMINED")`
                - set other_key to the remaining item in the list: `other_key = all_keys[0]`
                - now check whether the water use for UNDETERMINED is < the water use for the other key: `if swh_use_dict["UNDETERMINED"] < swh_use_dict[other_key]:`
                    - set the building_segment_shw_bat equal to other_key: `building_segment_shw_bat = other_key`
    - create the list in shw_and_spaces_dict for this bat if it doesn't exist: `shw_and_spaces_dict.set_default(building_segment.service_water_heating_area_type, [])`
    - look at each space in the building segment: `for space in building_segment.spaces:`
        - append the space.id to the dictionary: `shw_and_spaces_dict[(building_segment.service_water_heating_area_type].append(space.id)


**Returns** shw_and_spaces_dict

**[Back](../_toc.md)**

**Notes:**

