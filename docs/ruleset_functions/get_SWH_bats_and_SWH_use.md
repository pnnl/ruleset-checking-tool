## get_SWH_bats_and_SWH_use

Description: This function gets all the SWH Uses and the SWH space types and sorts them into a dictionary where the keys are the ServiceWaterHeatingBuildingAreaOptions2019ASHRAE901 and values are a list if ServiceWaterHeatingUse.ids  

Inputs:
- **RMD**

Returns:
- **swh_bat_and_SWH_use_dict**: A dictionary containing where the keys are the ServiceWaterHeatingSpaceOptions2019ASHRAE901 in the RMD and values are lists of SWHUse ids.  Example:  
{"DORMITORY":["swh1","swh2","swh3"], "AUTOMOTIVE_FACILITY":["swhg1","swhg2","swhg3"]}

Function Call:
- **get_SWH_uses_associated_with_each_building_segment**  
- **get_building_segment_SWH_bat**  
- **get_component_by_id**  

Logic:
- create a blank dictionary: `swh_and_SWH_use_dict = {}`
- look at each building segment: `for building_segment in RMD.building_segments:`
    - get the swh_bat by using the function: get_building_segment_SWH_bat: `swh_bat = get_building_segment_SWH_bat(RMD,building_segment)`
    - add this bat to swh_and_SWH_use_dict if it doesnt exist yet: `swh_and_SWH_use_dict.set_default(swh_bat,[])`
    - get the service water heating uses in the building segment `service_water_heating_use_ids = get_SWH_uses_associated_with_each_building_segment(P_RMD, building_segment.id)`
    - add all of the swh_use ids in the building segment to the list: `for swh_use in building_segment.service_water_heating_uses:`
        - append the id of the swh_use to the list: `swh_and_SWH_use_dict[swh_bat].append(swh_use.id)`

**Returns** swh_and_SWH_use_dict

**[Back](../_toc.md)**

**Notes:**

