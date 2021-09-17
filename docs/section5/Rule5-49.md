
# Envelope - Rule 5-49  

**Rule ID:** 5-49  
**Rule Description:** The proposed air leakage rate of the building envelope (I75Pa) at a fixed building pressure differential of 0.3 in. of water shall be 0.6 cfm/ft2 for buildings providing verification in accordance with Section 5.9.1.2. The air leakage rate of the building envelope shall be converted to appropriate units for the simulation program using one of the methods in Section G3.1.1.4. Exceptions: When whole-building air leakage testing, in accordance with Section 5.4.3.1.1, is specified during design and completed after construction, the proposed design air leakage rate of the building envelope shall be as measured.  
**Rule Assertion:** Sum of P-RMR zone.infiltration.air_leakage_rate = expected value  
**Appendix G Section:** Section G3.1-5(b) Building Envelope Modeling Requirements for the Proposed design  
**Appendix G Section Reference:** None  

**Applicability:** All required data elements exist for P_RMR  
**Applicability Checks:**  None  

**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  
**Function Call:** 

  1. get_surface_conditioning_category()
  2. get_zone_conditioning_category()

## Rule Logic:  

- Get surface conditioning category dictionary for P_RMR: `scc_dict_p = get_surface_conditioning_category(P_RMR)`

- Get zone conditioning category dictionary for P_RMR: `zone_conditioning_category_dict_p = get_zone_conditioning_category(P_RMR)`

- For each building segment in the Proposed model: `for building_segment_p in P_RMR.building.building_segments:`

  - For each thermal block in building segment: `for thermal_block_p in building_segment_p.thermal_blocks:`

    - For each zone in thermal block: `for zone_p in thermal_block_p.zones:`

      - For each surface in zone: `for surface_p in zone_p.surfaces:`

        - Check if surface is regulated, add zone total area of building envelope to building total: `if scc_dict_p[surface_p.id] != "UNREGULATED": building_total_envelope_area += sum(surface.area for surface in zone_p.surfaces)`

      - Check if zone is conditioned or semi-heated, add zone air leakage rate to building total: `if zone_conditioning_category_dict_p[zone.id] in [CONDITIONED RESIDENTIAL, CONDITIONED NON-RESIDENTIAL, CONDITIONED MIXED, SEMI-HEATED]: building_total_air_leakage_rate += zone_p.infiltration.air_leakage_rate`

- Calculate the required proposed design air leakage rate at 75Pa: `target_air_leakage_rate_p = 0.6 * building_total_envelope_area * 0.00047194745`

**Rule Assertion:**  

- Case 1: For P_RMR, if infiltration pressure difference is 75Pa and the total air leakage rate for conditioned and semi-heated zones is equal to the required proposed design air leakage rate at 75Pa: `if ( P_RMR.ASHRAE229.infiltration_pressure_difference == 75 ) AND ( building_total_air_leakage_rate == target_air_leakage_rate_p ): PASS`

- Case 2: Else if infiltration pressure difference is 75Pa for P_RMR and the total air leakage rate for conditioned and semi-heated zones is not equal to the required proposed design air leakage rate at 75Pa: `if ( P_RMR.ASHRAE229.infiltration_pressure_difference == 75 ) AND ( building_total_air_leakage_rate != target_air_leakage_rate_p ): FAIL`

- Case 3: Else if infiltration pressure difference is 0Pa for P_RMR and the total air leakage rate for conditioned and semi-heated zones is equal to the required proposed design air leakage rate at 0Pa: `if ( P_RMR.ASHRAE229.infiltration_pressure_difference == 0 ) AND ( building_total_air_leakage_rate == target_air_leakage_rate_p * 0.112 ): PASS`

- Case 4: Else if infiltration pressure difference is 0Pa for P_RMR and the total air leakage rate for conditioned and semi-heated zones is not equal to the required proposed design air leakage rate at 0Pa: `if ( P_RMR.ASHRAE229.infiltration_pressure_difference == 0 ) AND ( building_total_air_leakage_rate != target_air_leakage_rate_p * 0.112 ): FAIL`

- Case 5: Else, infiltration pressure difference is neither 75Pa nor 0Pa for P_RMR: `else: FAIL and raise_warning "90.1 SECTION G3.1.1.4 PRESCRIBED PROPOSED DESIGN INFILTRATION RATE AT 75PA AND METHODOLOGY TO CONVERT AIR LEAKAGE RATE AT 75PA TO AIR LEAKAGE AT WIND PRESSURE. THE MODELED INFILTRATION IS AT PRESSURE DIFFERENTIAL OTHER THAN THE TWO OPTIONS PRESCRIBED BY 90.1. EXCEPTION APPLIES WHEN WHOLE-BUILDING AIR LEAKAGE TESTING IS SPECIFIED DURING DESIGN AND COMPLETED AFTER CONSTRUCTION. THE PROPOSED DESIGN AIR LEAKAGE RATE OF THE BUILDING ENVELOPE SHALL BE AS MEASURED. MANUAL CHECK IS REQUIRED TO VERIFY THAT PROPOSED DESIGN INFILTRATION WAS MODELED CORRECTLY."`

**[Back](../_toc.md)**
