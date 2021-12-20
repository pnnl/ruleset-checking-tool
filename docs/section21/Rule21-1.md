
# Boiler - Rule 21-1  

**Rule ID:** 21-1  
**Rule Description:** For systems using purchased hot water or steam, the heating source shall be modeled as
purchased hot water or steam in both the proposed design and baseline building design. If any system in the proposed design uses purchased hot water or steam, all baseline systems with hot water coils shall use the same type of purchased hot water or steam.  
**Rule Assertion:** B-RMR = expected value  
**Appendix G Section:** Section 21 Boiler  
**Appendix G Section Reference:** Section G3.1.1.1 & G3.1.1.3.1 Building System-Specific Modeling Requirements for the Baseline model  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  

1. P-RMR is modeled with purchased hot water or steam
2. B-RMR is modeled with at least one air-side system that is Type-1, 5, 7, 11, or 12.

**Manual Check:** None  
**Evaluation Context:** Building  
**Data Lookup:** None  
**Function Call:** None  

**Applicability Check 1:**

1. Rule is applicable if B-RMR is modeled with at least one air-side system that is Type-1, 5, 7, 11, or 12: `PLACEHOLDER`

## Rule Logic:  

- For each external fluid source in P_RMR: `for external_fluid_source_p in P_RMR.ASHRAE229.external_fluid_source:`

  - Check if external fluid source in P_RMR is purchased hot water or steam: `if external_fluid_source_p.type in ["HOT_WATER", "STEAM]:`

    - Set applicability flag: `rule_applicability_check = TRUE`

**Rule Assertion:**

- Case 1: If P-RMR is modeled with purchased hot water or steam: `if rule_applicability_check: UNDETERMINED and raise_message "P-RMR IS MODELED WITH PURCHASED HOT WATER OR STEAM. VERIFY B-RMR HEATING SOURCE IS MODELED CORRECTLY."`

**Applicability Check 2:**

1. Rule is applicable if P-RMR is modeled with purchased hot water or steam: `if rule_applicability_check: is_applicable = TRUE`

**[Back](../_toc.md)**

**Notes:**

1. Do we need to check the utility rate (Hot-water or steam costs shall be based on actual utility rates)?
2. What if P-RMR is modeled with purchased hot water and steam, which source should be modeled in the baseline?
3. Can SHW also be served by purchased HHW or steam?
