
# Envelope - Rule 5-6  

**Rule ID:** 5-6  
**Rule Description:** Baseline below-grade walls shall match the appropriate assembly maximum C-factors in Tables G3.4-1 through G3.4-8.  
**Rule Assertion:** Baseline RMR below-grade wall: C_factor = expected value  
**Appendix G Section:** Section G3.1-5(b) Building Envelope Modeling Requirements for the Baseline building  
**Appendix G Section Reference:** Tables G3.4-1 to G3.4-8  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:** None  

**Manual Check:** Yes  
**Evaluation Context:** Each Data Element  
**Data Lookup:** Tables G3.4-1 to G3.4-8  
**Function Call:**  

  1. get_more_stringent_surface_conditioning_category()  
  2. get_opaque_surface_type()  

## Rule Logic:  

- Get building climate zone: ```climate_zone = B_RMR.weather.climate_zone```  

- Get surface conditioning category dictionary for B_RMR: ```scc_dictionary_b = get_more_stringent_surface_conditioning_category(B_RMR, P_RMR)```  

- For each building segment in the Baseline model: ```for building_segment_b in B_RMR.building.building_segments:```  

  - For each thermal_block in building segment: ```for thermal_block_b in building_segment_b.thermal_blocks:```  

    - For each zone in thermal block: ```for zone_b in thermal_block_b.zones:```  

      - For each surface in zone: ```for surface_b in zone_b.surfaces:```  

        - Check if surface is below-grade wall: ```if get_opaque_surface_type(surface_b) == "BELOW-GRADE WALL":```  

          - Get surface construction: ```surface_construction_b = surface_b.construction```  

          - Get surface conditioning category: ```scc_b = scc_dictionary_b[surface_b.id]```  

            - If surface is exterior residential, exterior non-residential, or semi-exterior, get baseline construction from Table G3.4-1 to G3.4-8 based on climate zone, surface conditioning category and surface type: ```if ( ( scc_b == "EXTERIOR RESIDENTIAL" ) OR ( scc_b == "EXTERIOR NON-RESIDENTIAL" ) OR ( scc_b == "SEMI-EXTERIOR" ) ): target_c_factor = data_lookup(table_G3_4, climate_zone, scc_b, "BELOW-GRADE WALL")```  

            - Else if surface is exterior mixed, get baseline construction for both residential and non-residential type below-grade wall: ```else if ( scc_b == "EXTERIOR MIXED" ): target_c_factor_res = data_lookup(table_G3_4, climate_zone, "EXTERIOR RESIDENTIAL", "BELOW-GRADE WALL"), target_c_factor_nonres = data_lookup(table_G3_4, climate_zone, "EXTERIOR NON-RESIDENTIAL", "BELOW-GRADE WALL")```  

              - If residential and non-residential type below-grade wall construction requirements are the same, save as baseline construction: ```if target_c_factor_res == target_c_factor_nonres: target_c_factor = target_c_factor_res```  

              - Else: ```manual_review_flag = TRUE```  

                **Rule Assertion:**  

                Case 1: If zone has both residential and non-residential spaces and the construction requirements for below-grade wall are different, request manual review: ```if manual_review_flag == TRUE: RAISE_WARNING```  

                Case 2: Else if below-grade wall C-factor matches Table G3.4: ```else if surface_construction_b.c_factor == target_c_factor: PASS```  

                Case 3: Else: ```else: FAIL```  

**Notes:**

1. Update Rule ID from 5-8 to 5-6 on 10/26/2023

**[Back](../_toc.md)**
