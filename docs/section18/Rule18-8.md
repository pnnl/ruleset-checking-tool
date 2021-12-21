
# CHW&CW - Rule 18-8  

**Rule ID:** 18-8  
**Rule Description:** For systems using purchased chilled water, the cooling source shall be modeled as purchased chilled water in both the proposed design and baseline building design. If any system in the proposed design uses purchased chilled water, all baseline systems with chilled water coils shall use purchased chilled water. On-site chillers and direct expansion equipment shall not be modeled in the baseline building design.  
**Rule Assertion:** B-RMR = expected value  
**Appendix G Section:** Section 22 CHW&CW Loop  
**Appendix G Section Reference:** Section G3.1.1.1 & G3.1.1.3.1 Building System-Specific Modeling Requirements for the Baseline model  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  

1. B-RMR is modeled with at least one air-side system that is Type-7, 8, 11, 12, or 13

**Manual Check:** None  
**Evaluation Context:** Building  
**Data Lookup:** None  
**Function Call:** None  

**Applicability Checks:**  

1. B-RMR is modeled with at least one air-side system that is Type-7, 8, 11, 12, or 13: `PLACEHOLDER`

## Rule Logic:  

- For each external fluid source in P_RMR: `for external_fluid_source_p in P_RMR.ASHRAE229.external_fluid_source:`

  - Check if external fluid source in P_RMR is purchased chilled water: `if external_fluid_source_p.type == "CHILLED_WATER":`

    - Set applicability flag: `rule_applicability_check = TRUE`

**Rule Assertion:**

- Case 1: If P-RMR is modeled with purchased chilled water: `if rule_applicability_check: UNDETERMINED and raise_message "P-RMR IS MODELED WITH PURCHASED CHILLED WATER. VERIFY B-RMR COOLING SOURCE IS MODELED CORRECTLY."`

**Applicability Check 2:**

1. Rule is applicable if P-RMR is modeled with purchased chilled water: `if rule_applicability_check: is_applicable = TRUE`

**[Back](../_toc.md)**
