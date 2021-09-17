
# Envelope - Rule 5-37  

**Rule ID:** 5-37  
**Rule Description:** Skylight U-factors for residential, non-residential and semi-heated spaces in the baseline model must match the appropriate requirements in Table G3.4-1 through G3.4-8.  
**Rule Assertion:** B-RMR subsurface: U_factor = expected value  
**Appendix G Section:** Section G3.1-5(e) Building Envelope Modeling Requirements for the Baseline building  
**Appendix G Section Reference:** Tables G3.4-1 to G3.4-8  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:** None  

**Manual Check:** Yes  
**Evaluation Context:** Each Data Element  
**Data Lookup:** Tables G3.4-1 to G3.4-8  
**Function Call:**

  1. get_surface_conditioning_category()  
  2. get_opaque_surface_type()  
  3. get_building_segment_skylight_roof_areas()

## Rule Logic:  

- Get building climate zone: `climate_zone = B_RMR.weather.climate_zone`  

- Get surface conditioning category dictionary for B_RMR: `scc_dictionary_b = get_surface_conditioning_category(B_RMR)`  

- Get building skylight roof areas dictionary: `skylight_roof_areas_dictionary_b = get_building_segment_skylight_roof_areas(B_RMR)`

- For each building segment in the Baseline model: `for building_segment_b in B_RMR.building.building_segments:`  

  - Calculate building segment skylight roof ratio: `srr_b = skylight_roof_areas_dictionary_b[building_segment_b.id][0] / skylight_roof_areas_dictionary_b[building_segment_b.id][1]`

    - If skylight roof area is 2% or less, set skylight percentage of roof area to "0%-2.0%": `if srr_b <=0.02: skylight_type_b = "0%-2.0%"`

    - Else, set skylight percentage of roof area to "2.1%+": `else: skylight_type_b = "2.1+"`

  - For each thermal_block in building segment: `for thermal_block_b in building_segment_b.thermal_blocks:`  

    - For each zone in thermal block: `for zone_b in thermal_block_b.zones:`  

      - For each surface in zone: `for surface_b in zone_b.surfaces:`  

        - Check if surface is roof or ceiling and is regulated, get surface conditioning category: `if ( get_opaque_surface_type(surface_b) == "ROOF" ) AND ( scc_dictionary_b[surface_b] != "UNREGULATED" ): scc_b = scc_dictionary_b[surface_b]`

          - If surface is exterior residential, exterior non-residential, or semi-exterior, get baseline skylight construction U-factor from Table G3.4-1 to G3.4-8 based on climate zone, surface conditioning category and skylight percentage of roof area: `if scc_b in ["EXTERIOR RESIDENTIAL", "EXTERIOR NON-RESIDENTIAL", "SEMI-EXTERIOR"]: target_u_factor = data_lookup(table_G3_4, climate_zone, scc_b, "SKYLIGHT", skylight_type_b, "ASSEMBLY MAX. U")`  

          - Else if surface is exterior mixed, get baseline construction for both residential and non-residential type skylight: `else if ( scc_b == "EXTERIOR MIXED" ): target_u_factor_res = data_lookup(table_G3_4, climate_zone, "EXTERIOR RESIDENTIAL", "SKYLIGHT", skylight_type_b, "ASSEMBLY MAX. U"), target_u_factor_nonres = data_lookup(table_G3_4, climate_zone, "EXTERIOR NON-RESIDENTIAL", "SKYLIGHT", skylight_type_b, "ASSEMBLY MAX. U")`  

            - If residential and non-residential type skylight construction requirements are the same, save as baseline construction U-factor: `if target_u_factor_res == target_u_factor_nonres: target_u_factor = target_u_factor_res`  

            - Else: `manual_review_flag = TRUE`  

          - For each subsurface in surface, check if subsurface is skylight: `if subsurface.classification == "SKYLIGHT" for subsurface in surface_b.subsurfaces:`

            **Rule Assertion:**  

            Case 1: For each skylight, if zone has both residential and non-residential spaces and the construction requirements for skylight are different, request manual review: `if manual_review_flag: CAUTION and raise_warning "ZONE HAS BOTH RESIDENTIAL AND NON-RESIDENTIAL SPACES AND THE CONSTRUCTION U-FACTOR REQUIREMENTS FOR SKYLIGHT ARE DIFFERENT. VERIFY SKYLIGHT U-FACTOR IS MODELED CORRECTLY."`  

            Case 2: Else if skylight U-factor matches Table G3.4: `else if subsurface.u_factor == target_u_factor: PASS`  

            Case 3: Else: `else: FAIL`  

**[Back](../_toc.md)**
