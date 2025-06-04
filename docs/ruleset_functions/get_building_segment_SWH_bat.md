## get_building_segment_SWH_bat

Description: This function determines the SWH BAT for the given building segment.

Inputs:
- **RMD**
- **building_segment**
- **is_leap_year**  

Returns:
- **building_segment_swh_bat**: one of the ServiceWaterHeatingSpaceOptions2019ASHRAE901 options

Function Call:

- get_energy_required_to_heat_swh_use  
- get_component_by_ID  

Data Lookup: None

Logic:

- set the building_segment_swh_bat to nil: `building_segment_swh_bat = "UNDETERMINED"`
- get the service_water_heating_building_area_type value: `building_segment_swh_bat = building_segment.get("service_water_heating_building_area_type", None)`
- if building_segment_swh_bat doesn't have service_water_heating_building_area_type, we need to determine the building segment SWH area type by looking at individual SWH uses: `if building_segment_swh_bat is None`
    - create a dictionary that will hold the different types of swh_use_bat_types and the total service water used for the year: `swh_use_dict = {}`
	- create a list of all of the swh uses stored in spaces - note to DEV team - just take the actual objects, not the object references at this stage: `swh_uses_from_spaces = find_all(f'$.buildings[*].building_segments[*][?(@.id == "{building_segment.id}")].zones[*].spaces[*].service_water_heating_uses[*]', rmd)`
	- create a list of all the swh uses stored at the building segment level: `swh_uses_direct = find_all(f'$.buildings[*].building_segments[*][?(@.id == "{building_segment.id}")].service_water_heating_uses[*]', rmd)`

    - look at each service water heating use in the building: `for swh_use in swh_uses_from_spaces + swh_uses_direct:`
        - if any swh_use has use_units equal to "OTHER" or swh_use is not an empty dict, the total energy required to heat the use cannot be determined, and building_segment_swh_bat is "UNDETERMINED": `if swh_use and swh_use.use_units == "OTHER": building_segment_swh_bat = "UNDETERMINED"`
        - calculate the total energy required to heat the swh_use using the function get_energy_required_to_heat_swh_use: `swh_use_energy_by_space = get_energy_required_to_heat_swh_use(swh_use, RMD, building_segment, is_leap_year)`
        - check to see if the swh_use has service_water_heating_area_type: `if swh_use.area_type:`
            - add the SWH building area type to the swh_use_dict and set the default value to 0: `swh_use_dict.setdefault(swh_use.area_type, ZERO.ENERGY)`
            - add the energy used by this swh_use: `swh_use_dict[swh_use.area_type] += sum(swh_use_energy_by_space.values())`
        - otherwise: `else:`
            - go through each space served by the swh_use and see if it has a service_water_heating_bat: `for space_id in swh_use_energy_by_space:`
                - get the space: `space = get_component_by_ID(RMD, space_id)`
                - check if the space has a swh_use_bat: `if space.service_water_heating_bat:`
                    - First add the BAT and set the default: `swh_use_dict.setdefault("space.service_water_heating_bat", ZERO.ENERGY)`
                    - add the energy used to the dict: `swh_use_dict["space.service_water_heating_bat"] += swh_use_energy_by_space[space_id]`
                - otherwise, we'll add this use to UNDETERMINED.`else:`
                    - First add UNDETERMINED and set the default: `swh_use_dict.setdefault("UNDETERMINED", ZERO.ENERGY)`
                    - add the energy used to the dict: `swh_use_dict["UNDETERMINED"] += swh_use_energy_by_space[space_id]`
    - now we need to determine the building_segment SWH area type based on the following rules:
    - At least 50% of the SWH uses needs to be assigned a SWH area type  
    - All SWH needs to be assigned to the same SWH area type  
    - Select the building area type that has the greateest value: `building_segment_swh_bat = max(swh_use_dict, key=swh_use_dict.get) if swh_use_dict else "UNDETERMINED"`

- if the building_segment.service_water_heating_building_area_type exists set the swh_bat to the one given: `if building_segment.service_water_heating_building_area_type:`
    - set the building_segment_swh_bat to the building_segment.service_water_heating_building_area_type: `building_segment_swh_bat = building_segment.service_water_heating_building_area_type`

- return result: `return: building_segment_swh_bat`


**Returns** building_segment_swh_bat

**[Back](../_toc.md)**

**Notes:**
1. relies on re-structuring of SWH as in: https://github.com/open229/ruleset-model-description-schema/issues/264
