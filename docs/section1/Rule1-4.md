# Section 1 - Rule 1-4
**Schema Version:** 0.0.29  
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
- Get the Performance Cost Index-Target from the output of the proposed model: `output_pci_target = P_RMD.output.performance_cost_index_target`
- Get the Performance Cost Index from the output of the proposed model: `output_pci = P_RMD.output.performance_cost_index`
**Rule Assertion**
- Case 1: If the PCI is less than or equal to the PCI target, PASS: `if output_pci <= output_pci_target: outcome = PASS`
- Case 2: Else, FAIL `else: outcome = FAIL`


**Notes/Questions:** None


**[Back](../_toc.md)**