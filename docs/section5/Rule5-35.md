
# Envelope - Rule 5-35  

**Rule ID:** 5-35  
**Rule Description:** The infiltration shall be modeled using the same methodology and adjustments for weather and building operation in both the proposed design and the baseline building design.  
**Rule Assertion:** For all zones, B-RMR infiltration:modeling_method_name = P-RMR infiltration:modeling_method_name and B-RMR infiltration:modeling_method = P-RMR infiltration:modeling_method.  
**Appendix G Section:** Section G3.1-5(b) Building Envelope Modeling Requirements for the Proposed design and Baseline  
**Appendix G Section Reference:** None  

**Applicability:** All required data elements exist for P_RMR  
**Applicability Checks:**  None  

**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  
**Function Call:** 

  1. match_data_element()

## Rule Logic:  

- For each building segment in the Proposed model: `for building_segment_p in P_RMR.building.building_segments:`  

    - For each zone in building segment: `for zone_p in building_segment_p.zones:`

      - Get zone infiltration: `infiltration_p = zone_p.infiltration`  

      - Get matching zone in B_RMR: `zone_b = match_data_element(B_RMR, Zones, zone_p.id)`

        - Get zone infiltration in B_RMR: `infiltration_b = zone_b.infiltration`

          **Rule Assertion:**  

          - Case 1: For each zone, if both zone infiltration modeling method name and modeling method in P_RMR match that in B_RMR: `if ( infiltration_p.modeling_method_name == infiltration_b.modeling_method_name ) AND ( infiltration_p.modeling_method == infiltration_b.modeling_method ): PASS`

          - Case 2: Else: `Else: FAIL`

**Notes:**

1. Update Rule ID from 5-46 to 5-35 on 10/26/2023

**[Back](../_toc.md)**
