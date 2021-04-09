
# Lighting - Rule 6-jl

**Rule ID:** 6-jl  
**Rule Description:** Spaces in proposed building with hardwired lighting, including Hotel/Motel Guest Rooms, Dormitory Living Quarters, Dwelling Units, ILP <= Table 9.6.1  
**Appendix G Section:** Lighting  
**Appendix G Section Reference:**  

- Table 9.6.1, Lighting Power Density Allowances Using the Space-by-Space Method and Minimum Control Requirements Using Either Method  

**Applicability:** All required data elements exist for P_RMR  
**Applicability Checks:**  

  1. Building has Hotel/Model Guestroom or Dormitory Living Quarters, Dwelling Units space types  

**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** Table 9.6.1  
## Rule Logic: 

- **Applicability Check 1:** Check if any Hotel/Model Guestroom or Dormitory Living Quarters, or Dwelling Units exist in the building segment in the Proposed model: ```For building_segment in P_RMR.building.building_segments:```  

  - Get thermal_block from building segment: ```thermal_block in building_segment.thermal_blocks:```

  - Get thermal_zone from thermal block: ```thermal_zone in thermal_block.thermal_zones:```

  - Get space from thermal zone: ```space in thermal_zone.spaces:```  

    - Get the space type of the space: ```space_type = space.space_type```  

    - If the space_type is "Guest Room", or "Dormitory Living Quarters", or "Dwelling Unit": ```if space_type == "Guest Room" or space_type == "Dormitory Living Quarters" or space_type == "Dwelling Unit"```  

      - Get the lighting power denstiy allowance: ```lighting_power_allowance = data_lookup(table_9_6_1, space_type)```

      - Get the total lighting power modeled in the space: ```space_lighting_power_proposed = space.lighting_power```  

      - Get the area of the space: ```floor_area_proposed = space.floor_area```  

      **Rule Assertion:** For each space: ```space_lighting_power_proposed <= floor_area_proposed * lighting_power_allowance```  
