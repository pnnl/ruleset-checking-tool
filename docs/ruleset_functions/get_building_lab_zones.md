# get_building_lab_zones  

**Schema Version:** 0.0.28

**Description:** returns a list of all of the zones in the building that include a laboratory space

**Inputs:** 
- **P_RMI**

**Returns:**  
- **laboratory_zones_list**: a list of zone.ids for all zones that have a laboratory space in the building
 
**Function Call:**


## Logic:
- create a list of laboratory zones: `laboratory_zones_list = []`
- we want to do the exhaust air volume calculations based on the P_RMI, so find all laboratory zones in the P_RMI by looping through zones: `for z in P_RMI...zones:`
  - set is_laboratory to false: `is_laboratory = false`
  - look through all spaces in the z to see if at least one of them is a laboratory: `for space in z.spaces:`
    - look for LABORATORY space.function: `if space.function == LABORATORY:`
      - set is_laboratory to true: `is_laboratory = true`
  - if is_laboratory is true, add the z to the laboratory_zones_list: `if is_laboratory == true: laboratory_zones_list.append z.id`



**Returns** `laboratory_zones_list`

**Notes**


**[Back](../_toc.md)**

