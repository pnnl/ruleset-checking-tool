
# Envelope - Rule 5-37  

**Rule ID:** 5-37  
**Rule Description:** Skylight U-factors for residential, non-residential and semi-heated spaces in the baseline model must match the appropriate requirements in Table G3.4-1 through G3.4-8.  
**Rule Assertion:** B-RMR subsurface: U_factor = expected value  
**Appendix G Section:** Section 5 Envelope  
**Appendix G Section Reference:** Section G3.1-5(e) Building Envelope Modeling Requirements for the Baseline building

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:** None  

**Manual Check:** Yes  
**Evaluation Context:** Each Data Element  
**Data Lookup:** Tables G3.4-1 to G3.4-8  
**Function Call:**

  1. get_surface_conditioning_category()
  2. get_opaque_surface_type()
  3. get_scc_skylight_roof_ratios()
  4. data_lookup()

## Rule Logic:  

- Get building climate zone: `climate_zone = B_RMR.weather.climate_zone`  

- Get surface conditioning category dictionary for B_RMR: `scc_dictionary_b = get_surface_conditioning_category(B_RMR)`  

- Get building skylight roof ratios dictionary: `skylight_roof_ratios_dictionary_b = get_scc_skylight_roof_ratios(B_RMR)`

- For each building segment in the Baseline model: `for building_segment_b in B_RMR.building.building_segments:`

  - Check if building segment has exterior mixed type skylight: `if skylight_roof_ratios_dictionary_b[building_segment_b.id]["EXTERIOR MIXED"] > 0:`

    - Check if residential and non-residential type skylight U-factor requirements for different skylight-roof-ratio are the same, get skylight U-factor requirements: `if ( data_lookup(table_G3_4, climate_zone, "RESIDENTIAL, "SKYLIGHT", "0%-2.0%", "ASSEMBLY MAX. U") == data_lookup(table_G3_4, climate_zone, "RESIDENTIAL, "SKYLIGHT", "2.1%+", "ASSEMBLY MAX. U") ) AND ( data_lookup(table_G3_4, climate_zone, "NON-RESIDENTIAL, "SKYLIGHT", "0%-2.0%", "ASSEMBLY MAX. U") == data_lookup(table_G3_4, climate_zone, "NON-RESIDENTIAL, "SKYLIGHT", "2.1%+", "ASSEMBLY MAX. U") ) AND ( data_lookup(table_G3_4, climate_zone, "RESIDENTIAL, "SKYLIGHT", "0%-2.0%", "ASSEMBLY MAX. U") == data_lookup(table_G3_4, climate_zone, "NON-RESIDENTIAL, "SKYLIGHT", "0%-2.0%", "ASSEMBLY MAX. U") ): target_u_factor_res = target_u_factor_nonres = data_lookup(table_G3_4, climate_zone, "RESIDENTIAL, "SKYLIGHT", "0%-2.0%", "ASSEMBLY MAX. U")`

    - Else, request manual review: `else: manual_review_flag = TRUE`

  - Else, building segment does not have exterior mixed type roof surface: `else:`

    - Get skylight-roof-ratio for residential type roofs: `srr_res = skylight_roof_ratios_dictionary_b[building_segment_b.id]["EXTERIOR RESIDENTIAL"]`

      - If skylight-roof-ratio is greater than 2.0%, get baseline skylight construction requirement: `if srr_res > 0.02: target_u_factor_res = data_lookup(table_G3_4, climate_zone, "RESIDENTIAL", "SKYLIGHT", "2.1%+", "ASSEMBLY MAX. U")`

      - Else, skylight-roof-ratio is 0% to 2.0%, get baseline skylight construction requirement: `else: target_u_factor_res = data_lookup(table_G3_4, climate_zone, "RESIDENTIAL", "SKYLIGHT", "0%-2.0%", "ASSEMBLY MAX. U")`

    - Get skylight-roof-ratio for non-residential type roofs: `srr_nonres = skylight_roof_ratios_dictionary_b[building_segment_b.id]["NON-RESIDENTIAL"]`

      - If skylight-roof-ratio is greater than 2.0%, get baseline skylight construction requirement: `if srr_nonres > 0.02: target_u_factor_nonres = data_lookup(table_G3_4, climate_zone, "NON-RESIDENTIAL", "SKYLIGHT", "2.1%+", "ASSEMBLY MAX. U")`

      - Else, skylight-roof-ratio is 0% to 2.0%, get baseline skylight construction requirement: `else: target_u_factor_nonres = data_lookup(table_G3_4, climate_zone, "NON-RESIDENTIAL", "SKYLIGHT", "0%-2.0%", "ASSEMBLY MAX. U")`

  - Get skylight-roof-ratio for semi-exterior type roofs: `srr_semi_exterior = skylight_roof_ratios_dictionary_b[building_segment_b.id]["SEMI-EXTERIOR"]`

    - If skylight-roof-ratio is greater than 2.0%, get baseline skylight construction requirement: `if srr_semi_exterior > 0.02: target_u_factor_semiheated = data_lookup(table_G3_4, climate_zone, "SEMIHEATED, "SKYLIGHT", "2.1%+", "ASSEMBLY MAX. U")`

    - Else, skylight-roof-ratio is 0% to 2.0%, get baseline skylight construction requirement: `else: target_u_factor_semiheated = data_lookup(table_G3_4, climate_zone, "SEMIHEATED", "SKYLIGHT", "0%-2.0%", "ASSEMBLY MAX. U")`

  - For each zone in building segment: `for zone_b in building_segment_b...zones:`

    - For each surface in zone: `for surface_b in zone_b.surfaces:`

      - Check if surface is roof and has subsurface: `if ( get_opaque_surface_type(surface_b) == "ROOF"  ) AND ( surface_b.subsurfaces ):`

        - For each subsurface in roof: `for subsurface_b in surface_b.subsurfaces:`

          **Rule Assertion:**

          - Case 1； If roof is exterior mixed type and the baseline requirements for residential and non-residential type U-factor for different skylight-roof-ratio are different: `if manual_review_flag AND ( scc_dictionary_b[surface_b] == "EXTERIOR MIXED" ): CAUTION and raise_warning "MANUAL REVIEW IS REQUESTED TO VERIFY SKYLIGHT MEETS U-FACTOR REQUIREMENT AS PER TABLE G3.4."`

          - Case 2: Else if roof is exterior mixed type and skylight U-factor matches Table G3.4 requirement: `else if ( scc_dictionary_b[surface_b] == "EXTERIOR MIXED" ) AND ( subsurface_b.u_factor == target_u_factor_res ): PASS`

          - Case 3: Else if roof is exterior residential type and skylight U-factor matches Table G3.4 requirement: `else if ( scc_dictionary_b[surface_b] == "EXTERIOR RESIDENTIAL" ) AND ( subsurface_b.u_factor == target_u_factor_res ): PASS`

          - Case 4: Else if roof is exterior non-residential type and skylight U-factor matches Table G3.4 requirement: `else if ( scc_dictionary_b[surface_b] == "EXTERIOR NON-RESIDENTIAL" ) AND ( subsurface_b.u_factor == target_u_factor_nonres ): PASS`

          - Case 5: Else if roof is semi-exterior type and skylight U-factor matches Table G3.4 requirement: `else if ( scc_dictionary_b[surface_b] == "SEMI-EXETERIOR" ) AND ( subsurface_b.u_factor == target_u_factor_semiheated ): PASS`

          - Case 6: Else: `else: FAIL`

**[Back](../_toc.md)**
