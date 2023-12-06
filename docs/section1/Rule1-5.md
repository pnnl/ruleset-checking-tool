# Section 1 - Rule 1-5
**Schema Version:** 0.0.29  
**Mandatory Rule:** True  
**Rule ID:** 1-5
**Rule Description:** When on-site renewable energy generation exceeds the thresholds defined in Section 4.2.1.1, the methodology defined in this section shall be used to calculate the PCIt.
**Rule Assertion:** Options are Pass/Fail/NOT_APPLICABLE     
**Appendix G Section:** None
**90.1 Section Reference:** Section 4.2.1.1  

**Data Lookup:** None 

**Evaluation Context:** RMD

**Applicability Checks:** 
1. Applies to projects where the proposed on site renewable energy production offsets more than 5% of the baseline building performance cost

**Function Calls:**


## Rule Logic:
- Get the proposed building performance (PBP) from the output of the proposed model: `output_pbp = P_RMD.output.total_proposed_building_energy_cost_including_renewable_energy`
- Get the baseline building performance (BBP) from the output of the proposed model: `output_bbp = P_RMD.output.baseline_building_performance_energy_cost`
- Get the proposed building performance without any credit for on-site renewable energy generation systems: `output_pbp_nre = P_RMD.output.total_proposed_building_energy_cost_excluding_renewable_energy`
- Get the Performance Cost Index (PCI) from the output of the proposed model: `output_pci = P_RMD.output.performance_cost_index`
- Get the Performance Cost Index-Target (PCIt) from the output of the proposed model: `output_pci_target = P_RMD.output.performance_cost_index_target`
**Applicability Check 1:** If the proposed on site renewable energy production offsets less than or equal to 5% of the baseline building performance: NOT_APPLICABLE ` if (output_pbp_nre - output_pbp)/output_bbp <= 0.05: NOT_APPLICABLE`
- Else, continue to rule assertion: `else:`

  **Rule Assertion:** 
  - If PCI + ((PBPnre - PBP)/BBP) - 0.05 <= PCIt: PASS `if output_pci + ((output_pbp_nre - output_pbp)/output_bbp) - 0.05 <= output_pci_target: outcome = PASS`
  - Else: FAIL `else: outcome = FAIL`


**Notes/Questions:** None


**[Back](../_toc.md)**