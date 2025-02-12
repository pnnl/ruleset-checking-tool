# Envelope - Rule 5-27  

**Rule ID:** 5-27  
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

  1. get_more_stringent_surface_conditioning_category()
  2. get_opaque_surface_type()
  3. get_building_scc_skylight_roof_ratios_dict()
  4. data_lookup()

## Rule Logic:  

- Get RMR climate zone: `climate_zone = ASHRAE229.weather.climate_zone`  

- Get surface conditioning category dictionary for B_RMR: `scc_dictionary_b = get_more_stringent_surface_conditioning_category(B_RMD, P_RMD)`  

- Get B_RMR skylight roof ratios dictionary: `get_building_scc_skylight_roof_ratios_dict = get_building_scc_skylight_roof_ratios_dict(B_RMR)`

- Check if B_RMR has exterior mixed type skylight: `if get_building_scc_skylight_roof_ratios_dict["EXTERIOR MIXED"] > 0:`

  - Check if residential and non-residential type skylight U-factor requirements for different skylight-roof-ratio are the same, get skylight U-factor requirements: `if ( data_lookup(table_G3_4, climate_zone, "RESIDENTIAL, "SKYLIGHT", "0%-2.0%", "ASSEMBLY MAX. U") == data_lookup(table_G3_4, climate_zone, "RESIDENTIAL, "SKYLIGHT", "2.1%+", "ASSEMBLY MAX. U") ) AND ( data_lookup(table_G3_4, climate_zone, "NON-RESIDENTIAL, "SKYLIGHT", "0%-2.0%", "ASSEMBLY MAX. U") == data_lookup(table_G3_4, climate_zone, "NON-RESIDENTIAL, "SKYLIGHT", "2.1%+", "ASSEMBLY MAX. U") ) AND ( data_lookup(table_G3_4, climate_zone, "RESIDENTIAL, "SKYLIGHT", "0%-2.0%", "ASSEMBLY MAX. U") == data_lookup(table_G3_4, climate_zone, "NON-RESIDENTIAL, "SKYLIGHT", "0%-2.0%", "ASSEMBLY MAX. U") ): target_u_factor_mixed = data_lookup(table_G3_4, climate_zone, "RESIDENTIAL, "SKYLIGHT", "0%-2.0%", "ASSEMBLY MAX. U")`

  - Else, request manual review: `else: manual_review_flag = TRUE`

- Else, B_RMR does not have exterior mixed type roof surface: `else:`

  - Get skylight-roof-ratio for residential type roofs: `srr_res = get_building_scc_skylight_roof_ratios_dict["EXTERIOR RESIDENTIAL"]`

    - If skylight-roof-ratio is greater than 2.0%, get baseline skylight construction requirement: `if srr_res > 0.02: target_u_factor_res = data_lookup(table_G3_4, climate_zone, "RESIDENTIAL", "SKYLIGHT", "2.1%+", "ASSEMBLY MAX. U")`

    - Else, skylight-roof-ratio is 0% to 2.0%, get baseline skylight construction requirement: `else: target_u_factor_res = data_lookup(table_G3_4, climate_zone, "RESIDENTIAL", "SKYLIGHT", "0%-2.0%", "ASSEMBLY MAX. U")`

  - Get skylight-roof-ratio for non-residential type roofs: `srr_nonres = get_building_scc_skylight_roof_ratios_dict["NON-RESIDENTIAL"]`

    - If skylight-roof-ratio is greater than 2.0%, get baseline skylight construction requirement: `if srr_nonres > 0.02: target_u_factor_nonres = data_lookup(table_G3_4, climate_zone, "NON-RESIDENTIAL", "SKYLIGHT", "2.1%+", "ASSEMBLY MAX. U")`

    - Else, skylight-roof-ratio is 0% to 2.0%, get baseline skylight construction requirement: `else: target_u_factor_nonres = data_lookup(table_G3_4, climate_zone, "NON-RESIDENTIAL", "SKYLIGHT", "0%-2.0%", "ASSEMBLY MAX. U")`

- Get skylight-roof-ratio for semi-exterior type roofs: `srr_semi_exterior = get_building_scc_skylight_roof_ratios_dict["SEMI-EXTERIOR"]`

  - If skylight-roof-ratio is greater than 2.0%, get baseline skylight construction requirement: `if srr_semi_exterior > 0.02: target_u_factor_semiheated = data_lookup(table_G3_4, climate_zone, "SEMIHEATED, "SKYLIGHT", "2.1%+", "ASSEMBLY MAX. U")`

  - Else, skylight-roof-ratio is 0% to 2.0%, get baseline skylight construction requirement: `else: target_u_factor_semiheated = data_lookup(table_G3_4, climate_zone, "SEMIHEATED", "SKYLIGHT", "0%-2.0%", "ASSEMBLY MAX. U")`

- For each zone in B_RMR: `for zone_b in B_RMR...zones:`

  - For each surface in zone: `for surface_b in zone_b.surfaces:`

    - Check if surface is roof with subsurface and is regulated: `if ( get_opaque_surface_type(surface_b) == "ROOF"  ) AND ( surface_b.subsurfaces ) AND ( scc_dictionary_b[surface_b.id] != "UNREGULATED" ):`

      - For each subsurface in roof: `for subsurface_b in surface_b.subsurfaces:`

        - Check if subsurface is door and glazed area is more than 50% of the total door area, or subsurface is not door: `if (( subsurface_b.classification == "DOOR" ) AND ( subsurface_b.glazed_area > subsurface_b.opaque_area )) OR ( subsurface_b.classification != "DOOR" ):`

          **Rule Assertion - Component:**

          - Case 1； For each subsurface, if roof is exterior mixed type and the baseline requirements for residential and non-residential type U-factor for different skylight-roof-ratio are different: `if manual_review_flag AND ( scc_dictionary_b[surface_b] == "EXTERIOR MIXED" ): UNDETERMINED`

          - Case 2: Else if roof is exterior mixed type and skylight U-factor matches Table G3.4 requirement: `else if ( scc_dictionary_b[surface_b] == "EXTERIOR MIXED" ) AND ( subsurface_b.u_factor == target_u_factor_mixed ): PASS`

          - Case 3: Else if roof is exterior residential type and skylight U-factor matches Table G3.4 requirement: `else if ( scc_dictionary_b[surface_b] == "EXTERIOR RESIDENTIAL" ) AND ( subsurface_b.u_factor == target_u_factor_res ): PASS`

          - Case 4: Else if roof is exterior non-residential type and skylight U-factor matches Table G3.4 requirement: `else if ( scc_dictionary_b[surface_b] == "EXTERIOR NON-RESIDENTIAL" ) AND ( subsurface_b.u_factor == target_u_factor_nonres ): PASS`

          - Case 5: Else if roof is semi-exterior type and skylight U-factor matches Table G3.4 requirement: `else if ( scc_dictionary_b[surface_b] == "SEMI-EXTERIOR" ) AND ( subsurface_b.u_factor == target_u_factor_semiheated ): PASS`

          - Case 6: Else: `else: FAIL`

**Rule Assertion - RMR:**

- Case 1: If any subsurface in B-RMR is ruled as "UNDETERMINED": `UNDETERMINED and raise_message "MANUAL REVIEW IS REQUESTED TO VERIFY SKYLIGHT MEETS U-FACTOR REQUIREMENT AS PER TABLE G3.4."`

- Case 2: Else if all subsurface in B-RMR is rules as "PASS": `PASS`

- Case 3: Else: `FAIL and raise_message "${NUMBER_OF_FAIL_COMPONENTS} of subsurfaces have failed the test.`


**Notes:**

1. Update Rule ID from 5-37 to 5-27 on 10/26/2023

**[Back](../_toc.md)**
