# Section 1 - Rule 1-4
**Schema Version:** 0.0.36  
**Mandatory Rule:** True  
**Rule ID:** 1-4  
**Rule Description:** The PCI shall be less than or equal to the PCIt when calculated in accordance with Standard 90.1 2019, Section 4.2.1.1  
**Rule Assertion:** Options are Pass/Fail  
**Appendix G Section:** None  
**90.1 Section Reference:** 4.2.1.1  

**Data Lookup:** None  

**Evaluation Context:** RMD

**Applicability Checks:** None

**Function Calls:** None


## Rule Logic:
- Create a set of the PCI Target values from the various outputs (it only needs to exist in at least 1 output): `pci_target_set = set([B_0_RMD.output.performance_cost_index_target, B_90_RMD.output.performance_cost_index_target, B_180_RMD.output.performance_cost_index_target, B_270_RMD.output.performance_cost_index_target, P_RMD.output.performance_cost_index_target, U_RMD.output.performance_cost_index_target])`
- Create a set of the PCI values from the various outputs (it only needs to exist in at least 1 output): `pci_set = set([B_0_RMD.output.performance_cost_index, B_90_RMD.output.performance_cost_index, B_180_RMD.output.performance_cost_index, B_270_RMD.output.performance_cost_index, P_RMD.output.performance_cost_index, U_RMD.output.performance_cost_index])`
- If the length of the PCI Target set is not 1, raise a message and return FAIL: `if len(pci_target_set) != 1: outcome = FAIL and raise_message "Ruleset expects exactly one PCI Target value to be used in the project."`
- If the length of the PCI set is not 1, raise a message and return FAIL: `if len(pci_set) != 1: outcome = FAIL and raise_message "Ruleset expects exactly one PCI value to be used in the project."`

- Get the Performance Cost Index-Target from the output(s): `output_pci_target = pci_target_set[0]`
- Get the Performance Cost Index from the output(s): `output_pci = pci_set[0]`

**Rule Assertion**

- Case 1: If the PCI is less than or equal to the PCI target, PASS: `if output_pci <= output_pci_target: outcome = PASS`
- Case 2: Else, FAIL `else: outcome = FAIL`


**Notes/Questions:** None


**[Back](../_toc.md)**
