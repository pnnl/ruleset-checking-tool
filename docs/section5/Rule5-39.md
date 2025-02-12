# Envelope - Rule 5-39  
**Schema Version** 0.0.23
**Primary Rule** True
**Rule ID:** 5-39  
**Rule Description:** U-factor of the baseline door is based on Tables G3.4-1 through G3.4-8 for the applicable door type (swinging or non-swinging) and envelope conditioning category.
**Appendix G Section:** Section 5 Envelope  
**Appendix G Section Reference:** Section G3.1-5(b) Building Envelope Modeling Requirements for the Baseline model  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:** Yes

**Evaluation Context:** Each Data Element  
**Data Lookup:** Tables G3.4-1 to G3.4-8  
**Function Call:**  

  1. get_more_stringent_surface_conditioning_category()

## Rule Logic:  

- Get building climate zone: ```climate_zone = B_RMR.weather.climate_zone```

- Get surface conditioning category dictionary for B_RMR: ```scc_dictionary_b = get_more_stringent_surface_conditioning_category(B_RMD, P_RMD)```

- For each building segment in the Proposed model: ```for building_segment_b in B_RMR.building.building_segments:```

  - For each zone in building_segment: ```for zone_b in building_segment_b.zones:```

    - For each surface in zone: ```for surface_b in zone_b.surfaces:```

      - Get surface conditioning category: ```scc_b = scc_dictionary_b[surface_b.id]```

      - Skip over unregulated surfaces: ```if (scc_b == "UNREGULATED"): continue```

      - For each subsurface in surface: ```for subsurface_b in surface_b.subsurfaces:```

        - Check if subsurface is opaque door: ```if ( subsurface_b.classification == "DOOR" ) AND ( subsurface_b.glazed_area <= subsurface.opaque_area )```

          - Get subsurface subclassification: ```subclassification_b = subsurface_b.subclassification```

          - If surface is exterior residential, exterior non-residential, or semi-exterior, and the subsurface classification is swinging or nonswinging, get baseline construction U-factor requirement from Table G3.4-1 to G3.4-8 based on climate zone, surface conditioning category, and door type: `if (scc_b in ["EXTERIOR RESIDENTIAL", "EXTERIOR NON-RESIDENTIAL", "SEMI-EXTERIOR"]) and (subclassification_b in ["SWINGING_DOOR", "NONSWINGING_DOOR"]): target_u_factor = data_lookup(table_G3_4, climate_zone, scc_b, "DOOR", subclassification_b)`

          - Else, (surface is exterior mixed, or subclassification is not swinging or nonswinging) create a list for all possible U-factor requirements: ```else: target_u_factor_options = []```

            - If subclassification is swinging or nonswinging (surface must be exterior mixed): append the residential and nonresidential U-factor requirements for the subclassification to the list of U-factor options: ```if (subclassification_b in ["SWINGING_DOOR", "NONSWINGING_DOOR"]): target_u_factor_options.extend([data_lookup(table_G3_4, climate_zone, "EXTERIOR RESIDENTIAL", "DOOR", subclassification_b), data_lookup(table_G3_4, climate_zone, "EXTERIOR NON-RESIDENTIAL", "DOOR", subclassification_b)])```

            - Else if surface is exterior residential, exterior non-residential, or semi-exterior: append the swinging and nonswinging U-factor requirements for the surface conditioning category to the list of U-factor options: ```else if (scc_b in ["EXTERIOR RESIDENTIAL", "EXTERIOR NON-RESIDENTIAL", "SEMI-EXTERIOR"]): target_u_factor_options.extend([data_lookup(table_G3_4, climate_zone, scc_b, "DOOR", "SWINGING_DOOR"), data_lookup(table_G3_4, climate_zone, scc_b, "DOOR", "NONSWINGING_DOOR")])```

            - Else, (surface is exterior mixed AND subclassification is not swinging or nonswinging): append the residential swinging, residential nonswinging, nonresidential swinging, and nonresidential nonswinging U-factor requirements to the list of U-factor options: ```else: target_u_factor_options.extend([data_lookup(table_G3_4, climate_zone, "EXTERIOR RESIDENTIAL", "DOOR", "SWINGING_DOOR"), data_lookup(table_G3_4, climate_zone, "EXTERIOR RESIDENTIAL", "DOOR", "NONSWINGING_DOOR"), data_lookup(table_G3_4, climate_zone, "EXTERIOR NON-RESIDENTIAL", "DOOR", "SWINGING_DOOR"), data_lookup(table_G3_4, climate_zone, "EXTERIOR NON-RESIDENTIAL", "DOOR", "NONSWINGING_DOOR")]```
            
            - If the options for door construction U-factor requirements are the same, save as the target U-factor: ```if (len(set(target_u_factor_options)) == 1): target_u_factor = target_u_factor_options[0]```
            
            - Else, flag for manual review, outcome will be UNDETERMINED or FAIL: ```manual_review_flag = TRUE```
            
            **Rule Assertion:**  
            
            - Case 1: If the door was flagged for manual review, and the baseline U-factor equals one of the target U-factor options; outcome is UNDETERMINED: ```if (manual_review_flag == TRUE) and (subsurface_b.u_factor in target_u_factor_options): outcome = UNDETERMINED and raise_message "PRESCRIBED U-FACTOR REQUIREMENT COULD NOT BE DETERMINED. VERIFY THE BASELINE DOOR U-FACTOR (${subsurface_b.u_factor}) IS MODELED CORRECTLY."```
            
            - Case 2: If the door was flagged for manual review, and the baseline U-factor does not equal any of the target U-factor options; outcome is FAIL: ```if (manual_review_flag == TRUE) and (subsurface_b.u_factor not in target_u_factor_options): outcome = FAIL```

            - Case 3: Else (door's parent zone consists entirely of residential or non-residential spaces, the subclassification is swinging or nonswinging, or the target U-factor options are all the same) if door U-factor matches Table G3.4, outcome is PASS: ```else if subsurface_b.u_factor == target_u_factor: outcome = PASS```

            - Case 4: Else, outcome is FAIL: ```else: outcome = FAIL```
              
              - If the baseline U-factor is lower than the expected value, raise message "RULE EVALUATION FAILS WITH A CONSERVATIVE OUTCOME": ```if (subsurface_b.u_factor < target_u_factor): raise_message: "RULE EVALUATION FAILS WITH A CONSERVATIVE OUTCOME"```

**Notes:**

1. Update Rule ID from 5-53 to 5-40 on 10/26/2023
2. Update Rule ID from 5-40 to 5-39 on 12/22/2023

**[Back](../_toc.md)**
