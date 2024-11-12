# Service Water Heating - Rule 11-6

**Schema Version:** 0.0.37  
**Mandatory Rule:** True  
**Rule ID:** 11-6  
**Rule Description:** Piping losses shall not be modeled.   
**Rule Assertion:** Options are PASS/FAIL/NOT_APPLICABLE/UNDETERMINED  
**Appendix G Section Reference:** Table G3.1 #11, baseline column, i

**Evaluation Context:** Each SWH Distribution System  
**Data Lookup:**   
**Function Call:**
1. get_swh_components_associated_with_each_swh_distribution_system()

**Applicability Checks:**
- Every Baseline distribution system is applicable


    ## Rule Logic:
- use get_swh_components_associated_with_each_swh_distribution_system to get the SWH BATs and SWH equipment in the building: `swh_distribution_and_eq_dict = get_swh_components_associated_with_each_swh_distribution_system(B_RMD)`
    - create a value indicating whether piping losses were modeled: `piping_losses_modeled = false`
    - look at every ServiceWaterPiping including child pipings connected to the distribution: `for piping_id in swh_distribution_and_eq_dict[distribution_id]["Piping"]`
        - get the piping: `piping = get_component_by_id(piping_id, B_RMD, ServiceWaterPiping) `
        - check if the piping has piping_losses_modeled: `if piping.are_thermal_losses_modeled:`
            - set the piping_losses_modeled to true and go directly to rule assertion: `piping_losses_modeled = true: GO TO RULE_ASSERTION`

    - **Rule Assertion - Zone:**
    - Case1: piping losses are not modeled, PASS: `if piping_losses_modeled == False: PASS`
    - Case2: piping losses are modeled, FAIL: `else: FAIL`


**Notes:**

**[Back](../_toc.md)**
