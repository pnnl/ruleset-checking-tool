# does_zone_meet_G3_1_1f
**Schema Version:** 0.0.22

**Description:** determines whether a given zone meets the G3_1_1f exception "If the baseline HVAC system type is 9 or 10, use additional system types for all HVAC zones that are mechanically cooled in the proposed design." - this function is only called if the expected baseline system type has already been confirmed to be system type 9 or 10

**Inputs:**
- **B-RMI** - the baseline building
- **zone_id** - the zone in the proposed building

**Returns:**  
- **result**: an enum - either YES or NO
 
**Function Call:**
- **is_zone_mechanically_cooled**

## Logic:
- set the result variable to NO - only a positive test can give it a different value: `result = NO`
- get the proposed zone: `zone_p = get_component_by_id(P-RMI, zone_id)for building_segment_p in P-RMI.building_segments:`
- check if the proposed is cooled: `if is_zone_mechanically_cooled(P-RMI, zone_p):`
	- `result = YES`

**Returns** `result`


**Notes/Questions:**  

