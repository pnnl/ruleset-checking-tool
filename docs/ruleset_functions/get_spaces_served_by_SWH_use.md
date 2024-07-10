## get_spaces_served_by_SWH_use

Description: This function determines the spaces served by a given SWH use.  The rule is that if spaces reference the swh_use, then the use applies to only those spaces.  If the use references no spaces, it applies to all spaces in the building segment.


Inputs:
- **RMD**
- **swh_use**

Returns:
- **spaces_served**: a list of space ids

Function Call:


Data Lookup: None

Logic:

- find the building_segment that contains this swh_use by looking through each building segment: `for building_segment in RMD.building_segments:`
    - check if the swh_use is in this building segment: `if swh_use in? building_segment.service_water_heating_uses:`
        - create a list of spaces: `spaces = []`
        - look eat each building segment: `for building_segment in RMD.building_segments`
            - check if the swh_use is in this building_segment: `if swh_use in? building_segment.service_water_heating_uses:`
                - look at each space in the building segment to see which of them reference the swh_use: `for space in building_segment.spaces:`
                    - if the swh_use ID is in the list of space ServiceWaterHeatingUses, then the space is one of the spaces and we add it to the list: `if swh_use.id in? space.service_water_heating_uses: spaces << space`
        - here, we check whether there are any spaces applied to the swh_use.  If no spaces are applied, then this use applies to all spaces in the building_segment: `if len(spaces) == 0: spaces = building_segment.spaces`
        - convert the list of spaces to a list of space ids: `space_ids = [space.id for space in spaces]
        - return space_ids: `return space_ids`



- return result: `return: building_segment_swh_bat`


**Returns** swh_and_spaces_dict

**[Back](../_toc.md)**

**Notes:**
1. relies on re-structuring of SWH as in: https://github.com/open229/ruleset-model-description-schema/issues/264
