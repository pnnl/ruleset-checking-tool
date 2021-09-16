
# Envelope - Rule 5-48  

**Rule ID:** 5-48  
**Rule Description:** The air leakage rate must be the same in the baseline and proposed design.  
**Rule Assertion:** B-RMR infiltration:air_leakage_rate = P-RMR infiltration:air_leakage_rate  
**Appendix G Section:** Section G3.1-1 Building Envelope Modeling Requirements for the Proposed design and Baseline building  
**Appendix G Section Reference:** None  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  None  

**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  
**Function Call:** 

  1. match_data_element()

## Rule Logic:  

- For each building segment in the B_RMR: `for building_segment_b in B_RMR.building.building_segments:`

  - For each thermal block in building segment: `for thermal_block_b in building_segment_b.thermal_blocks:`

    - For each zone in thermal block: `for zone_b in thermal_block_b.zones:`

      - Get zone infiltration: `infiltration_b = zone_b.infiltration`

      - Get matching zone in P_RMR: `zone_p = match_data_element(P_RMR, Zones, zone_b.id)`

        - Get zone infiltration in P_RMR: `infiltration_p = zone_p.infiltration`

          **Rule Assertion:**  

          - Case 1: For each unconditioned and unenclosed zone, if zone infiltration air leakage rate in B_RMR matches that in P_RMR: `if infiltration_b.air_leakage_rate == infiltration_p.air_leakage_rate: PASS`  

          - Case 2: Else: `Else: FAIL`

**[Back](../_toc.md)**
