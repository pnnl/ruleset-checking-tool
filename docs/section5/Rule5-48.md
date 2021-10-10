
# Envelope - Rule 5-48  

**Rule ID:** 5-48  
**Rule Description:** The air leakage rate in unconditioned and unenclosed spaces must be the same the baseline and proposed design.  
**Rule Assertion:** B-RMR infiltration:air_leakage_rate = P-RMR infiltration:air_leakage_rate  
**Appendix G Section:** Section 5 Envelope  
**Appendix G Section Reference:** Section G3.1-1 Building Envelope Modeling Requirements for the Proposed design and Baseline building  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  None  

**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  
**Function Call:** 

  1. match_data_element()
  2. get_zone_conditioning_category()

## Rule Logic:  

- Get zone conditioning category for B_RMR: `zcc_b = get_zone_conditioning_category(B_RMR)`

- Get measured infiltration pressure difference: `measured_infiltration_pressure_difference_b = ASHRAE229.measured_infiltration_pressure_difference`

  - Check if measured infiltration pressure difference is at wind pressure: `if measured_infiltration_pressure_difference_b == "NO_TEST_PERFORMED":`

    - For each zone in B_RMR: `for zone_b in B_RMR...zones:`

      - Check if zone is unconditioned or unenclosed: `if zcc_b[zone_b.id] in ["UNENCLOSED", "UNCONDITIONED"]:`

        - Get zone infiltration: `infiltration_b = zone_b.infiltration`

        - Get matching zone in P_RMR: `zone_p = match_data_element(P_RMR, Zones, zone_b.id)`

          - Get zone infiltration in P_RMR: `infiltration_p = zone_p.infiltration`

            **Rule Assertion:**  

            - Case 1: For each unconditioned and unenclosed zone, if zone infiltration air leakage rate in B_RMR matches that in P_RMR: `if infiltration_b.measured_air_leakage_rate == infiltration_p.measured_air_leakage_rate: PASS`  

            - Case 2: Else: `Else: FAIL`

**[Back](../_toc.md)**
