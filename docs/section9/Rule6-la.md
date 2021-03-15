
# Lighting - Rule 6-la

**Rule ID:** 6-la  
**Rule Description:** Interior lighting level for spaces with plug in lighting not shown in design drawings, LPD shall be greater of as-designed or prescriptive values in Table 9.6.1. For the dwelling units, lighting power used in the simulation shall be equal to 0.60 W/ft2 or as designed, whichever is greater. (Note XC, as per the TCD this rule about just checking the dwellling unit?)  
**Appendix G Section:** Lighting  
**Appendix G Section Reference:**  

- Table 9.6.1, Lighting Power Density Allowances Using the Space-by-Space Method and Minimum Control Requirements Using Either Method  

**Applicability:** All required data elements exist for P_RMR  
**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** Table 9.6.1 (Note XC, or None if only checking dwelling unit?)  
**Determining Expected Value:**  

- Check if any dwelling units exist in the building segment in the Proposed model: ```For building_segment in P_RMR.building.building_segments:```  

  - Get thermal_block from building segment: ```thermal_block in building_segment.thermal_blocks:```

  - Get thermal_zone from thermal block: ```thermal_zone in thermal_block.thermal_zones:```

  - Get space from thermal zone: ```space in thermal_zone.spaces:```  

    - Get the space type of the space: ```space_type = space.space_type```  

    - If the space_type is "Dwelling Unit": ```if space_type == "Dwelling Unit"```  

      - Get the total lighting power modeled in the space: ```space_lighting_power_proposed = space.lighting_power```  

      - Get the area of the space: ```floor_area_proposed = space.floor_area```  

**Rule Assertion:** For each dwelling type space: ```space_lighting_power_proposed >= floor_area_proposed * 0.6```  
