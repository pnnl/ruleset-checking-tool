
# Lighting - Rule 6-jb

**Rule ID:** 6-jb  
**Rule Description:** For the proposed building, each space has the same lighting power as the corresponding space in the U-RMR  
**Appendix G Section:** Lighting  
**Appendix G Section Reference:** None

**Applicability:** All required data elements exist for U_RMR and P_RMR  
**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  
**Determining Expected Value:**  

- Calculate the total lighting power for each space under each building segment in the User RMR: ```For building_segment in U_RMR.building.building_segments:``` (Note XC, right now in the schema, interior lighting is independent of the space it is in. It is only related to space type. Hard to calculate the lighting power for each space.)

  - Get thermal_block from building segment: ```thermal_block in building_segment.thermal_blocks:```

  - Get thermal_zone from thermal block: ```thermal_zone in thermal_block.thermal_zones:```

  - Get space from thermal zone: ```space in thermal_zone.spaces:```

  - Get the total lighting power for each space: ```space_lighting_power_user = space.lighting_power``` (Note XC, depending on how rmr reports the lighting power for each space, e.g. report fixtures, or report total wattage, this needs to be adjusted.)

- Calculate the total lighting power for each space under each building segment in the Proposed RMR: ```For building_segment in P_RMR.building.building_segments:```

  - Get thermal_block from building segment: ```thermal_block in building_segment.thermal_blocks:```

  - Get thermal_zone from thermal block: ```thermal_zone in thermal_block.thermal_zones:```

  - Get space from thermal zone: ```space in thermal_zone.spaces:```

  - Get the total lighting power for each space: ```space_lighting_power_proposed = space.lighting_power```

**Rule Assertion:** The total lighting power in each space for U_RMR and P_RMR are the same: ```space_lighting_power_user = space_lighting_power_proposed```