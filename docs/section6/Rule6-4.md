
# Lighting - Rule 6-4

**Rule ID:** 6-4  
**Rule Description:** Where a complete lighting system exists, the actual lighting power for each thermal block shall be used in the model.  Where a lighting system has been designed and submitted with design documents, lighting power shall be determined in accordance with Sections 9.1.3 and 9.1.4. Where lighting neither exists nor is submitted with design documents, lighting shall comply with but not exceed the requirements of Section 9. Lighting power shall be determined in accordance with the Building Area Method (Section 9.5.1)

**Appendix G Section:** Section G3.1-6(a)(b)(c) Modeling Requirements for the Proposed Design  
**Appendix G Section Reference:** None  

**Applicability:** All required data elements exist for P_RMR  
**Applicability Checks:** None  
**Manual Check:** Yes

**Evaluation Context:** Each Data Element  
**Data Lookup:** Table 9.5.1  
**Function Call:**  

  - get_lighting_status_type()
  - match_data_element()

## Rule Logic: 

- For each building segment in the proposed model: `building_segment_p in P_RMR.building.building_segments:`  

  - Get lighting status type dictionary for building segment: `space_lighting_status_type_dict = get_lighting_status_type(building_segment_p)`  

  - For each thermal block in building segment: `thermal_block_p in building_segment_p.thermal_blocks:`  

    - For each zone in thermal block: `zone_p in thermal_block_p.zones:`  

      - For each space in zone: `space_p in zone_p.spaces:`  

        - Get total lighting power density in space: `total_space_LPD_p = sum(interior_lighting.power_per_area for interior_lighting in space_p.interior_lighting)`

        - Get matching space in U_RMR: `space_u = match_data_element(U_RMR, Spaces, space_p.id)`

          - Get total lighting power density in space in U_RMR: `total_space_LPD_u = sum(interior_lighting.power_per_area for interior_lighting in space_u.interior_lighting)`

        **Rule Assertion:**  

        - Case 1: If lighting status type in space is as-designed or as-existing, and interior lighting power density in P_RMR matches U_RMR: `if ( space_lighting_status_type_dict[space.id] == "AS-DESIGNED OR AS-EXISTING" ) and ( total_space_LPD_p == total_space_LPD_u ): PASS and raise_warning "LIGHTING EXISTS OR IS SUBMITTED WITH DESIGN DOCUMENTS. LIGHTING POWER DENSITY IN P_RMR MATCHES U_RMR"`

        - Case 2: Else if lighting status type in space is as-designed or as-existing, and interior lighting power density in P_RMR does not match U_RMR: `else if ( space_lighting_status_type_dict[space.id] == "AS-DESIGNED OR AS-EXISTING" ) and ( total_space_LPD_p != total_space_LPD_u ): CAUTION and raise_warning "LIGHTING EXISTS OR IS SUBMITTED WITH DESIGN DOCUMENTS. LIGHTING POWER DENSITY IN P_RMR DOES NOT MATCH U_RMR."`

        - Case 3: Else, lighting status type in space is not-yet designed or is as-designed or as-existing but matches Table 9.5.1. If interior lighting power density in P_RMR matches U_RMR: `else if total_space_LPD_p == total_space_LPD_u: PASS and raise_warning "LIGHTING IS NOT YET DESIGNED, OR LIGHTING IS AS-DESIGNED OR AS-EXISTING BUT MATCHES TABLE 9.5.1. LIGHTING POWER DENSITY IN P_RMR MATCHES U_RMR."`

        - Case 4: Else, interior lighting power density in P_RMR does not match U_RMR: `else: CAUTION and raise_warning "LIGHTING IS NOT YET DESIGNED, OR LIGHTING IS AS-DESIGNED OR AS-EXISTING BUT MATCHES TABLE 9.5.1. LIGHTING POWER DENSITY IN P_RMR DOES NOT MATCH U_RMR."`

