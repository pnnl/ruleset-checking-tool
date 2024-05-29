# Service_Water_Heating - Rule 11-7  
**Schema Version:** 0.0.36  

**Mandatory Rule:** TRUE

**Rule ID:** 11-7  

**Rule Description:** Except in buildings that will have no service water heating loads,  the service water heating systems type in the baseline building design shall be as specified in Table G3.1.1-2 for each building area type in the proposed design. 

**Rule Assertion:** Options are PASS/FAIL

**Appendix G Section Reference:** Table G3.1 #11, baseline column, a & b

**Evaluation Context:** B-RMD each SWH Equipment
**Data Lookup:**   
- **Table G3.1.1-2(shw_bat)**
**Function Call:** 
- **get_component_by_id**
- **get_SHW_equipment_associated_with_each_SWH_bat**  
- **get_SHW_types_and_SHW_use**
- **get_SHW_equipment_type**  

**Applicability Checks:**
- Each SHW use type is applicable if there are SHW loads
- use get_SHW_equipment_associated_with_each_SWH_bat to get the SHW use types and SHW use in the building: `shw_bats_and_equip_dict = get_SHW_equipment_associated_with_each_SWH_bat(B_RMD)`

- call the function get_SHW_types_and_SHW_use for the proposed: `shw_bat_and_use_dict_p = get_SHW_types_and_SHW_use(P_RMD)`
- look through each of the SHW bats in the building: `for shw_bat in shw_bat_and_use_dict_p:`
  - check if there are SHW loads in this use type, continue to rule logic: `if len(shw_bat_and_use_dict_p[shw_bat]) > 0: CONTINUE TO RULE LOGIC`
  - otherwise, rule is not applicable for this shw_bat: `else: NOT_APPLICABLE`

  ## Rule Logic: 
  - look at each SWH Equipment in the shw_bat - there should only be one, but this is checked in rule 11-8: `for swh_equip_id in shw_bats_and_equip_dict[shw_bat]["SHWHeatingEq"]:`
    - get the SHW equipment type using the function get_SHW_equipment_type: `shw_equip_type = get_SHW_equipment_type(B_RMD, swh_equip_id)`
    - get the expected SHW equipment type by looking it up in the table G3.1.1-2: `expected_shw_equip_type = data_lookup(Table G3.1.1-2, shw_bat)`



## Rule Assertion: 
- Case1: the expected_shw_equip_type matches shw_equip_type: PASS: `if expected_shw_equip_type == shw_equip_type: PASS`
- Case2: the expected_shw_equip_type doesn't match shw_equip_type, `FAIL: else: FAIL`

  
  **Notes:**
  1.  The rule states bats for the proposed, but this is complex to check - can we add that SHW uses need to have the same use type to the section 1 general checks?

**[Back](../_toc.md)**
