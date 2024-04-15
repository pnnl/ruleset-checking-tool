# Section 1 - Rule 1-3
**Schema Version:** 0.0.36  
**Mandatory Rule:** True  
**Rule ID:** 1-3  
**Rule Description:** The Performance Cost Index-Target (PCIt) shall be calculated using the procedures defined in Section 4.2.1.1. The PCIt shall be equal to [baseline building unregulated energy cost (BBUEC) + BPF x baseline building regulated energy cost (BBREC)]/ BBP  
**Rule Assertion:** Options are Pass/Fail   
**Appendix G Section:** Section 4.2.1.1  
**90.1 Section Reference:** None  

**Data Lookup:** None  

**Evaluation Context:** 

**Applicability Checks:** 

**Function Calls:** None

## Rule Logic:   

- Create a set of the PCI Target values from the various outputs (it only needs to exist in at least 1 output): `pci_target_set = set([B_0_RMD.output.performance_cost_index_target, B_90_RMD.output.performance_cost_index_target, B_180_RMD.output.performance_cost_index_target, B_270_RMD.output.performance_cost_index_target, P_RMD.output.performance_cost_index_target, U_RMD.output.performance_cost_index_target])`


- Create a set of the project area weighted average building performance factor (BPF) from the various outputs (it only needs to exist in at least 1 output): `bpf_set = set([B_0_RMD.output.total_area_weighted_building_performance_factor, B_90_RMD.output.total_area_weighted_building_performance_factor, B_180_RMD.output.total_area_weighted_building_performance_factor, B_270_RMD.output.total_area_weighted_building_performance_factor, P_RMD.output.total_area_weighted_building_performance_factor, U_RMD.output.total_area_weighted_building_performance_factor])`


- Create a set of the baseline building performance (BBP) from the various outputs (it only needs to exist in at least 1 output): `bbp_set = set([B_0_RMD.output.baseline_building_performance_energy_cost, B_90_RMD.output.baseline_building_performance_energy_cost, B_180_RMD.output.baseline_building_performance_energy_cost, B_270_RMD.output.baseline_building_performance_energy_cost, P_RMD.output.baseline_building_performance_energy_cost, U_RMD.output.baseline_building_performance_energy_cost])`


- Create a set of the baseline building regulated energy cost (BBREC) from the various outputs (it only needs to exist in at least 1 output): `bbrec_set = set([B_0_RMD.output.baseline_building_regulated_energy_cost, B_90_RMD.output.baseline_building_regulated_energy_cost, B_180_RMD.output.baseline_building_regulated_energy_cost, B_270_RMD.output.baseline_building_regulated_energy_cost, P_RMD.output.baseline_building_regulated_energy_cost, U_RMD.output.baseline_building_regulated_energy_cost])`


- Create a set of the baseline building unregulated energy cost (BBUEC) from the various outputs (it only needs to exist in at least 1 output): `bbuec_set = set([B_0_RMD.output.baseline_building_unregulated_energy_cost, B_90_RMD.output.baseline_building_unregulated_energy_cost, B_180_RMD.output.baseline_building_unregulated_energy_cost, B_270_RMD.output.baseline_building_unregulated_energy_cost, P_RMD.output.baseline_building_unregulated_energy_cost, U_RMD.output.baseline_building_unregulated_energy_cost])`


- If the length of the PCI Target set is not 1, raise a message and return FAIL: `if len(pci_target_set) != 1: outcome = FAIL and raise_message "Ruleset expects exactly one PCI Target value to be used in the project."`
- If the length of the BPF set is not 1, raise a message and return FAIL: `if len(bpf_set) != 1: outcome = FAIL and raise_message "Ruleset expects exactly one BPF value to be used in the project."`
- If the length of the BBP set is not 1, raise a message and return FAIL: `if len(bbp_set) != 1: outcome = FAIL and raise_message "Ruleset expects exactly one BBP value to be used in the project."`
- If the length of the BBREC set is not 1, raise a message and return FAIL: `if len(bbrec_set) != 1: outcome = FAIL and raise_message "Ruleset expects exactly one BBREC value to be used in the project."`
- If the length of the BBUEC set is not 1, raise a message and return FAIL: `if len(bbuec_set) != 1: outcome = FAIL and raise_message "Ruleset expects exactly one BBUEC value to be used in the project."`


- Get the Performance Cost Index-Target from the output(s): `output_pci_target = pci_target_set[0]`
- Get the project area weighted average building performance factor (BPF) from the output(s): `output_bpf = bpf_set[0]`
- Get the baseline building performance (BBP) from the output(s): `output_bbp = bbp_set[0]`
- Get the baseline building regulated energy cost (BBREC) from the output(s): `output_bbrec = bbrec_set[0]`
- Get the baseline building unregulated energy cost (BBUEC) from the output(s): `output_bbuec = bbuec_set[0]`

- If the output_bbp value is 0, raise a message and return FAIL: `if output_bbp == 0: outcome = FAIL and raise_message "Ruleset expects baseline_building_performance_energy_cost to be greater than 0."`

  **Rule Assertion:** 
  - If PCIt = (BBUEC + (BPF * BBREC)) / BBP: PASS `if output_bbp !=0 and output_pci_target == (output_bbuec + (output_bpf * output_bbrec))/output_bbp: outcome = PASS`
  - Else: FAIL `else: outcome = FAIL`

**Notes/Questions:** None


**[Back](../_toc.md)**