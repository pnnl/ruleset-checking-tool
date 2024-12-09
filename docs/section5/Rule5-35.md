
# Envelope - Rule 5-35  

**Rule ID:** 5-35  
**Rule Description:** The baseline air leakage rate of the building envelope (I75Pa) at a fixed building pressure differential of 0.3 in. of water shall be 1 cfm/ft2.  The air leakage rate of the building envelope shall be converted to appropriate units for the simulation program using one of the methods in Section G3.1.1.4.  
**Rule Assertion:** Sum of B-RMD infiltration.infiltration.air_leakage_rate = expected value.  
**Appendix G Section:** Section 5 Envelope  
**Appendix G Section Reference:** Section G3.1-5(h) Building Envelope Modeling Requirements for the Baseline building  

**Applicability:** All required data elements exist for B_RMD  
**Applicability Checks:**  None  

**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  
**Function Call:** 

  1. get_surface_conditioning_category()
  2. get_zone_conditioning_category()

## Rule Logic:  

- Get surface conditioning category dictionary for B_RMD: `scc_dict_b = get_surface_conditioning_category(B_RMD)`

- Get zone conditioning category dictionary for B_RMD: `zone_conditioning_category_dict_b = get_zone_conditioning_category(B_RMD)`

- For each zone in the Baseline model: `for zone_b in B_RMD...zones:`

  - For each surface in zone: `for surface_b in zone_b.surfaces:`

    - Check if surface is regulated, add zone total area of building envelope to building total: `if scc_dict_b[surface_b.id] != "UNREGULATED": building_total_envelope_area += sum(surface.area for surface in zone_b.surfaces)`

  - Check if zone is conditioned or semi-heated, add zone infiltration flow rate to building total: `if zone_conditioning_category_dict_b[zone.id] in [CONDITIONED RESIDENTIAL, CONDITIONED NON-RESIDENTIAL, CONDITIONED MIXED, SEMI-HEATED]: building_total_air_leakage_rate_b += zone_b.infiltration.infiltration_flow_rate`

- Calculate the required baseline air leakage rate at 75Pa in cfm: `target_air_leakage_rate_75pa_b = 1.0 * building_total_envelope_area`

**Rule Assertion:**  

- Case 1: For B_RMD, if the total zone infiltration rate for conditioned and semi-heated zones is equal to the required baseline infiltration rate at 75Pa with a conversion factor of 0.112 as per Section G3.1.1.4: `if building_total_air_leakage_rate_b == target_air_leakage_rate_75pa_b * 0.112: PASS`

- Case 2: Else: `else: FAIL`

**Notes:**

1. Update Rule ID from 5-47 to 5-36 on 10/26/2023
2. Update Rule ID from 5-36 to 5-35 on 12/22/2023

**[Back](../_toc.md)**
