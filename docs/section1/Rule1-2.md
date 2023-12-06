# Section 1 - Rule 1-2
**Schema Version:** 0.0.29  
**Mandatory Rule:** True  
**Rule ID:** 1-2  
**Rule Description:** The performance of the proposed design is calculated in accordance with Standard 90.1-2019 Appendix G, where Performance Cost Index = Proposed building performance (PBP) /Baseline building performance (BBP), where both the PBP and the BBP include all end-use load components associated with the building when calculating the Performance Cost Index (PCI).
**Rule Assertion:** Options are Pass/Fail   
**Appendix G Section:** None
**90.1 Section Reference:** G1.2.2

**Data Lookup:** None

**Evaluation Context:** RPD

**Applicability Checks:** 
1. Applies to projects where the proposed on site renewable energy production offsets less than or equal to 5% of the baseline building performance

**Function Calls:** None

## Rule Logic:   

- Get the Performance Cost Index from the output of the proposed model: `output_pci = P_RMD.output.performance_cost_index`
- Get the proposed building performance (PBP) from the output of the proposed model: `output_pbp = P_RMD.output.total_proposed_building_energy_cost_including_renewable_energy`
- Get the baseline building performance (BBP) from the output of the proposed model: `output_bbp = P_RMD.output.baseline_building_performance_energy_cost`
- Get the proposed building performance without any credit for on-site renewable energy generation systems: `output_pbp_nre = P_RMD.output.total_proposed_building_energy_cost_excluding_renewable_energy`
**Applicability Check 1:** If the proposed on site renewable energy production offsets more than 5% of the baseline building performance: NOT_APPLICABLE ` if (output_pbp_nre - output_pbp)/output_bbp > 0.05: NOT_APPLICABLE`
- Else, continue to rule assertion: `else:`

  **Rule Assertion:** 
  - If PCI = PBP / BBP: PASS `if output_pci == output_pbp / output_bbp: outcome = PASS`
  - Else: FAIL `else: outcome = FAIL`

**[Back](../_toc.md)**