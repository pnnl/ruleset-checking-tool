
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

  - Get lighting building area type for building segment: `lighting_building_area_type_p = building_segment_p.lighting_building_area_type`  

  - For each thermal block in building segment: `thermal_block_p in building_segment_p.thermal_blocks:`  

    - For each zone in thermal block: `zone_p in thermal_block_p.zones:`  

      - For each space in zone: `space_p in zone_p.spaces:`  

        - For each interior lighting in space: `interior_lighting_p in space_p.interior_lightings:`  

          **Rule Assertion:**  

          - Case 1: If lighting status type in space is not-yet designed, and interior lighting power density matches Table 9.5.1: `if ( space_lighting_status_type_dict[space.id] == "NOT-YET DESIGNED" ) and ( interior_lighting_p.power_per_area == data_lookup(table_9_5_1, lighting_building_area_type_p) ): PASS and raise_warning "LIGHTING NEITHER EXISTS OR IS SUBMITTED WITH DESIGN DOCUMENTS. LIGHTING POWER DENSITY IN P_RMR MATCHES TABLE 9.5.1."`  

          - Case 2:  Else if lighting status type in space is not-yet designed, and interior lighting power density does not match Table 9.5.1 : `else if ( space_lighting_status_type_dict[space.id] == "NOT-YET DESIGNED" ) and ( interior_lighting_p.power_per_area != data_lookup(table_9_5_1, lighting_building_area_type_p) ): FAIL and raise_warning "LIGHTING NEITHER EXISTS OR IS SUBMITTED WITH DESIGN DOCUMENTS. LIGHTING POWER DENSITY IN P_RMR DOES NOT MATCH TABLE 9.5.1."`  

          - Case 3: Else if lighting status type in space is as-designed or as-existing, and interior lighting power density in P_RMR matches U_RMR: `else if ( space_lighting_status_type_dict[space.id] == "AS-DESIGNED OR AS-EXISTING" ) and ( interior_lighting_p.power_per_area == match_data_element(U_RMR, InteriorLightings, interior_lighting_p.id).power_per_area ): PASS and raise_warning "LIGHTING EXISTS OR IS SUBMITTED WITH DESIGN DOCUMENTS. LIGHTING POWER DENSITY IN P_RMR MATCHES U_RMR"`  

          - Case 4: Else if lighting status type in space is as-designed or as-existing, and interior lighting power density in P_RMR does not match U_RMR: `else if ( space_lighting_status_type_dict[space.id] == "AS-DESIGNED OR AS-EXISTING" ) and ( interior_lighting_p.power_per_area != match_data_element(U_RMR, InteriorLightings, interior_lighting_p.id).power_per_area ): CAUTION and raise_warning "LIGHTING EXISTS OR IS SUBMITTED WITH DESIGN DOCUMENTS. LIGHTING POWER DENSITY IN P_RMR DOES NOT MATCH U_RMR."`  

