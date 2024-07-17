# Service_Water_Heating - Rule 11-7  
**Schema Version:** 0.0.37  

**Mandatory Rule:** TRUE

**Rule ID:** 11-7  

**Rule Description:** Except in buildings that will have no service water heating loads, the service water heating system type in the baseline building design shall be as specified in Table G3.1.1-2 for each building area type in the proposed design. 

**Rule Assertion:** Options are PASS/FAIL/NOT_APPLICABLE

**Appendix G Section Reference:** Table G3.1 #11, baseline column, a & b

**Evaluation Context:** B-RMD each SWH Equipment  
**Data Lookup:**   
- **Table G3.1.1-2(swh_bat)**  
**Function Call:**  
- **get_component_by_id**  
- **get_SWH_equipment_associated_with_each_SWH_bat**  
- **get_SWH_bats_and_SWH_use**  
- **get_SWH_equipment_type**  

**Applicability Checks:**
- Note: Applicability is determined at the building segment level, but the rule is evaluated for all SWH equipment serving the building segment.
- Each SWH bat is applicable if there are SWH loads in the BAT in the proposed model

- call the function get_SWH_bats_and_SWH_use for the proposed: `swh_bats_and_uses_p = get_SWH_bats_and_SWH_use(P_RMD)`
- look through each of the SWH bats in the building: `for swh_bat in swh_bats_and_uses_p:`
    - look at each service water heating use in the BAT: `for swh_use_id in swh_bats_and_uses_p[swh_bat]:`
      - get the swh use from the swh_use_id: `swh_use = get_component_by_id(P_RMD, swh_use_id)`
      - check if there are SWH loads in this use, continue to rule logic.  In this case, we are not worried about the use_units, we just want to know that there is a use that is greater than 0: `if swh_use.use > 0: CONTINUE TO RULE LOGIC`
    - otherwise, rule is not applicable for this swh_bat: `else: NOT_APPLICABLE`

  ## Rule Logic: 
  - use get_SWH_equipment_associated_with_each_SWH_bat to get the SWH use types and SWH use in the building: `swh_bats_and_uses_b = get_SWH_equipment_associated_with_each_SWH_bat(B_RMD)`
  - look at each SWH Equipment in the swh_bat.  Appendix G requires only one system per bat, but this is covered in rule 11-8, so here we will allow multiple SWH equipment: `for swh_equip_id in swh_bats_and_uses_b[swh_bat]["SWHHeatingEq"]:`
    - get the SWH equipment type using the function get_SWH_equipment_type: `swh_equip_type = get_SWH_equipment_type(B_RMD, swh_equip_id)`
    - get the expected SWH equipment type by looking it up in the table G3.1.1-2: `expected_swh_equip_type = data_lookup(Table G3.1.1-2, swh_bat)`



## Rule Assertion: 
- Case1: the expected_swh_equip_type matches swh_equip_type: PASS: `if expected_swh_equip_type == swh_equip_type: PASS`
- Case2: the expected_swh_equip_type doesn't match swh_equip_type, `FAIL: else: FAIL`

  
  **Notes:**
  1.  The rule states bats for the proposed, but this is complex to check - can we add that SWH uses need to have the same use type to the section 1 general checks?

**[Back](../_toc.md)**
