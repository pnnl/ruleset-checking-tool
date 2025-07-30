## get_spaces_served_by_SWH_use

Description: This function determines the spaces served by a given SWH use.  The convention is that if any spaces reference the swh_use, then the service water heating use applies to only those spaces. If no spaces reference the service water heating use, it applies to all spaces in the building segment.


Inputs:
- **RMD**
- **swh_use_id**

Returns:
- **spaces_served**: a list of space ids


Logic:

- Initialize a list of spaces served: `spaces_served = []`
- Look through each building segment: `for building_segment in RMD...building_segments:`
    - if the swh_use is referenced by a building segment, then that use applies to every space within that building segment: `if swh_use_id in building_segment["service_water_heating_uses"]:`
      - return all spaces in that building segment: `return [space["id"] for space in building_segment...spaces]`
    - else, look through each space within the building segment: `for space in building_segment...spaces:`
        - if the swh_use is referenced directly by a space, add the space id to spaces_served: `if swh_use_id in space["service_water_heating_uses"]:`
            - append the space id to spaces_served: `spaces_served.append(space["id"])` 
- return the spaces served: `return spaces_served`



**Returns** space_ids list

**[Back](../_toc.md)**

**Notes:**  None 
