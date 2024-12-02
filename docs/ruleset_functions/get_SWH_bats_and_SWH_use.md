## get_SWH_bats_and_SWH_use

Description: This function gets all the SWH Uses and the SWH space types and sorts them into a dictionary where the keys are the ServiceWaterHeatingBuildingAreaOptions2019ASHRAE901 and values are a list of ServiceWaterHeatingUse.ids  

Inputs:
- **RMD**

Returns:
- **swh_bat_and_SWH_use_dict**: A dictionary containing where the keys are the ServiceWaterHeatingSpaceOptions2019ASHRAE901 in the RMD and values are lists of SWHUse ids.  Example:  
{"DORMITORY":["swh1","swh2","swh3"], "AUTOMOTIVE_FACILITY":["swhg1","swhg2","swhg3"]}

Function Call:
- **get_building_segment_SWH_bat**  
- **get_component_by_id**  

Logic:
- create a blank dictionary: `swh_and_SWH_use_dict = {}`
- look at each building segment: `for building_segment in RMD.building_segments:`
    - get the swh_bat by using the function: get_building_segment_SWH_bat: `swh_bat = get_building_segment_SWH_bat(RMD,building_segment["id"])`
    - add this bat to swh_and_SWH_use_dict if it doesnt exist yet: `swh_and_SWH_use_dict.setdefault(swh_bat,[])`
    - get the service water heating use ids in the building segment `service_water_heating_use_ids = find_all(               f'$.buildings[*].building_segments[*][?(@.id="{bldg_seg_id}")].zones[*].spaces[*].service_water_heating_uses[*].id', rmd)`
    - add all of the swh_use ids in the building segment to the list: `service_water_heating_use_ids[swh_bat].extend(service_water_heating_use_ids) `

**Returns** swh_and_SWH_use_dict

**[Back](../_toc.md)**

**Notes:**

