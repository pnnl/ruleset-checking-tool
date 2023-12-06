# Section 1 - Rule 1-3
**Schema Version:** 0.0.29  
**Mandatory Rule:** True  
**Rule ID:** 1-3
**Rule Description:** The Performance Cost Index-Target (PCIt) shall be calculated using the procedures defined in Section 4.2.1.1. The PCIt shall be equal to baseline building unregulated energy cost (BBUEC) + BPF x baseline building regulated energy cost (BBREC)/ BBP
**Rule Assertion:** Options are Pass/Fail   
**Appendix G Section:** Section 4.2.1.1  
**90.1 Section Reference:** None  

**Data Lookup:** None  

**Evaluation Context:** 

**Applicability Checks:** 

**Function Calls:** None

## Rule Logic:   

- Get the Performance Cost Index-Target from the output of the proposed model: `output_pci_target = P_RMD.output.performance_cost_index_target`
- Get the project area weighted average building performance factor (BPF) from the output of the proposed model: `output_bpf = P_RMD.output.total_area_weighted_building_performance_factor`
- Get the baseline building performance (BBP) from the output of the proposed model: `output_bbp = P_RMD.output.baseline_building_performance_energy_cost`
- Get the baseline building regulated energy cost (BBREC): `output_bbrec = P_RMD.output.baseline_building_regulated_energy_cost`
- Get the baseline building unregulated energy cost (BBUEC): `output_bbuec = P_RMD.output.baseline_building_unregulated_energy_cost`

  **Rule Assertion:** 
  - If PCIt = (BBUEC + (BPF * BBREC)) / BBP: PASS `if output_pci_target == (output_bbuec + (output_bpf * output_bbrec))/output_bbp: outcome = PASS`
  - Else: FAIL `else: outcome = FAIL`

**Notes/Questions:** None


**[Back](../_toc.md)**