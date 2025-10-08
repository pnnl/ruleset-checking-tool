# Receptacle - Rule 12-5
**Schema Version** 0.1.7  
**Primary Rule:** True  
**Rule ID:** 12-5  
**Rule Description:** These loads shall always be included in simulations of the building. These loads shall be included when calculating the proposed building performance and the baseline building performance as required by Section G1.2.1.   
**Appendix G Section:** Table G3.1-12 Proposed Building Performance column  
**Appendix G Section Reference:** None  

**Applicability:** This rule applies to all proposed models.
**Applicability Checks:**
1. Always applicable  

**Manual Check:** None  
**Evaluation Context:** P_RMD    
**Data Lookup:** None  
**Function Call:**
1. get_schedule_multiplier_hourly_value_or_default


## Rule Logic:  
- Iterate through the miscellaneous equipment data groups in the proposed model: `for misc_equipment_p in P_RMD...miscellaneous_equipment:` 
  - Get the equivalent full load hours (EFLH) for the assigned schedule: `schedule_eflh = sum(get_schedule_multiplier_hourly_value_or_default(P_RMD, misc_equipment_p["multiplier_schedule"], 0))`
  - Determine if the miscellaneous equipment power is greater than 0 and has either sensible or latent fractions greater than 0, and the assigned schedule has more than 0 EFLH then the loads are included in the building: `loads_included = misc_equipment_p.power > 0 and (misc_equipment_p.sensible_fraction > 0 or misc_equipment_p.latent_fraction > 0) and schedule_eflh > 0`
  - End iteration early if a load is included: `if loads_included: break`
- Iterate through the proposed output instance end use results: 
  - Determine if the proposed output instance has an end use result with type MISC_EQUIPMENT, INDUSTRIAL_PROCESS, OFFICE_EQUIPMENT, COMPUTER_SERVERS, or COMMERCIAL_COOKING and greater than 0 annual site energy use: `has_annual_energy_use = any(result for result in P_RMD.model_output.annual_end_use_results if result.type in ["MISC_EQUIPMENT", "INDUSTRIAL_PROCESS", "OFFICE_EQUIPMENT", "COMPUTER_SERVERS", "COMMERCIAL_COOKING"] and result.annual_site_energy_use > 0)`
  - End iteration early if a matching end use result is found: `if has_annual_energy_use: break`

  - **Rule Assertion:**  
      - Case 1: If the proposed model has miscellaneous equipment loads and end use results: PASS `if loads_included and has_annual_energy_use:` PASS`
      - Case 2: Else: FAIL and let the user know which part(s) caused the failure: `else: outcome = FAIL and raise_message(f"{'No miscellaneous equipment loads are included. [power: ' + f'{misc_equipment_p.power}, sensible_fraction: {misc_equipment_p.sensible_fraction}, latent_fraction: {misc_equipment_p.latent_fraction}, schedule_eflh: {schedule_eflh}] ' if not loads_included else ''}{'No annual end use energy is reported for the relevant equipment types.' if not has_annual_energy_use else ''}")"`


**Notes:**  
1. Agree on the MiscellaneousEquipment types that are included? MISC_EQUIPMENT, INDUSTRIAL_PROCESS, OFFICE_EQUIPMENT, COMPUTER_SERVERS, or COMMERCIAL_COOKING

- **[Back](../_toc.md)**
