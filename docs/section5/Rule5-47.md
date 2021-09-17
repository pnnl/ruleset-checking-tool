
# Envelope - Rule 5-47  

**Rule ID:** 5-47  
**Rule Description:** The baseline air leakage rate of the building envelope (I75Pa) at a fixed building pressure differential of 0.3 in. of water shall be 1 cfm/ft2.  The air leakage rate of the building envelope shall be converted to appropriate units for the simulation program using one of the methods in Section G3.1.1.4.  
**Rule Assertion:** Sum of B-RMR infiltration.infiltration.air_leakage_rate = expected value.  
**Appendix G Section:** Section G3.1-5(h) Building Envelope Modeling Requirements for the Baseline building  
**Appendix G Section Reference:** None  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  None  

**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  
**Function Call:** 

  1. get_surface_conditioning_category()
  2. get_zone_conditioning_category()

## Rule Logic:  

- Get surface conditioning category dictionary for B_RMR: `scc_dict_b = get_surface_conditioning_category(B_RMR)`

- Get zone conditioning category dictionary for B_RMR: `zone_conditioning_category_dict_b = get_zone_conditioning_category(B_RMR)`

- For each building segment in the Baseline model: `for building_segment_b in B_RMR.building.building_segments:`

  - For each thermal block in building segment: `for thermal_block_b in building_segment_b.thermal_blocks:`

    - For each zone in thermal block: `for zone_b in thermal_block_b.zones:`

      - For each surface in zone: `for surface_b in zone_b.surfaces:`

        - Check if surface is regulated, add zone total area of building envelope to building total: `if scc_dict_b[surface_b.id] != "UNREGULATED": building_total_envelope_area += sum(surface.area for surface in zone_b.surfaces)`

      - Check if zone is conditioned or semi-heated, add zone air leakage rate to building total: `if zone_conditioning_category_dict_b[zone.id] in [CONDITIONED RESIDENTIAL, CONDITIONED NON-RESIDENTIAL, CONDITIONED MIXED, SEMI-HEATED]: building_total_air_leakage_rate += zone_b.infiltration.air_leakage_rate`

- Calculate the required baseline air leakage rate at 75Pa: `target_air_leakage_rate_b = 1.0 * building_total_envelope_area * 0.00047194745`

**Rule Assertion:**  

- Case 1: For B_RMR, if infiltration pressure difference is 75Pa and the total air leakage rate for conditioned and semi-heated zones is equal to the required baseline air leakage rate at 75Pa: `if ( B_RMR.ASHRAE229.infiltration_pressure_difference == 75 ) AND ( building_total_air_leakage_rate == target_air_leakage_rate_b ): PASS`

- Case 2: Else if infiltration pressure difference is 75Pa for B_RMR and the total air leakage rate for conditioned and semi-heated zones is not equal to the required baseline air leakage rate at 75Pa: `if ( B_RMR.ASHRAE229.infiltration_pressure_difference == 75 ) AND ( building_total_air_leakage_rate != target_air_leakage_rate_b ): FAIL`

- Case 3: Else if infiltration pressure difference is 0Pa for B_RMR and the total air leakage rate for conditioned and semi-heated zones is equal to the required baseline air leakage rate at 0Pa: `if ( B_RMR.ASHRAE229.infiltration_pressure_difference == 0 ) AND ( building_total_air_leakage_rate == target_air_leakage_rate_b * 0.112 ): PASS`

- Case 4: Else if infiltration pressure difference is 0Pa for B_RMR and the total air leakage rate for conditioned and semi-heated zones is not equal to the required baseline air leakage rate at 0Pa: `if ( B_RMR.ASHRAE229.infiltration_pressure_difference == 0 ) AND ( building_total_air_leakage_rate != target_air_leakage_rate_b * 0.112 ): FAIL`

- Case 5: Else, infiltration pressure difference is neither 75Pa nor 0Pa for B_RMR: `else: FAIL and raise_warning "90.1 SECTION G3.1.1.4 PRESCRIBED BASELINE INFILTRATION RATE AT 75PA AND METHODOLOGY TO CONVERT AIR LEAKAGE RATE AT 75PA TO AIR LEAKAGE AT WIND PRESSURE. THE MODELED INFILTRATION IS AT PRESSURE DIFFERENTIAL OTHER THAN THE TWO OPTIONS PRESCRIBED BY 90.1. MANUAL CHECK IS REQUIRED TO VERIFY THAT BASELINE INFILTRATION WAS MODELED CORRECTLY."`

**[Back](../_toc.md)**
