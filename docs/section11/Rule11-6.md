# HVAC_SystemZoneAssignment - Rule 11-6

**Schema Version:** 0.0.36  
**Mandatory Rule:** True  
**Rule ID:** 11-6  
**Rule Description:** Piping losses shall not be modeled. 
**Rule Assertion:** Options are PASS/FAIL/NOT_APPLICABLE/UNDETERMINED  
**Appendix G Section Reference:** Table G3.1 #11, baseline column, i

**Evaluation Context:** Each SWH BAT  
**Data Lookup:**   
**Function Call:**

1. get_SHW_equipment_associated_with_each_SWH_bat()

**Applicability Checks:**
- Each SHW use type is applicable if there are SHW loads
- also use get_SHW_equipment_associated_with_each_SWH_bat to get the SHW BATs and SHW use in the building: `shw_bats_and_use_dict = get_SHW_equipment_associated_with_each_SWH_bat(P_RMD)`
- look through each of the SHW BATs in the building: `for shw_bat in shw_bats_and_use_dict:`
  - check if there are SHW loads in this use type, continue to rule logic: `if len(shw_bats_and_use_dict[shw_bat]) > 0: RULE_APPLICABLE`
  - otherwise, rule is not applicable for this shw_bat: `else: NOT_APPLICABLE`


    ## Rule Logic:
    - create a value indicating whether piping losses were modeled: `piping_losses_modeled = false`
    - look at every ServiceWaterPiping connected to the shw_bat: `for piping_id in shw_bats_and_use_dict[shw_bat]["Piping"]`
      - get the piping: `piping = get_component_by_id(piping_id, B_RMD, ServiceWaterPiping) `
      - check if the piping has piping_losses_modeled: `if piping.piping_losses_modeled:`
        - set the piping_losses_modeled to true: `piping_losses_modeled = true`

    - **Rule Assertion - Zone:**
    - Case1: piping losses are not modeled, PASS: `if !piping_losses_modeled: PASS`
    - Case2: piping losses are modeled, FAIL: `else: FAIL`


**Notes:**

**[Back](../_toc.md)**
