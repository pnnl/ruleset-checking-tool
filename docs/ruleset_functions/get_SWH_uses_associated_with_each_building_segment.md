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
- in each building segment, the service water heating uses can be defined at the building segment level or at the space level.  Look at each building segment: `for bldg_seg in RMD....building_segments:`
    - create the list for this building segment: `swh_uses_dict[bldg_seg.id] = []`
    - at the building segment level, service_water_heating_uses gives a list: [({ServiceWaterHeatingUse}, Reference)] - look at each service water heating use: `for swh_use in bldg_seg.service_water_heating_uses:`
        - append the use to the list if it is an actual use, and not a reference - if it is a reference, it'll be located at the space level, and we'll add it when we look at each space: `if type(swh_use) == ServiceWaterHeatingUse: swh_uses_dict[bldg_seg.id].append(swh_use)`
    - look at each space within the building segment: `for space in bldg_seg...spaces:`
        - at the space level, service_water_heating_uses gives a list: [({ServiceWaterHeatingUse}, Reference)] - look at each service water heating use: `for swh_use in space.service_water_heating_uses:`
            - append the use to the list if it is an actual use, and not a reference - if it is a reference it should've been stored at the building segment level and should already be in the list: `if type(swh_use) == ServiceWaterHeatingUse: swh_uses_dict[bldg_seg.id].append(swh_use)`

**Returns** swh_uses_dict

**[Back](../_toc.md)**

**Notes:**
