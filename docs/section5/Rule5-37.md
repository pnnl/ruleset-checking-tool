
# Envelope - Rule 5-37  

**Rule ID:** 5-37  
**Rule Description:** The proposed air leakage rate of the building envelope (I<sub>75Pa</sub>) at a fixed building pressure differential of 0.3 in. of water shall be 0.6 cfm/ft2 for buildings providing verification in accordance with Section 5.9.1.2. The air leakage rate of the building envelope shall be converted to appropriate units for the simulation program using one of the methods in Section G3.1.1.4. Exceptions: When whole-building air leakage testing, in accordance with Section 5.4.3.1.1, is specified during design and completed after construction, the proposed design air leakage rate of the building envelope shall be as measured.  
**Rule Assertion:** Sum of P-RMR zone.infiltration.air_leakage_rate = expected value  
**Appendix G Section:** Section G3.1-5(b) Building Envelope Modeling Requirements for the Proposed design  
**Appendix G Section Reference:** None  

**Applicability:** All required data elements exist for P_RMR  
**Applicability Checks:**  None  

**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  
**Function Call:**

  1. get_more_stringent_surface_conditioning_category()
  2. get_zone_conditioning_category()

## Rule Logic:  

- Get surface conditioning category dictionary for P_RMR: `scc_dict_p = get_more_stringent_surface_conditioning_category(B_RMD, P_RMD)`

- Get zone conditioning category dictionary for P_RMR: `zone_conditioning_category_dict_p = get_zone_conditioning_category(P_RMR)`

- For each building segment in the Proposed model: `for building_segment_p in P_RMR.building.building_segments:`

  - For each zone in building segment: `for zone_p in building_segment_p.zones:`

    - For each surface in zone: `for surface_p in zone_p.surfaces:`

      - Check if surface is regulated, add zone total area of building envelope to building total: `if scc_dict_p[surface_p.id] != "UNREGULATED": building_total_envelope_area += sum(surface.area for surface in zone_p.surfaces)`

    - Check if zone is conditioned or semi-heated, add zone air leakage rate to building total: `if zone_conditioning_category_dict_p[zone.id] in [CONDITIONED RESIDENTIAL, CONDITIONED NON-RESIDENTIAL, CONDITIONED MIXED, SEMI-HEATED]: building_total_air_leakage_rate += zone_p.infiltration.infiltration_flow_rate`

      - Check if measured air leakage rate is not entered for zone, raise empty measured air leakage rate flag: `if NOT zone_p.infiltration.measured_air_leakage_rate: empty_measured_air_leakage_rate_flow_flag = TRUE`

      - Else, measured air leakage rate is entered for zone, add measured air leakage rate to building total: `else: building_total_measured_air_leakage_rate += zone_p.infiltration.measured_air_leakage_rate`

- Calculate the required proposed design air leakage rate at 75Pa: `target_air_leakage_rate_75pa_p = 0.6 * building_total_envelope_area`

**Rule Assertion:**  

- Case 1: For P_RMR, if the building total air leakage rate for conditioned and semi-heated zones is equal to the required proposed design air leakage rate at 75Pa with a conversion factor of 0.112 as per Section G3.1.1.4: `if building_total_air_leakage_rate == target_air_leakage_rate_75pa_p * 0.112: PASS`

- Case 2: else if 1). the building total air leakage rate for conditioned and semi-heated zones is not equal to the required proposed design air leakage rate at 75Pa with a conversion factor of 0.112 as per Section G3.1.1.4, and 2). measured air leakage rate is not entered for all conditioned and semi-heated zones: `else if ( building_total_air_leakage_rate != target_air_leakage_rate_75pa_p * 0.112 ) AND ( empty_measured_air_leakage_rate_flow_flag ): UNDETERMINED and raise_message "THE BUILDING TOTAL AIR LEAKAGE RATE IS NOT EQUAL TO THE REQUIRED PROPOSED DESIGN AIR LEAKAGE RATE AT 75PA WITH A CONVERSION FACTOR OF 0.112 AS PER SECTION G3.1.1.4. AND MEASURED AIR LEAKAGE RATE IS NOT ENTERED FOR ALL CONDITIONED AND SEMI-HEATED ZONES. VERIFY THE PROPOSED AIR LEAKAGE RATE IS MODELED CORRECTLY."`

- Case 3: else if 1). the building total air leakage rate for conditioned and semi-heated zones is not equal to the required proposed design air leakage rate at 75Pa with a conversion factor of 0.112 as per Section G3.1.1.4, and 2). the measured air leakage rate is entered for all conditioned and semi-heated zones, and 3). the building total air leakage rate is equal to the measured air leakage rate with a conversion factor of 0.112 as per Section G3.1.1.4: `else if ( building_total_air_leakage_rate != target_air_leakage_rate_75pa_p * 0.112 ) AND ( empty_measured_air_leakage_rate_flow_flag == FALSE ) AND ( building_total_air_leakage_rate == building_total_measured_air_leakage_rate * 0.112 ): PASS`

- Case 4: else, 1). the building total air leakage rate for conditioned and semi-heated zones is not equal to the required proposed design air leakage rate at 75Pa with a conversion factor of 0.112 as per Section G3.1.1.4, and 2). the measured air leakage rate is entered for all conditioned and semi-heated zones, but 3). the building total air leakage rate is not equal to the measured air leakage rate with a conversion factor of 0.112 as per Section G3.1.1.4: `else: FAIL`

**Notes:**

1. Update Rule ID from 5-49 to 5-38 on 10/26/2023
2. Update Rule ID from 5-38 to 5-37 on 12/22/2023

**[Back](../_toc.md)**
