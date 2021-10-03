
# Boiler - Rule 21-1  

**Rule ID:** 21-1  
**Rule Description:** For systems using purchased hot water or steam, the heating source shall be modeled as purchased hot water or steam in both the proposed design and baseline building design. Hot-water or steam costs shall be based on actual utility rates.  
**Rule Assertion:** B-RMR ASHRAE229:conditioning_component(external_fluid_source).type = P-RMR ASHRAE229:conditioning_component(external_fluid_source).type  
**Appendix G Section:** Section 21 Boiler  
**Appendix G Section Reference:** Section G3.1.1.1 & G3.1.1.3.1 Building System-Specific Modeling Requirements for the Baseline model  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  

1. P-RMR is modeled with purchased hot water or steam

**Manual Check:** None  
**Evaluation Context:** Building  
**Data Lookup:** None  
**Function Call:** None  

## Rule Logic:  

- For each conditioning component in P_RMR: `for conditioning_component_p in P_RMR.ASHRAE229.conditioning_components:`

  - Check if conditioning component in P_RMR is purchased hot water or steam: `if ( conditioning_component_p IS ExternalFluidSource ) AND ( conditioning_component_p.type in ["HOT_WATER", "STEAM] ):`

    - Set applicability flag: `rule_applicability_check = TRUE`

    - Get matching external fluid source from B_RMR: `external_fluid_source_b = match_data_element(B_RMR, ExternalFluidSources, conditioning_component_p.id)`

      **Rule Assertion:**

      - Case 1: For each external fluid source that is purchased hot water or steam in P-RMR, if source type in B-RMR matches that in P-RMR: `if external_fluid_source_b.type == conditioning_component_p.type: PASS`

      - Case 2: Else: `else: FAIL`

**Applicability Check:**

1. Rule is applicable if P-RMR is modeled with purchased hot water or steam: `if rule_applicability_check: is_applicable = TRUE`

**[Back](../_toc.md)**

**Notes:**

1. Pending on how to get to external_fluid_source from conditioning_components.
2. Do we need to check the utility rate (Hot-water or steam costs shall be based on actual utility rates)?
