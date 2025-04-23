## get_SWH_uses_associated_with_each_building_segment

Description: This function gets all the SWH uses connected to a building segment. This function is primarily to encapsulate getting service water heating uses in one function so that if a change is made in the schema as to how service water heating use is specified, the RCT only needs to change in one place.   

Inputs:
- **RMD**  

Returns:
- **swh_uses_dict**:  A dictionary where the keys are all the building segment ids and the value is a list `service_water_heating_uses` objects.   

Function Call:
- get_obj_by_id  

Data Lookup: None

Logic:
- define `swh_uses_dict`: `swh_uses_dict = {}`
- look at each building segment in the building: `for bldg_seg in find_all("$.buildings[*].building_segments[*]", rmd):`
	- create the list for this building segment: `swh_uses_dict[bldg_seg.id] = []`
	- look at each swh use in the building segment: `for swh_use in bldg_seg.service_water_heating_uses:`
		- append the swh use id to the bldg_seg list: `swh_uses[bldg_seg.id].append(swh_use.id)`
	- look at each space in the building segment: `for space in build_seg...spaces:`
		- look at each service water heating use in the space - note to DEV team - we are only interested in actual objects, not references: `for swh_use in space.service_water_heating_uses:`
			- append the swh use id to the bldg_seg list: `swh_uses[bldg_seg.id].append(swh_use.id)`
			
			
**Returns** swh_uses_dict

**[Back](../_toc.md)**

**Notes:**
