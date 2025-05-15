# Receptacles – Rule 12-1   
**Schema Version:** 0.0.37        
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
- Determine the project's compliance path, if available: `compliance_path = RPD.get("compliance_path")`
- Store a list of any miscellaneous equipment power where proposed is greater than baseline: `unexpected_misc_equipment_power = []`
- Store a list of any miscellaneous equipment power where proposed is less than baseline: `reduced_misc_equipment_power = []`
- For each miscellaneous equipment load in the baseline RMD: `for misc_equipment_b in B_RMD...miscellaneous_equipment:`
  - Get the corresponding miscellaneous equipment load in the proposed RMD: `misc_equipment_p = match_data_element(P_RMD, MiscellaneousEquipment, misc_equipment_b.id)`
  - Get the miscellaneous equipment power in the proposed RMD: `misc_equipment_power_p = misc_equipment_p.power`
  - Get the miscellaneous equipment power in the baseline RMD: `misc_equipment_power_b = misc_equipment_b.power`
  - If the miscellaneous equipment power in the baseline RMD is greater than the miscellaneous equipment power in the proposed RMD: `if misc_equipment_power_b > misc_equipment_power_p:`
    - Append the miscellaneous equipment info for reporting: `reduced_misc_equipment_power.append({"id": misc_equipment_b.id, "baseline_power": misc_equipment_power_b, "proposed_power": misc_equipment_power_p})`
  - If the miscellaneous equipment power in the baseline RMD is less than the miscellaneous equipment power in the proposed RMD: `elif misc_equipment_power_b < misc_equipment_power_p:`
    - Append the miscellaneous equipment info for reporting: `unexpected_misc_equipment_power.append({"id": misc_equipment_b.id, "baseline_power": misc_equipment_power_b, "proposed_power": misc_equipment_power_p})`
**Rule Assertion:**  
  - Case 1: If all equipment power was modeled identically: PASS `if len(unexpected_misc_equipment_power) == 0 and len(reduced_misc_equipment_power) == 0: PASS`
  - Case 2: Else if any equipment power is reduced in the proposed and the compliance path is not "CODE_COMPLIANT" (includes when compliance path is not specified): UNDETERMINED: `elif len(unexpected_misc_equipment_power) == 0 and compliance_path != "CODE_COMPLIANT": UNDETERMINED and raise_message="The proposed building miscellaneous equipment load is less than the baseline, which is only permitted when the model is being used to quantify performance that exceeds the requirements of Standard 90.1."`
  - Case 3: Else, proposed equipment power is greater than the baseline, or the compliance path is code-compliant and proposed equipment power is less than the baseline: `else: FAIL`

**Notes/Questions:**
None

 **[Back](../_toc.md)**