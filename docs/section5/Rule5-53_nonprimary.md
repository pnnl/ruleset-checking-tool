# Envelope - Rule 5-53  
**Schema Version** 0.0.23
**Primary Rule** False
**Rule ID:** 5-53  
**Rule Description:** U-factor of the baseline door is based on Tables G3.4-1 through G3.4-8 for the applicable door type (swinging or non-swinging) and envelope conditioning category.
**Appendix G Section:** Section 5 Envelope  
**Appendix G Section Reference:** Section G3.1-5(b) Building Envelope Modeling Requirements for the Baseline model  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**
  1. The surface has an opaque door subsurface

**Evaluation Context:** Each Data Element  
**Data Lookup:** Tables G3.4-1 to G3.4-8  
**Function Call:**  

  1. get_surface_conditioning_category()

## Rule Logic:  

- Get building climate zone: ```climate_zone = B_RMR.weather.climate_zone```

- Get surface conditioning category dictionary for B_RMR: ```scc_dictionary_b = get_surface_conditioning_category(B_RMR)```

- For each building segment in the Proposed model: ```for building_segment_b in B_RMR.building.building_segments:```

  - For each zone in building_segment: ```for zone_b in building_segment_b.zones:```

    - For each surface in zone: ```for surface_b in zone_b.surfaces:```

      - Get surface conditioning category: ```scc_b = scc_dictionary_b[surface_b.id]```

      - For each subsurface in surface: ```for subsurface_b in surface_b.subsurfaces:```

        - Check if subsurface is opaque door: ```if ( subsurface_b.classification == "DOOR" ) AND ( subsurface_b.glazed_area < subsurface.opaque_area )```

          - Set rule applicability check to True: ```rule_applicability_check = TRUE```

          - Get subsurface subclassification: ```subclassification_b = subsurface_b.subclassification```

          - If surface is exterior residential, exterior non-residential, or semi-exterior, get baseline construction from Table G3.4-1 to G3.4-8 based on climate zone, surface conditioning category and door type: `if ( ( scc_b == "EXTERIOR RESIDENTIAL" ) OR ( scc_b == "EXTERIOR NON-RESIDENTIAL" ) OR ( scc_b == "SEMI-EXTERIOR" ) ): target_u_factor = data_lookup(table_G3_4, climate_zone, scc_b, "DOOR", subclassification_b)`

          - Else if surface is exterior mixed, get baseline construction for both residential and non-residential type door: ```else if ( scc_b == "EXTERIOR MIXED" ): target_u_factor_res = data_lookup(table_G3_4, climate_zone, "EXTERIOR RESIDENTIAL", "DOOR", subclassification_b), target_u_factor_nonres = data_lookup(table_G3_4, climate_zone, "EXTERIOR NON-RESIDENTIAL", "DOOR", subclassification_b)```

            - If residential and non-residential type door construction requirements are the same, save as baseline construction: ```if target_u_factor_res == target_u_factor_nonres: target_u_factor = target_u_factor_res```

            - Else, outcome is UNDETERMINED: ```manual_review_flag = TRUE```

            **Rule Assertion:**  

            - Case 1: For each opaque door, if the door's parent zone has both residential and non-residential spaces and the construction requirements for door are different, outcome is UNDETERMINED: ```if manual_review_flag == TRUE:
              outcome = UNDETERMINED and raise_message "ZONE HAS BOTH RESIDENTIAL AND NON-RESIDENTIAL TYPE SPACES AND THE REQUIREMENT FOR U-FACTOR FOR DOORS ARE DIFFERENT. VERIFY DOOR U-FACTOR IS MODELED CORRECTLY."```

            - Case 2: Else if door U-factor matches Table G3.4, outcome is PASS: ```else if subsurface_b.u_factor == target_u_factor: outcome = PASS```

            - Case 3: Else, outcome is FAIL: ```else: outcome = FAIL```

        - Case 4: If subsurface is not an opaque door, outcome is NOT_APPLICABLE: ```if NOT rule_applicability_check: outcome = NOT_APPLICABLE```

**[Back](../_toc.md)**
