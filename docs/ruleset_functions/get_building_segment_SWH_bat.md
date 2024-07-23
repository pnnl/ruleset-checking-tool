## get_building_segment_SWH_bat

Description: This function determines the SWH BAT for the given building segment.

Inputs:
- **RMD**
- **building_segment**

Returns:
- **building_segment_swh_bat**: one of the ServiceWaterHeatingSpaceOptions2019ASHRAE901 options

Function Call:

- get_energy_required_to_heat_swh_use  
- get_SWH_uses_associated_with_each_building_segment    
- get_component_by_ID  

Data Lookup: None

Logic:

- set the building_segment_swh_bat to nil: `building_segment_swh_bat = "UNDETERMINED"`
- if the building_segment.service_water_heating_building_area_type exists set the swh_bat to the one given: `if building_segment.service_water_heating_building_area_type:`
    - set the building_segment_swh_bat to the building_segment.service_water_heating_building_area_type: `building_segment_swh_bat = building_segment.service_water_heating_building_area_type`
- otherwise, if the building segment doesnt have service_water_heating_building_area_type, we need to determine the building segment SWH type by looking at individual SWH uses: `else:`
    - create a dictionary that will hold the different types of swh_use_bat_types and the total service water used for the year: `swh_use_dict = {}`
    - get the service water heating uses in the building segment `service_water_heating_use_ids = get_SWH_uses_associated_with_each_building_segment(RMD, building_segment.id)`
    - look at each service water heating use id: `for swh_use_id in service_water_heating_use_ids:`
        - get the swh_use using get_component_by_ID: `swh_use = get_component_by_ID(RMD, swh_use_id)`
        - if any swh_use has use_units equal to "OTHER", the total energy required to heat the use cannot be determined, and we return "UNDETERMINED": `if swh_use.use_units == "OTHER": return "UNDETERMINED"`
        - calculate the total energy required to heat the swh_use using the function get_energy_required_to_heat_swh_use: `swh_use_energy_by_space = get_energy_required_to_heat_swh_use(swh_use, RMD)`
        - check to see if the swh_use has service_water_heating_area_type: `if swh_use.area_type:`
            - add the SWH building area type to the swh_use_dict and set the default value to 0: `swh_use_dict.set_default(swh_use.area_type, 0)`
            - add the energy used by this swh_use: `swh_use_dict[swh_use.area_type] += sum(swh_use_energy_by_space.values())`
        - otherwise: `else:`
            - go through each space served by the swh_use and see if it has a service_water_heating_bat: `for space_id in swh_use_energy_by_space:`
                - get the space: `space = get_component_by_ID(RMD, space_id)`
                - check if the space has a swh_use_bat: `if space.service_water_heating_bat:`
                    - First add the BAT and set the default: `swh_use_dict.set_default("space.service_water_heating_bat", 0)`
                    - add the energy used to the dict: `swh_use_dict["space.service_water_heating_bat"] += swh_use_energy_by_space[space_id]`
                - otherwise, we'll add this use to UNDETERMINED.`else:`
                    - First add UNDETERMINED and set the default: `swh_use_dict.set_default("UNDETERMINED", 0)`
                    - add the energy used to the dict: `swh_use_dict["UNDETERMINED"] += swh_use_energy_by_space[space_id]`
    - now we need to determine the building_segment swh_use_type based on the following rules:
    -     1. At least 50% of the SWH uses needs to be assigned a use type
    -     2. All SWH needs to be assigned to the same use type
    - if there is only one element in swh_use_dict, the building_segment_swh_bat is the only key in swh_use_dict: `if(len(swh_use_dict)==1): building_segment_swh_bat = list(swh_use_dict.keys())[0]`
    - otherwise, if swh_use_dict has two elements: `elsif(len(swh_use_dict)) == 2:`
        - in order to meet the requirement that all SWH needs to be assigned to the same use type - ie any SWH that doesn't have a use-type is covered by "UNDETERMINED", we expect the dict to have keys "UNDETERMINED" and one other area use type: `if "UNDETERMINED" in swh_use_dict:`
            - get the other key.  First get a list of all keys: `all_keys = list(swh_use_dict.keys())`
            - remove "UNDETERMINED": `all_keys.remove("UNDETERMINED")`
            - set other_key to the remaining item in the list: `other_key = all_keys[0]`
            - now check whether the water use for UNDETERMINED is < the water use for the other key: `if swh_use_dict["UNDETERMINED"] < swh_use_dict[other_key]:`
                - set the building_segment_swh_bat equal to other_key: `building_segment_swh_bat = other_key`

- return result: `return: building_segment_swh_bat`


**Returns** building_segment_swh_bat

**[Back](../_toc.md)**

**Notes:**
1. relies on re-structuring of SWH as in: https://github.com/open229/ruleset-model-description-schema/issues/264
