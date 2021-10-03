
# Boiler - Rule 21-4  

**Rule ID:** 21-4  
**Rule Description:** When baseline building does not use purchased heat, baseline systems 1,5,7,11,12 shall be modeled with natural draft boilers.  
**Rule Assertion:** B-RMR  
**Appendix G Section:** Section 21 Boiler  
**Appendix G Section Reference:** Section G3.1.3.2 Building System-Specific Modeling Requirements for the Baseline model  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  

1. Baseline number of HW Loops > 0 and number of boilers in HW loop > 0.  

**Manual Check:** None  
**Evaluation Context:** Building  
**Data Lookup:** None  
**Function Call:** None  

## Rule Logic:  

- For each conditioning component in B_RMR: `for conditioning_component_b in B_RMR.ASHRAE229.conditioning_components:`

  - Check if conditioning component is boiler: `if conditioning_component_b IS Boiler:`

    - Check if boiler serves hot water loop: `if conditioning_component_b.loop.type == "HEATING":`

      - Set applicability flag: `rule_applicability_check = TRUE`

        **Rule Assertion:**

        - Case 1: For each boiler, if it is modeled as natural draft type: `if conditioning_component_b.draft_type == "NATURAL": PASS`

        - Case 2: Else: `else: FAIL`

**Applicability Check:**

1. Rule is applicable if B-RMR is modeled with at least one boiler: `if rule_applicability_check: is_applicable = TRUE`

**[Back](../_toc.md)**

**Notes:**

1. Do we need to check if baseline system is 1,5,7,11,12, or does this rule apply to all boilers in B-RMR?
2. Pending on how to get to external_fluid_source from conditioning_components.
