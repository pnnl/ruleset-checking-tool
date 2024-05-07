# Receptacles – Rule 12-1   
**Schema Version:** 0.0.36        
**Mandatory Rule:** True          
**Rule ID:** 12-1  
**Rule Description:** Receptacle and process power shall be modeled as identical to the proposed design  
**Rule Assertion:** B-RMD = P-RMD                                           
**Appendix G Section:** G3.1  
**Appendix G Section Reference:** Table G3.1-12  
**Data Lookup:** None  
**Evaluation Context:** Each RPD  

**Applicability Checks:**  
N/A

**Function Call:**  
match_data_element

## Rule Logic:
- Store a list of any miscellaneous equipment power that does not match between baseline and proposed: `mismatched_misc_equipment_power = []`
- For each miscellaneous equipment load in the baseline RMD: `for misc_equipment_b in B_RMD...miscellaneous_equipment:`
  - Get the corresponding miscellaneous equipment load in the proposed RMD: `misc_equipment_p = match_data_element(P_RMD, MiscellaneousEquipment, misc_equipment_b.id)`
  - Get the miscellaneous equipment power in the proposed RMD: `misc_equipment_power_p = misc_equipment_p.power`
  - Get the miscellaneous equipment power in the baseline RMD: `misc_equipment_power_b = misc_equipment_b.power`
  - If the miscellaneous equipment power in the baseline RMD does not match the miscellaneous equipment power in the proposed RMD: `if misc_equipment_power_b != misc_equipment_power_p:`
    - Append the miscellaneous equipment id to the list of mismatched miscellaneous equipment power: `mismatched_misc_equipment_power.append({"id": misc_equipment_b.id, "baseline_power": misc_equipment_power_b, "proposed_power": misc_equipment_power_p})`

**Rule Assertion:**  
  - Case 1: If the length of mismatched equipment power is 0: PASS `if len(mismatched_misc_equipment_power) == 0: PASS`
  - Case 2: Else: `FAIL`

**Notes/Questions:**
None

 **[Back](../_toc.md)**