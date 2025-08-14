# Section 1 - Rule 1-5  
**Schema Version:** 0.0.36  
**Mandatory Rule:** True  
**Rule ID:** 1-5  
**Rule Description:** When on-site renewable energy generation exceeds the thresholds defined in Section 4.2.1.1, the methodology defined in this section shall be used to calculate the PCI.  
**Rule Assertion:** Options are Pass/Fail/NOT_APPLICABLE     
**Appendix G Section:** None  
**90.1 Section Reference:** Section 4.2.1.1  

**Data Lookup:** None 

**Evaluation Context:** RMD

**Applicability Checks:** 
1. Applies to projects where the proposed on site renewable energy production offsets more than 5% of the baseline building performance cost

**Function Calls:**


## Rule Logic:
- Create a set of the PBP values from the various outputs (it only needs to exist in at least 1 output): `pbp_set = set([B_0_RMD.output.total_proposed_building_energy_cost_including_renewable_energy, B_90_RMD.output.total_proposed_building_energy_cost_including_renewable_energy, B_180_RMD.output.total_proposed_building_energy_cost_including_renewable_energy, B_270_RMD.output.total_proposed_building_energy_cost_including_renewable_energy, P_RMD.output.total_proposed_building_energy_cost_including_renewable_energy, U_RMD.output.total_proposed_building_energy_cost_including_renewable_energy])`
- Create a set of the BBP values from the various outputs (it only needs to exist in at least 1 output): `bbp_set = set([B_0_RMD.output.baseline_building_performance_energy_cost, B_90_RMD.output.baseline_building_performance_energy_cost, B_180_RMD.output.baseline_building_performance_energy_cost, B_270_RMD.output.baseline_building_performance_energy_cost, P_RMD.output.baseline_building_performance_energy_cost, U_RMD.output.baseline_building_performance_energy_cost])`
- Create a set of the PBP_nre values from the various outputs (it only needs to exist in at least 1 output): `pbp_nre_set = set([B_0_RMD.output.total_proposed_building_energy_cost_excluding_renewable_energy, B_90_RMD.output.total_proposed_building_energy_cost_excluding_renewable_energy, B_180_RMD.output.total_proposed_building_energy_cost_excluding_renewable_energy, B_270_RMD.output.total_proposed_building_energy_cost_excluding_renewable_energy, P_RMD.output.total_proposed_building_energy_cost_excluding_renewable_energy, U_RMD.output.total_proposed_building_energy_cost_excluding_renewable_energy])`
- Create a set of the PCI values from the various outputs (it only needs to exist in at least 1 output): `pci_set = set([B_0_RMD.output.performance_cost_index, B_90_RMD.output.performance_cost_index, B_180_RMD.output.performance_cost_index, B_270_RMD.output.performance_cost_index, P_RMD.output.performance_cost_index, U_RMD.output.performance_cost_index])`
- Create a set of the PCI Target values from the various outputs (it only needs to exist in at least 1 output): `pci_target_set = set([B_0_RMD.output.performance_cost_index_target, B_90_RMD.output.performance_cost_index_target, B_180_RMD.output.performance_cost_index_target, B_270_RMD.output.performance_cost_index_target, P_RMD.output.performance_cost_index_target, U_RMD.output.performance_cost_index_target])`


- If the length of the PBP set is not 1, raise a message and return FAIL: `if len(pbp_set) != 1: outcome=FAIL and raise_message "Ruleset expects exactly one PBP value to be used in the project."`
- If the length of the BBP set is not 1, raise a message and return FAIL: `if len(bbp_set) != 1: outcome=FAIL and raise_message "Ruleset expects exactly one BBP value to be used in the project."`
- If the length of the PBP_nre set is not 1, raise a message and return FAIL: `if len(pbp_nre_set) != 1: outcome=FAIL and raise_message "Ruleset expects exactly one PBP_nre value to be used in the project."`
- If the length of the PCI set is not 1, raise a message and return FAIL: `if len(pci_set) != 1: outcome=FAIL and raise_message "Ruleset expects exactly one PCI value to be used in the project."`
- If the length of the PCI Target set is not 1, raise a message and return FAIL: `if len(pci_target_set) != 1: outcome=FAIL and raise_message "Ruleset expects exactly one PCI Target value to be used in the project."`

- Get the proposed building performance (PBP) from the output(s): `output_pbp = pbp_set[0]`
- Get the baseline building performance (BBP) from the output(s): `output_bbp = bbp_set[0]`
- Get the proposed building performance without any credit for on-site renewable energy generation systems from the output(s): `output_pbp_nre = pbp_nre_set[0]`
- Get the Performance Cost Index (PCI) from the output(s): `output_pci = pci_set[0]`
- Get the Performance Cost Index-Target (PCIt) from the output(s): `output_pci_target = pci_target_set[0]`  

- If the output_bbp value is 0, raise a message and return FAIL: `if output_bbp == 0: outcome = FAIL and raise_message "Ruleset expects baseline_building_performance_energy_cost to be greater than 0."`

**Applicability Check 1:**  

- If the proposed on site renewable energy production offsets less than or equal to 5% of the baseline building performance: NOT_APPLICABLE ` if (output_pbp_nre - output_pbp)/output_bbp <= 0.05: NOT_APPLICABLE`
- Else, continue to rule assertion: `else:`

**Rule Assertion:**  

  - Case 1: If output_bbp != 0 and PCI + ((PBPnre - PBP)/BBP) - 0.05 <= PCIt, PASS `if output_bbp != 0 and output_pci + ((output_pbp_nre - output_pbp)/output_bbp) - 0.05 <= output_pci_target: outcome = PASS`
  - Case 2: Else, FAIL `else: outcome = FAIL`


**Notes/Questions:** None


**[Back](../_toc.md)**
