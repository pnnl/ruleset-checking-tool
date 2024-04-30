# HVAC_SystemZoneAssignment - Rule 11-6

**Schema Version:** 0.0.36  
**Mandatory Rule:** True  
**Rule ID:** 11-6  
**Rule Description:** Piping losses shall not be modeled. 
**Rule Assertion:** Options are PASS/FAIL/NOT_APPLICABLE/UNDETERMINED  
**Appendix G Section Reference:** Table G3.1 #11, proposed column, f

**Evaluation Context:** Each SWH space type  
**Data Lookup:**   
**Function Call:**

1. get_SHW_equipment_connected_to_use_type()
2. get_SHW_types_and_SHW_use()

**Applicability Checks:**
- Each SHW use type is applicable if there are SHW loads
- call the function get_SHW_equipment_connected_to_use_type: `shw_equip_dict = get_SHW_equipment_connected_to_use_type(B_RMD)`
- also use get_SHW_types_and_SHW_use to get the SHW use types and SHW use in the building: `shw_types_and_use_dict = get_SHW_types_and_SHW_use(P_RMD)`
- look through each of the SHW types in the building: `for shw_use_type in shw_types_and_use_dict:`
  - check if there are SHW loads in this use type, continue to rule logic: `if len(shw_types_and_use_dict[shw_use_type]) > 0: RULE_APPLICABLE`
  - otherwise, rule is not applicable for this shw_use_type: `else: NOT_APPLICABLE`


    ## Rule Logic:
    - create a value indicating whether piping losses were modeled: `piping_losses_modeled = false`
    - look at every ServiceWaterPiping connected to the shw_use_type: `for piping_id in shw_types_and_use_dict[shw_use_type]["Piping"]`
      - get the piping: `piping = get_component_by_id(piping_id, B_RMD, ServiceWaterPiping) `
      - check if the piping has piping_losses_modeled: `if piping.piping_losses_modeled:`
        - set the piping_losses_modeled to true: `piping_losses_modeled = true`

    - **Rule Assertion - Zone:**
    - Case1: piping losses are not modeled, PASS: `if !piping_losses_modeled: PASS`
    - Case2: piping losses are modeled, FAIL: `else: FAIL`


**Notes:**

**[Back](../_toc.md)**
