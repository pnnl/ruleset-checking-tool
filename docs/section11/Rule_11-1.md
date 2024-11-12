# Service_Water_Heating - Rule 11-1
**Schema Version:** 0.0.37  

**Mandatory Rule:** TRUE

**Rule ID:** 11-1

**Rule Description:** "Where a complete service water-heating system exists, the proposed design shall reflect the actual system type. Where a service water-heating system has been designed the service waterheating type shall be consistent with design documents.  Where no service water-heating system exists or has been designed and submitted with design documents but the building will have service water-heating loads, a service water-heating system shall be modeled that matches the system type in the baseline building design"

**Rule Assertion:** Options are PASS/FAIL

**Appendix G Section Reference:** Table G3.1 #11, proposed column, a & b

**Evaluation Context:** custom evaluation context created for this rule of all SWH Distribution system ids located in the proposed, baseline and user RMDs  
**Data Lookup:**   
**Function Call:**  
- **get_component_by_id**  
- **compare_swh_dist_systems_and_components**
- **compare_context_pair** - there is no RDS for this function, but it is a function developed for Rule 1-6 that compares two elements  
- **get_swh_components_associated_with_each_swh_distribution_system**  


**Applicability Checks:**
- check that the U_RMD has SWH Uses with loads

## Applicability Checks:
- in this case, all of the SWH Distribution IDs identified when the custom context was created are applicable to this rule.
- Look at each swh distribution system id: `for swh_dist_system_id in context: CONTINUE TO RULE LOGIC`

  ## Rule Logic #
  - there are a couple cases here:
    1.  If the swh distribution exists in the user model, AND has swh use, then expect user and proposed systems to be match
    2.  Otherwise, expect the distribution system to match between proposed and baseline
    3.  Systems that don't do 1 or 2 fail
  
  - create a variable user_proposed_str, which is the string lookup used by compare_context_pair for comparing elements between the user and proposed RMDS: `user_proposed_str = "AppG 11-1 P_RMD Equals U_RMD"`
  - create a variable base_proposed_str, which is the string lookup used by compare_context_pair for comparing elements between the user and proposed RMDS: `base_proposed_str = "AppG 11-1 P_RMD Equals B_RMD"`
  - set a boolean user_proposed_comparison to FALSE: `user_proposed_comparison = FALSE`
  - set a boolean user_baseline_comparison to FALSE: `user_baseline_comparison = FALSE`
  
  - Check whether the system exists in the user model: `if u_swh_system_and_equip_dict[swh_dist_system_id]:`
    - check whether the system has SWH uses in the user model: `if u_swh_system_and_equip_dict[swh_dist_system_id]["USES"]:`
      - get the user swh_use: `u_swh_use = get_component_by_id(U_RMD, swh_use_id)`
      - if the u_swh_use exists, and is greater than zero: `if u_swh_use != NULL and u_swh_use.use > 0:`
        - compare the proposed and user models using the function compare_swh_dist_systems_and_components.  This function returns a list of errors.  If the list of errors has a length of 0, then the comparison encountered no issues: `user_proposed_comparison = compare_swh_dist_systems_and_components(P_RMD,U_RMD,user_proposed_str,swh_dist_system_id)`
        - from here, go directly to the rule assertion: `GO TO RULE ASSERTION`

  - if we got to this line without going to the rule assertion, it means that there is no equivalent system in the user model, or that the user model does not have SWH use.  Compare the proposed and baseline models using the function compare_swh_dist_systems_and_components.  This function returns a list of errors.  If the list of errors has a length of 0, then the comparison encountered no issues: `user_baseline_comparison = compare_swh_dist_systems_and_components(P_RMD,B_RMD,user_proposed_str,swh_dist_system_id)`
  
  - now go to rule assertion: `GO TO RULE ASSERTION`
    

## Rule Assertion: 
- Case1: if the length of either user_proposed_comparison or user_baseline comparison is 0, then the rule passes: `if (len(user_proposed_comparison) == 0) || (len(user_baseline_comparison) == 0): PASS`
- Case2: all other cases, FAIL: `else: FAIL`



**[Back](../_toc.md)**
