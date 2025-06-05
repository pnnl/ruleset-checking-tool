
# Envelope - Rule 5-36  

**Rule ID:** 5-36  
**Rule Description:** The air leakage rate in unconditioned and unenclosed spaces must be the same the baseline and proposed design.  
**Rule Assertion:** B-RMD infiltration:air_leakage_rate = P-RMR infiltration:air_leakage_rate  
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

- For each zone in B_RMR: `for zone_b in B_RMR...zones:`

  - Check if zone is unconditioned or unenclosed: `if zcc_b[zone_b.id] in ["UNENCLOSED", "UNCONDITIONED"]:`

    - Get zone infiltration: `infiltration_b = zone_b.infiltration`

    - Get matching zone in P_RMR: `zone_p = match_data_element(P_RMR, Zones, zone_b.id)`

      - Get zone infiltration in P_RMR: `infiltration_p = zone_p.infiltration`

        **Rule Assertion:**  

        - Case 1: For each unconditioned and unenclosed zone, if zone infiltration flow rate in B_RMR matches that in P_RMR: `if infiltration_b.infiltration_flow_rate == infiltration_p.infiltration_flow_rate: PASS`  

        - Case 2: Else: `Else: FAIL`

**Notes:**

1. Update Rule ID from 5-48 to 5-37 on 10/26/2023
2. Update Rule ID from 5-37 to 5-36 on 12/22/2023

**[Back](../_toc.md)**
