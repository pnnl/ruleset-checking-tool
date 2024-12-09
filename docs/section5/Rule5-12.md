
# Envelope - Rule 5-12  

**Rule ID:** 5-12  
**Rule Description:** Baseline slab-on-grade floor assemblies must match the appropriate assembly maximum F-factors in Tables G3.4-1 through G3.4-9.  
**Rule Assertion:** Baseline RMD slab-on-grade floor: F_factor = expected value  
**Appendix G Section:** Section G3.1-5(b) Building Envelope Modeling Requirements for the Baseline building  
**Appendix G Section Reference:** Tables G3.4-1 to G3.4-8  

**Applicability:** All required data elements exist for B_RMD  
**Applicability Checks:** None  

**Manual Check:** Yes  
**Evaluation Context:** Each Data Element  
**Data Lookup:** Tables G3.4-1 to G3.4-8  
**Function Call:**  

  1. get_surface_conditioning_category()  
  2. get_opaque_surface_type()  

## Rule Logic:  

- Get building climate zone: `climate_zone = B_RMD.weather.climate_zone`  

- Get surface conditioning category dictionary for B_RMD: `scc_dictionary_b = get_surface_conditioning_category(B_RMD)`  

- For each building segment in the Baseline model: `for building_segment_b in B_RMD.building.building_segments:`  

  - For each thermal_block in building segment: `for thermal_block_b in building_segment_b.thermal_blocks:`  

    - For each zone in thermal block: `for zone_b in thermal_block_b.zones:`  

      - For each surface in zone: `for surface_b in zone_b.surfaces:`  

        - Check if surface is unheated slab-on-grade: `if get_opaque_surface_type(surface_b) == "UNHEATED SLAB-ON-GRADE":`  

          - Get surface construction: `surface_construction_b = surface_b.construction`  

          - Get surface conditioning category: `scc_b = scc_dictionary_b[surface_b.id]`  

            - If surface is exterior residential, exterior non-residential, or semi-exterior, get baseline construction from Table G3.4-1 to G3.4-8 based on climate zone, surface conditioning category and surface type: `if ( ( scc_b == "EXTERIOR RESIDENTIAL" ) OR ( scc_b == "EXTERIOR NON-RESIDENTIAL" ) OR ( scc_b == "SEMI-EXTERIOR" ) ): target_f_factor = data_lookup(table_G3_4, climate_zone, scc_b, "SLAB-ON-GRADE FLOOR")`  

            - Else if surface is exterior mixed, get baseline construction for both residential and non-residential type slab-on-grade floor: `else if ( scc_b == "EXTERIOR MIXED" ): target_f_factor_res = data_lookup(table_G3_4, climate_zone, "EXTERIOR RESIDENTIAL", "SLAB-ON-GRADE FLOOR"), target_f_factor_nonres = data_lookup(table_G3_4, climate_zone, "EXTERIOR NON-RESIDENTIAL", "SLAB-ON-GRADE FLOOR")`  

              - If residential and non-residential type slab-on-grade floor construction requirements are the same, save as baseline construction: `if target_f_factor_res == target_f_factor_nonres: target_f_factor = target_f_factor_res`  

              - Else: `manual_review_flag = TRUE`  

          **Rule Assertion:**  

          Case 1: If zone has both residential and non-residential spaces and the construction requirements for slab-on-grade floor are different, request manual review: `if manual_review_flag == TRUE: CAUTION and raise_warning "ZONE HAS BOTH RESIDENTIAL AND NON-RESIDENTIAL SPACES AND THE CONSTRUCTION REQUIREMENTS FOR SLAB-ON-GRADE FLOOR ARE DIFFERENT. VERIFY CONSTRUCTION IS MODELED CORRECTLY."`  

          Case 2: Else if slab-on-grade floor F-factor matches Table G3.4: `else if surface_construction_b.f_factor == target_f_factor: PASS`  
          
              - Conservative comparison less equal: ```if AHJ_RA_compare == True and surface_construction_b.f_factor <= target_f_factor: PASS```

          Case 3: Else: `else: FAIL and raise_warning: "BASELINE SLAB F-FACTOR IS NOT AS EXPECTED FOR SLABS THAT ARE LESS THAN 24" BELOW GRADE. VERIFY THAT THE SLAB IS MORE THAN 24" BELOW GRADE AND IS UNREGULATED."`  

**Notes:**

1. Update Rule ID from 5-15 to 5-12 on 10/26/2023

**[Back](../_toc.md)**
