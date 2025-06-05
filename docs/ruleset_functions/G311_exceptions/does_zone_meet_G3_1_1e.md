# does_zone_meet_G3_1_1e
**Schema Version:** 0.0.22  

**Description:** determines whether a given zone meets the G3_1_1e exception "Thermal zones designed with heating-only systems in the proposed design serving storage rooms, stairwells, vestibules, electrical/mechanical rooms, and restrooms not exhausting or transferring air from mechanically cooled thermal zones in the proposed design shall use system type 9 or 10 in the baseline building design."

**Inputs:**
- **P-RMI**
- **B-RMI**
- **zone_id**

**Returns:**  
- **result**: boolean, True eligible but maybe the zone is a vestibule, False, not eligible
 
**Function Call:**
- **is_a_vestibule**
- **is_zone_mechanically_heated_and_not_cooled**
- **get_component_by_id**

## Logic:
- create list of eligible space types: `eligible_space_types = ["STORAGE_ROOM_HOSPITAL", "STORAGE_ROOM_SMALL", "STORAGE_ROOM_LARGE", "WAREHOUSE_STORAGE_AREA_MEDIUM_TO_BULKY_PALLETIZED_ITEMS", "WAREHOUSE_STORAGE_AREA_SMALLER_HAND_CARRIED_ITEMS", "STAIRWELL", "ELECTRICAL_MECHANICAL_ROOM", "RESTROOM_FACILITY_FOR_THE_VISUALLY_IMPAIRED", "RESTROOM_ALL_OTHERS"]
- set the result variable to No - only a positive test can give it a different value: `result = False`
- set eligibility boolean to TRUE: `eligible = TRUE`
- get the zone in the P-RMI: `zone_p = get_component_by_id(P-RMI,zone_id)`
- get the zone in the B-RMI: `zone_b = get_component_by_id(B-RMI,zone_id)`
- For each space in zone_b: `for space_b in zone_b.Spaces:`
    - check if the space has an eligible lighting type: `if space_b.lighting_space_type not in eligible_space_types:`
        - set eligibility to False - any non-compliant space type will result in a non-eligible zone: `eligible = FALSE`

- if the zone is not eligible, check if it is a vestibule: `if not eligible:`
    - set variable is_a_vestibule = is_zone_a_vestibule: `is_a_vestibule = is_zone_a_vestibule(zone_b, B-RMI)`
    - if the result is not equal to no, then it is eligible to be a vestibule: `if is_a_vestibule != NO:`
        - set eligible to true: `eligible = TRUE`

- if the zone is still eligible: `if eligible:`
    - check if the proposed has a heating-only system by using the is_zone_mechanically_heated_and_not_cooled function: `if not is_zone_mechanically_heated_and_not_cooled(P-RMI,zone_p)`
        - mechanically cooled zones are not eligible: `eligible = FALSE`

- if the zone is still eligible: `if eligible:`
    - set result to YES: `result = True`
	
    '''
	I am moving this logic to zone_target_baseline_system.
    - we still need to signal if the zone is MAYBE a vestible.  We only do this if the zone is eligible in all the other checks.  So if the proposed zone is mechanically cooled, it doesn't matter if this is a vestibule or not: `if is_a_vestibule == MAYBE:`
        - set result to MAYBE_VESTIBULE: result = `MAYBE_VESTIBULE`
    '''


**Returns** `result`


**Notes/Questions:**  


**[Back](../_toc.md)**
