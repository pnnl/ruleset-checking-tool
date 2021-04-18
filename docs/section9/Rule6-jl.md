
# Lighting - Rule 6-jl

**Rule ID:** 6-jl  
**Rule Description:** Spaces in proposed building with hardwired lighting, including Hotel/Motel Guest Rooms, Dormitory Living Quarters, Dwelling Units, Interior Lighting Power <= Table 9.6.1; Baseline Interior Lighting Power Allowance for these spaces is determined based in Table G3.7  
**Appendix G Section:** Table G3.1 Part 6 Lighting under Proposed Building Performance paragraph (e)  
**Appendix G Section Reference:**  

- Table 9.6.1, Lighting Power Density Allowances Using the Space-by-Space Method and Minimum Control Requirements Using Either Method  
- Table G3.7, Performance Rating Method Lighting Power Density Allowances and Occupancy Sensor Reductions Using the Space-by-Space Method

**Applicability:** All required data elements exist for P_RMR  and B_RMR
**Applicability Checks:**  

  1. Building has Hotel/Model Guestroom or Dormitory Living Quarters, Dwelling Units space types  

**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** Table 9.6.1 and Table G3.7  
## Rule Logic: 

- **Applicability Check 1:** Check if any Hotel/Model Guestroom or Dormitory Living Quarters, or Dwelling Units exist in the building segment in the Proposed model: ```for building_segment_proposed in P_RMR.building.building_segments:```  

- For each thermal_block in building segment in the Proposed model: ```thermal_block_proposed in building_segment_proposed.thermal_blocks:```

- For each zone in thermal block: ```zone_proposed in thermal_block_proposed.zones:```

- For each space in zone: ```space_proposed in zone_proposed.spaces:```  

  - Check if lighting_space_type of the space is applicable: ```if ( space_proposed.lighting_space_type == "Guest Room" or "Dormitory Living Quarters" or "Dwelling Unit" ): lighting_power_allowance_proposed = space_proposed.lighting_space_type```  

    - If the lighting_space_type is "Guest Room", or "Dormitory Living Quarters": ```if ( lighting_space_type_proposed == "Guest Room" or "Dormitory Living Quarters" ):```  

      - Get the lighting power denstiy allowance for the proposed model: ```lighting_power_allowance_proposed = data_lookup(table_9_6_1, lighting_space_type_proposed)```  

    - If the lighting_space_type is "Dwelling Unit": ```else: lighting_power_allowance_proposed = 0.6```  

    - Get interior_lighting in space: ```interior_lighting_proposed = space_proposed.interior_lightings```  

      - Get the total design power_per_area for the space: ```space_lighting_power_per_area_proposed = sum( lighting.power_per_area for lighting in interior_lighting_proposed )```  

      **Rule Assertion:** For each space that is Hotel/Motel Guestroom or Dormitory Living Quarters, or Dwelling Unites in the proposed model: ```space_lighting_power_per_area_proposed <= lighting_power_allowance_proposed```  

    - Get matching space from Baseline RMR: ```space_baseline = match_data_element(B_RMR, spaces, space_proposed.name)```  

      - Get the lighting power denstiy allowance for the baseline model: ```lighting_power_allowance_baseline = data_lookup(table_G_3_7, lighting_space_type_proposed)```  

      - Get interior_lighting in space: ```interior_lighting_baseline = space_baseline.interior_lightings```  

      - Get the total baseline power_per_area for the space: ```space_lighting_power_per_area_baseline = sum( lighting.power_per_area for lighting in interior_lighting_baseline )```  

      **Rule Assertion:** For each space that is Hotel/Motel Guestroom or Dormitory Living Quarters, or Dwelling Unites in the baseline model: ```space_lighting_power_per_area_baseline == lighting_power_allowance_baseline```  
