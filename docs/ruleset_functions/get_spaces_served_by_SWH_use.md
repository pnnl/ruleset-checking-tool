## get_spaces_served_by_SWH_use

Description: This function determines the spaces served by a given SWH use.  The convention is that if any spaces reference the swh_use, then the service water heating use applies to only those spaces. If no spaces reference the service water heating use, it applies to all spaces in the building segment.


Inputs:
- **RMD**
- **swh_use**

Returns:
- **spaces_served**: a list of spaces

Function Call:


Data Lookup: None

Logic:

- find the building_segment that contains this swh_use by looking through each building segment: `for building_segment in RMD.building_segments:`
    - check if the swh_use is in this building segment: `if swh_use in building_segment.service_water_heating_uses:`
        - create a list of spaces: `spaces_served = []`
          - look at each space in the building segment to see which of them reference the swh_use: `for space in building_segment...spaces:`
            - if the swh_use ID is in the list of space ServiceWaterHeatingUses, then the space is one of the spaces and we add it to the list: `if swh_use.id in space.service_water_heating_uses: spaces_served.append(space)`
        - return space_ids: `return spaces_served`



**Returns** space_ids

**[Back](../_toc.md)**

**Notes:**
1. relies on re-structuring of SWH as in: https://github.com/open229/ruleset-model-description-schema/issues/264
