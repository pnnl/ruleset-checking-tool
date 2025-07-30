## get_building_segment_SWH_bat

Description: This function determines the SWH BAT for the given building segment.

Inputs:
- **RMD**
- **building_segment**

Returns:
- **building_segment_swh_bat**: one of the ServiceWaterHeatingSpaceOptions2019ASHRAE901 options

Function Call:

- get_energy_required_to_heat_swh_use  
- get_component_by_ID  

Data Lookup: None

Logic:

- get the service_water_heating_building_area_type: `building_segment_swh_bat = building_segment.get("service_water_heating_building_area_type", "UNDETERMINED")`

- if building segment doesn't have service water heating building area type defined, determine the building segment SWH area type by looking at individual SWH uses: `if building_segment_swh_bat == "UNDETERMINED":`
    - create a dictionary that will hold the different types of swh_use_bat_types and the total service water used for the year: `swh_use_dict = {}`
    - create a list of all swh use ids referenced by spaces: `swh_uses_from_spaces = find_all(f'$.buildings[*].building_segments[*][?(@.id == "{building_segment.id}")].zones[*].spaces[*].service_water_heating_uses[*]', rmd)`
    - create a list of all swh use ids referenced by the building segment: `swh_uses_from_building_segment = find_all(f'$.buildings[*].building_segments[*][?(@.id == "{building_segment.id}")].service_water_heating_uses[*]', rmd)`

    - look at each service water heating use: `for swh_use in swh_uses_from_spaces + swh_uses_from_building_segment:`
        - if any swh_use has use_units equal to "OTHER" or swh_use is an empty dict, the total energy required to heat the use cannot be determined, and building_segment_swh_bat is "UNDETERMINED":  
          `if swh_use and swh_use.use_units == "OTHER": building_segment_swh_bat = "UNDETERMINED"`
        - calculate the total energy required to heat the swh_use using the function get_energy_required_to_heat_swh_use:  
          `swh_use_energy_by_space = get_energy_required_to_heat_swh_use(swh_use, RMD, building_segment, is_leap_year)`
        - check to see if the swh_use has service_water_heating_area_type: `if swh_use.area_type:`
            - add the SWH building area type to the swh_use_dict and set the default value to 0: `swh_use_dict.setdefault(swh_use.area_type, 0)`
            - add the energy used by this swh_use: `swh_use_dict[swh_use.area_type] += sum(swh_use_energy_by_space.values())`
        - otherwise: `else:`
            - go through each space served by the swh_use and see if it has a service_water_heating_bat: `for space_id in swh_use_energy_by_space:`
                - get the space: `space = get_component_by_ID(RMD, space_id)`
                - check if the space has a swh_use_bat: `if space.service_water_heating_bat:`
                    - First add the BAT and set the default: `swh_use_dict.setdefault(space.service_water_heating_bat, 0)`
                    - add the energy used to the dict: `swh_use_dict[space.service_water_heating_bat] += swh_use_energy_by_space[space_id]`
                - otherwise, we'll add this use to UNDETERMINED: `else:`
                    - First add UNDETERMINED and set the default: `swh_use_dict.setdefault("UNDETERMINED", 0)`
                    - add the energy used to the dict: `swh_use_dict["UNDETERMINED"] += swh_use_energy_by_space[space_id]`

    - Determine the building segment SWH area type based on the following rules:  
        1) At least 50% of the SWH use energy must be assigned a known SWH area type (not "UNDETERMINED")  
        2) All assigned SWH energy must go to the same SWH area type  
        3) Otherwise, return "UNDETERMINED"

    - calculate total and assigned energy:  
      `total_energy = sum(swh_use_dict.values())`  
      `assigned_energy = total_energy - swh_use_dict.get("UNDETERMINED", 0)`

    - get list of known (non-UNDETERMINED) area types:  
      `known_area_types = [k for k in swh_use_dict if k != "UNDETERMINED"]`

    - if less than 50% of energy is assigned to a known area type: `if assigned_energy < 0.5 * total_energy:`  
        - set building_segment_swh_bat to UNDETERMINED: `building_segment_swh_bat = "UNDETERMINED"`

    - else if more than one known SWH area type exists: `elif len(known_area_types) > 1:`  
        - set building_segment_swh_bat to UNDETERMINED: `building_segment_swh_bat = "UNDETERMINED"`

    - else:  
        - set the building_segment_swh_bat to the only known area type:  
          `building_segment_swh_bat = known_area_types[0]`

- if the building segment service water heating building area type exists, set the swh_bat to the one given: `if building_segment.service_water_heating_building_area_type:`
    - set the building_segment_swh_bat to the building_segment.service_water_heating_building_area_type: `building_segment_swh_bat = building_segment.service_water_heating_building_area_type`

- return result: `return: building_segment_swh_bat`


**Returns** building_segment_swh_bat

**[Back](../_toc.md)**

**Notes:**
1. relies on re-structuring of SWH as in: https://github.com/open229/ruleset-model-description-schema/issues/264
