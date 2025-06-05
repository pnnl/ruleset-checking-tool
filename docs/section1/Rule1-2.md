# Section 1 - Rule 1-2
**Schema Version:** 0.0.36  
**Mandatory Rule:** True  
**Rule ID:** 1-2  
**Rule Description:** The performance of the proposed design is calculated in accordance with Standard 90.1-2019 Appendix G, where Performance Cost Index = Proposed building performance (PBP) /Baseline building performance (BBP), where both the PBP and the BBP include all end-use load components associated with the building when calculating the Performance Cost Index (PCI).  
**Rule Assertion:** Options are Pass/Fail/NOT_APPLICABLE  
**Appendix G Section:** G1.2.2  
**90.1 Section Reference:** None  

**Data Lookup:** None  

**Evaluation Context:** RMD  

**Applicability Checks:** None  

**Function Calls:** None  

## Rule Logic:   
- Create a set of the PCI values from the various outputs (it only needs to exist in at least 1 output): `pci_set = set([B_0_RMD.output.performance_cost_index, B_90_RMD.output.performance_cost_index, B_180_RMD.output.performance_cost_index, B_270_RMD.output.performance_cost_index, P_RMD.output.performance_cost_index, U_RMD.output.performance_cost_index])`


- Create a set of the PBP values from the various outputs (it only needs to exist in at least 1 output): `pbp_set = set([B_0_RMD.output.total_proposed_building_energy_cost_including_renewable_energy, B_90_RMD.output.total_proposed_building_energy_cost_including_renewable_energy, B_180_RMD.output.total_proposed_building_energy_cost_including_renewable_energy, B_270_RMD.output.total_proposed_building_energy_cost_including_renewable_energy, P_RMD.output.total_proposed_building_energy_cost_including_renewable_energy, U_RMD.output.total_proposed_building_energy_cost_including_renewable_energy])`


- Create a set of the BBP values from the various outputs (it only needs to exist in at least 1 output): `bbp_set = set([B_0_RMD.output.baseline_building_performance_energy_cost, B_90_RMD.output.baseline_building_performance_energy_cost, B_180_RMD.output.baseline_building_performance_energy_cost, B_270_RMD.output.baseline_building_performance_energy_cost, P_RMD.output.baseline_building_performance_energy_cost, U_RMD.output.baseline_building_performance_energy_cost])`


- If the length of the PCI set is not 1, raise a message and return FAIL: `if len(pci_set) != 1: outcome = FAIL and raise_message "Ruleset expects exactly one PCI value to be used in the project."`
- If the length of the PBP set is not 1, raise a message and return FAIL: `if len(pbp_set) != 1: outcome = FAIL and raise_message "Ruleset expects exactly one PBP value to be used in the project."`
- If the length of the BBP set is not 1, raise a message and return FAIL: `if len(bbp_set) != 1: outcome = FAIL and raise_message "Ruleset expects exactly one BBP value to be used in the project."`


- Get the Performance Cost Index: `output_pci = pci_set[0]`
- Get the proposed building performance (PBP): `output_pbp = pbp_set[0]`
- Get the baseline building performance (BBP): `output_bbp = bbp_set[0]`

- If the output_bbp value is 0, raise a message and return FAIL: `if output_bbp == 0: outcome = FAIL and raise_message "Ruleset expects baseline_building_performance_energy_cost to be greater than 0."`

  **Rule Assertion:** 

  - Case 1: If PCI = PBP / BBP: PASS `if output_bbp != 0 and output_pci == output_pbp / output_bbp: outcome = PASS`
  - Case 2: Else: FAIL `else: outcome = FAIL`

**[Back](../_toc.md)**
