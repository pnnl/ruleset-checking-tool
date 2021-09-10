
# Envelope - Rule 5-48  

**Rule ID:** 5-48  
**Rule Description:** The air leakage rate, schedule and method in unconditioned and unenclosed spaces must be the same in the baseline and proposed design.  
**Rule Assertion:** B-RMR infiltration:infiltration.air_leakage_rate, modeling_method, modeling_method_name, multiplier_Schedule= P-RMR infiltration.air_leakage_rate, modeling_method, modeling_method_name, multiplier_Schedule  
**Appendix G Section:** Section G3.1-1 Building Envelope Modeling Requirements for the Proposed design and Baseline building  
**Appendix G Section Reference:** None  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  None  

**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  
**Function Call:** 

  1. get_zone_conditioning_category()
  2. match_data_element()

## Rule Logic:  

- Get zone conditioning category for B_RMR: `zcc_b = get_zone_conditioning_category(B_RMR)`

- Get zone conditioning category for P_RMR: `zcc_p = get_zone_conditioning_category(P_RMR)`

- For each building segment in the B_RMR: `for building_segment_b in B_RMR.building.building_segments:`

  - For each thermal block in building segment: `for thermal_block_b in building_segment_b.thermal_blocks:`

    - For each zone in thermal block: `for zone_b in thermal_block_b.zones:`

      - Check if zone is unconditioned or unenclosed: `if zcc_b[zone_b] in ["UNENCLOSED", "UNCONDITIONED"]:`

        - Get zone infiltration: `infiltration_b = zone_b.infiltration`

        - Get matching zone in P_RMR: `zone_p = match_data_element(P_RMR, Zones, zone_b.id)`

          - Get zone infiltration in P_RMR: `infiltration_p = zone_p.infiltration`

            **Rule Assertion:**  

            - Case 1: For each unconditioned and unenclosed zone, if zone infiltration air leakage rate, schedule and method in B_RMR matches that in P_RMR: `if ( infiltration_b.air_leakage_rate == infiltration_p.air_leakage_rate ) AND ( infiltration_b.modeling_method == infiltration_p.modeling_method ) AND ( infiltration_b.multiplier_schedule == infiltration_p.multiplier_schedule ): PASS`  

            - Case 2: Else: `Else: FAIL`

**[Back](../_toc.md)**

**Notes:**

1. Do we need to exclude unconditioned and unenclosed zone in 5-45 and 5-46? They are checking schedule and method for all zones.
