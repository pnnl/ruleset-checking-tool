# Service_Water_Heating - Rule 11-8
**Schema Version:** 0.0.37  

**Mandatory Rule:** TRUE

**Rule ID:** 11-8

**Rule Description:** "One system per building area type shall be modeled in the baseline."

**Rule Assertion:** Options are PASS/FAIL/NOT_APPLICABLE

**Appendix G Section Reference:** Table G3.1 #11, baseline column, a + b

**Evaluation Context:** B-RMD each SWH BAT  
**Data Lookup:**   
**Function Call:**  
- **get_SWH_components_associated_with_each_SWH_bat**  
- **get_building_segment_SWH_bat**  
- **get_SWH_bats_and_SWH_use**  


## Applicability Checks:
- Each SWH bat is applicable if there are SWH loads in the BAT in the proposed model

- call the function get_SWH_bats_and_SWH_use for the proposed: `swh_bats_and_uses_p = get_SWH_bats_and_SWH_use(P_RMD)`
- look through each of the SWH BATs in the building: `for swh_bat in swh_bats_and_uses_p:`
    - look at each service water heating use in the BAT: `for swh_use_id in swh_bats_and_uses_p[swh_bat]:`
      - get the swh use from the swh_use_id: `swh_use = get_component_by_id(P_RMD, swh_use_id)`
      - check if there are SWH loads in this use, continue to rule logic.  In this case, we are not worried about the use_units, we just want to know that there is a use that is greater than 0: `if swh_use.use > 0: CONTINUE TO RULE LOGIC`
    - otherwise, rule is not applicable for this swh_bat: `else: NOT_APPLICABLE`

        ## Rule Logic: 
    - use get_SWH_components_associated_with_each_SWH_bat to get the SWH use types and SWH use in the building: `swh_bats_and_equip_dict = get_SWH_components_associated_with_each_SWH_bat(B_RMD)`
    - get a dictionary of all SWH equipment connected to the current SWH BAT in the baseline model: `swh_bats_and_equip_dict_this_use = swh_bats_and_equip_dict[swh_bat]`
    - get the quantity of service water heating distribution systems serving this building area type: `num_swh_systems = len(swh_bats_and_equip_dict_this_use["SWHDistribution"])`
    - get the quantity of service water heating equipment serving this building area type: `num_swh_equipment_this_use = len(swh_bats_and_equip_dict_this_use["SWHHeatingEq"])`
    - create a boolean is_referenced_in_other_bats and set it to false: `is_referenced_in_other_bats = false`
    
    - if there is exactly one system, check that the system is not used in any of the other BATs: `if num_swh_systems == 1:`
        - create a variable swh_dist_id and set it to the id of the swh distribution system for this bat: `swh_dist_id = swh_bats_and_equip_dict_this_use["SWHDistribution"][0]`
        - loop through each BAT: `for other_swh_bat in swh_bats_and_equip_dict:`
        - if other_swh_bat is not equal to the current swh_bat: `if other_swh_bat != swh_bat:`
            - check whether the swh_dist_id is in the list of SWH Distribution system for the other SWH_bat: `if swh_dist_id in swh_bats_and_equip_dict[other_swh_bat]["SWHDistribution"]:`
            - set the boolean is_referenced_in_other_bats to true: `is_referenced_in_other_bats = true`
    - create a boolean called multiple_segments_with_bat_other and set it to false.  This boolean will tell us if the a) the swh_bat is "OTHER"; b) there are multiple building segments with swh_bat equal to "OTHER": `multiple_segments_with_bat_other = false` 
    - check whether the swh_bat is "OTHER": `if swh_bat == "OTHER":`
        - now create a variable num_segments and set it to 0.  This variable will be used to count the number of building segments with swh_bat == "OTHER": `num_segments = 0`
        - now look at each building segment in the building: `for building_segment in B_RMD:`
            - get the building segment swh_bat.  If it's "OTHER" increment, num_segments: `if (get_building_segment_SWH_bat(B_RMD, building_segment) == "OTHER"): num_segments += 1`
        - check whether there are multiple building segments with swh_bat "OTHER", if so, set the boolean other equal to true: `if num_segments > 1: multiple_segments_with_bat_other = true`

    ## Rule Assertion: 
    - Case1: there is more than one swh system in the building segment: FAIL: `if num_swh_systems > 1: FAIL`
    - Case2: The SWH BAT is "UNDETERMINED", there is only one building segment in the model: PASS: `elif shw_bat == "UNDETERMINED" && len(B_RMD.building.building_segments) == 1: PASS`
    - Case3: The SWH BAT is "UNDETERMINED" and there is more than one building segment: UNDETERMINED & provide a note: `elif swh_bat == "UNDETERMINED": UNDETERMINED note = "The Service Water Heating Building Area type for this building segment is undetermined, and there are multiple building segments in the project.  Therefore it cannot be determined whether this building segment shares a service water heating building area type with one of the other building segments."`
    - Case4: the swh_bat is "OTHER" and is applied to more than one building segment - there could be multiple types of "OTHER" SWH BAT's - return UNDETERMINED: `elif multiple_segments_with_bat_other: UNDETERMINED; note = "The Service Water Heating Building Area Type is 'OTHER' and is applied to multiple building segments.  'OTHER' can describe multiple Service Water Heating Building Area Types.  Confirm that Service Water Heating Building Area Type is provided with one and only one service water heating system.`
    - Case5: the system is not referenced by any other swh_bats: PASS: `elif is_referenced_in_other_bats == false: PASS`
    - Case6: all else, FAIL: `else: FAIL`

  
  **Notes:**
  1.  Are there configurations in which a complete SWH system could exist without SWHDistribution? - ANSWER: distrbution_system is a required data element, so no.
  2.  Is more than one SWH Equipment allowed per building segment (water heater?)

**[Back](../_toc.md)**