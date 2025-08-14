## get_SWH_uses_associated_with_each_building_segment

Description: This function gets all the SWH uses connected to a building segment. This function is primarily to encapsulate getting service water heating uses in one function so that if a change is made in the schema as to how service water heating use is specified, the RCT only needs to change in one place.   

Inputs:
- **RMD**  

Returns:
- **swh_uses_dict**:  A dictionary where the keys are all the building segment ids and the value is `service_water_heating_uses` object under the `service_water_heating_uses`.   

Function Call:
- get_obj_by_id  

Data Lookup: None

Logic:
- define `swh_uses_dict`: `swh_uses_dict = {}`
- look at each swh use: `for bldg_seg in find_all("$.buildings[*].building_segments[*]", rmd)`  
    - append the use to the list: `swh_uses_dict = {bldg_seg["id"]: find_all("$.zones[*].spaces[*].service_water_heating_uses[*]", rmd)}`   

**Returns** swh_uses_dict

**[Back](../_toc.md)**

**Notes:**
