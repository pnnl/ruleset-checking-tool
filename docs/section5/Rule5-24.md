
# Envelope - Rule 5-24  

**Rule ID:** 5-24  
**Rule Description:** Vertical fenestration U-factors for residential, non-residential and semi-heated spaces in the baseline model must match the appropriate requirements in Table G3.4-1 through G3.4-8 for the appropriate WWR in the baseline RMR.  
**Rule Assertion:** Baseline RMR = expected value  
**Appendix G Section:** Section G3.1-5(d) Building Envelope Modeling Requirements for the Baseline building  
**Appendix G Section Reference:** Tables G3.4-1 to G3.4-8  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  None  

**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** Tables G3.4-1 to G3.4-8  
**Function Call:**  

  1. data_lookup()
  2. get_opaque_surface_type()
  3. get_surface_conditioning_category()
  4. get_building_scc_window_wall_ratios()

## Rule Logic:  

- Get building climate zone: `climate_zone = B_RMR.weather.climate_zone`

- Get surface conditioning category dictionary for B_RMR: `scc_dictionary_b = get_surface_conditioning_category(B_RMR)`

- Get window wall ratio ratios dictionary for B_RMR: `building_scc_window_wall_ratios_dictionary = get_building_scc_window_wall_ratios(B_RMR)`

- For each building in the Baseline model: `for building_b in B_RMR.buildings:`

  - Check if building has exterior mixed type fenestration: `if building_scc_window_wall_ratios_dictionary[building_b.id]["EXTERIOR MIXED"] > 0:`

    - Check if residential and non-residential type vertical fenestration U-factor requirements for different window-wall-ratio are the same, get vertical fenestration U-factor requirements: `if ( data_lookup(table_G3_4, climate_zone, "RESIDENTIAL, "VERTICAL GLAZING", "0%-10.0%", "ASSEMBLY MAX. U") == data_lookup(table_G3_4, climate_zone, "RESIDENTIAL, "VERTICAL GLAZING", "10.1%-20.0", "ASSEMBLY MAX. U") == data_lookup(table_G3_4, climate_zone, "RESIDENTIAL, "VERTICAL GLAZING", "20.1%-30.0", "ASSEMBLY MAX. U") == data_lookup(table_G3_4, climate_zone, "RESIDENTIAL, "VERTICAL GLAZING", "30.1%-40.0", "ASSEMBLY MAX. U")) AND ( data_lookup(table_G3_4, climate_zone, "NON-RESIDENTIAL, "VERTICAL GLAZING", "0%-10.0%", "ASSEMBLY MAX. U") == data_lookup(table_G3_4, climate_zone, "NON-RESIDENTIAL, "VERTICAL GLAZING", "10.1%-20.0", "ASSEMBLY MAX. U") == data_lookup(table_G3_4, climate_zone, "NON-RESIDENTIAL, "VERTICAL GLAZING", "20.1%-30.0", "ASSEMBLY MAX. U") == data_lookup(table_G3_4, climate_zone, "NON-RESIDENTIAL, "VERTICAL GLAZING", "30.1%-40.0", "ASSEMBLY MAX. U")) AND ( data_lookup(table_G3_4, climate_zone, "RESIDENTIAL, "VERTICAL GLAZING", "0%-10.0%", "ASSEMBLY MAX. U") == data_lookup(table_G3_4, climate_zone, "NON-RESIDENTIAL, "VERTICAL GLAZING", "0%-10.0%", "ASSEMBLY MAX. U") ): target_u_factor_mixed = data_lookup(table_G3_4, climate_zone, "RESIDENTIAL, "VERTICAL GLAZING", "0%-10.0%", "ASSEMBLY MAX. U")`

    - Else, request manual review: `else: manual_review_flag = TRUE`

  - Else, building does not have exterior mixed type wall surface: `else:`

    - Get window-wall-ratio for residential type walls: `wwr_res = building_scc_window_wall_ratios_dictionary[building_b.id]["EXTERIOR RESIDENTIAL"]`

      - If window-wall-ratio is between 0% to 10%, get baseline vertical fenestration construction U-factor requirement: `if ( wwr_res > 0.0% ) AND ( wwr_res <= 10.0% ): target_u_factor_res = data_lookup(table_G3_4, climate_zone, "RESIDENTIAL", "VERTICAL GLAZING", "0%-10.0%", "ASSEMBLY MAX. U")`

      - Else if window-wall-ratio is between 10% to 20%, get baseline vertical fenestration construction U-factor requirement: `if ( wwr_res > 10.0% ) AND ( wwr_res <= 20.0% ): target_u_factor_res = data_lookup(table_G3_4, climate_zone, "RESIDENTIAL", "VERTICAL GLAZING", "10.1%-20.0%", "ASSEMBLY MAX. U")`

      - Else if window-wall-ratio is between 20% to 30%, get baseline vertical fenestration construction U-factor requirement: `if ( wwr_res > 20.0% ) AND ( wwr_res <= 30.0% ): target_u_factor_res = data_lookup(table_G3_4, climate_zone, "RESIDENTIAL", "VERTICAL GLAZING", "20.1%-30.0%", "ASSEMBLY MAX. U")`

      - Else, window-wall-ratio is between 30% to 40%, get baseline vertical fenestration construction U-factor requirement: `if ( wwr_res > 30.0% ) AND ( wwr_res <= 40.0% ): target_u_factor_res = data_lookup(table_G3_4, climate_zone, "RESIDENTIAL", "VERTICAL GLAZING", "30.1%-40.0%", "ASSEMBLY MAX. U")`

    - Get window-wall-ratio for non-residential type walls: `wwr_nonres = building_scc_window_wall_ratios_dictionary[building_b.id]["EXTERIOR NON-RESIDENTIAL"]`

      - If window-wall-ratio is between 0% to 10%, get baseline vertical fenestration construction U-factor requirement: `if ( wwr_nonres > 0.0% ) AND ( wwr_nonres <= 10.0% ): target_u_factor_nonres = data_lookup(table_G3_4, climate_zone, "NON-RESIDENTIAL", "VERTICAL GLAZING", "0%-10.0%", "ASSEMBLY MAX. U")`

      - Else if window-wall-ratio is between 10% to 20%, get baseline vertical fenestration construction U-factor requirement: `if ( wwr_nonres > 10.0% ) AND ( wwr_nonres <= 20.0% ): target_u_factor_nonres = data_lookup(table_G3_4, climate_zone, "NON-RESIDENTIAL", "VERTICAL GLAZING", "10.1%-20.0%", "ASSEMBLY MAX. U")`

      - Else if window-wall-ratio is between 20% to 30%, get baseline vertical fenestration construction U-factor requirement: `if ( wwr_nonres > 20.0% ) AND ( wwr_nonres <= 30.0% ): target_u_factor_nonres = data_lookup(table_G3_4, climate_zone, "NON-RESIDENTIAL", "VERTICAL GLAZING", "20.1%-30.0%", "ASSEMBLY MAX. U")`

      - Else, window-wall-ratio is between 30% to 40%, get baseline vertical fenestration construction U-factor requirement: `if ( wwr_nonres > 30.0% ) AND ( wwr_nonres <= 40.0% ): target_u_factor_nonres = data_lookup(table_G3_4, climate_zone, "NON-RESIDENTIAL", "VERTICAL GLAZING", "30.1%-40.0%", "ASSEMBLY MAX. U")`

    - Get window-wall-ratio for semi-heated type walls: `wwr_semiheated = building_scc_window_wall_ratios_dictionary[building_b.id]["SEMI-EXTERIOR"]`

      - If window-wall-ratio is between 0% to 10%, get baseline vertical fenestration construction U-factor requirement: `if ( wwr_semiheated > 0.0% ) AND ( wwr_semiheated <= 10.0% ): target_u_factor_semiheated = data_lookup(table_G3_4, climate_zone, "SEMIHEATED", "VERTICAL GLAZING", "0%-10.0%", "ASSEMBLY MAX. U")`

      - Else if window-wall-ratio is between 10% to 20%, get baseline vertical fenestration construction U-factor requirement: `if ( wwr_semiheated > 10.0% ) AND ( wwr_semiheated <= 20.0% ): target_u_factor_semiheated = data_lookup(table_G3_4, climate_zone, "SEMIHEATED", "VERTICAL GLAZING", "10.1%-20.0%", "ASSEMBLY MAX. U")`

      - Else if window-wall-ratio is between 20% to 30%, get baseline vertical fenestration construction U-factor requirement: `if ( wwr_semiheated > 20.0% ) AND ( wwr_semiheated <= 30.0% ): target_u_factor_semiheated = data_lookup(table_G3_4, climate_zone, "SEMIHEATED", "VERTICAL GLAZING", "20.1%-30.0%", "ASSEMBLY MAX. U")`

      - Else, window-wall-ratio is between 30% to 40%, get baseline vertical fenestration construction U-factor requirement: `if ( wwr_semiheated > 30.0% ) AND ( wwr_semiheated <= 40.0% ): target_u_factor_semiheated = data_lookup(table_G3_4, climate_zone, "SEMIHEATED", "VERTICAL GLAZING", "30.1%-40.0%", "ASSEMBLY MAX. U")`

  - For each zone in building: `for zone_b in building_b...zones:`

    - For each surface in zone: `for surface_b in zone_b.surfaces:`

      - Check if surface is above-grade wall with subsurface and is regulated: `if ( get_opaque_surface_type(surface_b) == "ABOVE-GRADE WALL" ) AND ( surface_b.subsurfaces ) AND ( scc_dictionary_b[surface_b.id] != "UNREGULATED" ):`

        - For each subsurface in wall: `for subsurface_b in surface_b.subsurfaces:`

          - Check if subsurface is door and glazed area is more than 50% of the total door area, or subsurface is not door: `if (( subsurface_b.classification == "DOOR" ) AND ( subsurface_b.glazed_area > subsurface_b.opaque_area )) OR ( subsurface_b.classification != "DOOR" ):`

            **Rule Assertion - Component:**

            - Case 1: For each subsurface that is vertical fenestration, if wall is exterior mixed type and the baseline requirements for residential and non-residential type U-factor for different window-wall-ratio are different: `if manual_review_flag AND ( scc_dictionary_b[surface_b] == "EXTERIOR MIXED" ): UNDETERMINED`

            - Case 2: Else if wall is exterior mixed type and vertical fenestration U-factor matches Table G3.4 requirement: `else if ( scc_dictionary_b[surface_b] == "EXTERIOR MIXED" ) AND ( subsurface_b.u_factor == target_u_factor_mixed ): PASS`

            - Case 3: Else if wall is exterior residential type and vertical fenestration U-factor matches Table G3.4 requirement: `else if ( scc_dictionary_b[surface_b] == "EXTERIOR RESIDENTIAL" ) AND ( subsurface_b.u_factor == target_u_factor_res ): PASS`

            - Case 4: Else if wall is exterior non-residential type and vertical fenestration U-factor matches Table G3.4 requirement: `else if ( scc_dictionary_b[surface_b] == "EXTERIOR NON-RESIDENTIAL" ) AND ( subsurface_b.u_factor == target_u_factor_nonres ): PASS`

            - Case 5: Else if wall is semi-exterior type and skylight U-factor matches Table G3.4 requirement: `else if ( scc_dictionary_b[surface_b] == "SEMI-EXTERIOR" ) AND ( subsurface_b.u_factor == target_u_factor_semiheated ): PASS`

            - Case 6: Else: `else: FAIL`

**Rule Assertion - RMR:**

- Case 1: If any subsurface in B-RMR is ruled as "UNDETERMINED": `UNDETERMINED and raise_message "MANUAL REVIEW IS REQUESTED TO VERIFY VERTICAL FENESTRATION MEETS U-FACTOR REQUIREMENT AS PER TABLE G3.4."`

- Case 2: Else if all subsurface in B-RMR is rules as "PASS": `PASS`

- Case 3: Else: `FAIL and raise_message "${NUMBER_OF_FAIL_COMPONENTS} of subsurfaces have failed the test."`

**[Back](../_toc.md)**
