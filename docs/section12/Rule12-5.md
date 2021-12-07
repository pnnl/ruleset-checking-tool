
# Receptacle - Rule 12-5

**Rule ID:** 12-5  
**Rule Description:** User RMR Receptacle Power in Proposed RMR?  
**Rule Assertion:** Proposed RMR = User RMR  
**Appendix G Section:** Section G3.1-12 Modeling Requirements for the Proposed design  
**Appendix G Section Reference:** None  

**Applicability:** All required data elements exist for P_RMR and U_RMR  
**Applicability Checks:**  

  1. Rule 12-3 = True  

**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  

## Rule Logic:  

- **Applicability Check 1:** `if (rule-12-3.status == TRUE):`

- Get the receptacle load of each space in the building segment in the User model, for each zone in U_RMR: `for zone_user in U_RMR...zones:`  

  - For each space from thermal zone: `space_user in zone_user.spaces:`  

    - Get the total miscellaneous_equipment in the space: `space_total_misc_equipment_user = sum( equipment.peak_usage for equipment in space_user.miscellaneous_equipment )`  

    - Get matching space from Proposed RMR: `space_proposed = match_data_element(P_RMR, spaces, space_user.id)`

      - Get the total miscellaneous_equipment in the space: `space_total_misc_equipment_proposed = sum( equipment.peak_usage for equipment in space_proposed.miscellaneous_equipment )`  

        **Rule Assertion - Component:** 

        - Case 1: For each space, if U-RMR receptacle power is modeled the same as in P-RMR: `if space_total_misc_equipment_user == space_total_misc_equipment_proposed: PASS`  

        - Case 2: Else, save space to output array: `else: FAIL and fail_check_array.append(space_user.id)`

**Rule Assertion - RMR:** 

- Case 1: If all spaces in U-RMR pass rule: `PASS`

- Case 2: Else, at least one of the spaces in U-RMR fails rule: `FAIL and raise_message "THE SPACES IN U-RMR LISTED BELOW IS NOT MODELED WITH THE SAME RECEPTACLE POWER AS IN P-RMR: ${fail_check_array}"`

**[Back](../_toc.md)**
