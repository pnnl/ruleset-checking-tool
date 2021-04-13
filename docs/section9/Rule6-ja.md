
# Lighting - Rule 6-ja

**Rule ID:** 6-ja  
**Rule Description:** The total building interior lighting power shall not exceed the interior lighting power allowance determined using either Table G3.7 or G3.8.  
**Appendix G Section:** Section G1.2.1(b) Mandatory Provisions related to interior lighting power
  
**Appendix G Section Reference:**  

- Table G3.7, Performance Rating Method Lighting Power Density Allowances and Occupancy Sensor Reductions Using the Space-by-Space Method
- Table G3.8, Performance Rating Method Lighting Power Densities Using the Building Area Method  

**Applicability:** All required data elements exist for P_RMR  
**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** Table G3.7 and Table G3.8  
## Rule Logic: 

- Get the building area lighting area type of the building segment in the Proposed model: ```building_light_area_type = building_segment.lighting_building_area_type``` (Note XC, assuming this field lists values from T-9.5.1 or T-G3.8, for "Building Area Method", or "None" if the building goes for "Space-by-Space Method")

- Get thermal_block from building segment: ```thermal_block in building_segment.thermal_blocks:```

- Get thermal_zone from thermal block: ```thermal_zone in thermal_block.zones:```

- Get space from thermal zone: ```space in thermal_zone.spaces:```

- Get floor_area from space: ```space_floor_area = space.floor_area```

  - If building_light_area_type is in Table G3.8 then add floor_area to the total building floor area: ```total_building_area.append(space_floor_area)```

    - Get the allowable lighting power density for this building area type: ```if building_light_area_type in table_G3_8: allowable_LPD = data_lookup(table_G3_8, building_light_area_type) else raise_warning```

    - Calculate the building total allowable lighting wattage: ```building_allowable_lighting_wattage = allowable_LPD * total_building_area```

  - If building_light_area_type is "None", get space_lighting_type: (Note XC, there is currently no space lighting type for spaces as per Table G3.7. This is needed to determine the basis for the Baseline lighting power allowance) ```space_type_lighting = space.space_lighting_type```

    - If space_type_lighting exists in Table G3.7 then get the allowable lighting power density for this space type: ```if space_lighting_type in table_G3_7: allowable_LPD = data_lookup(table_G3_7, space_type_lighting) else raise_warning```

    - Calculate the building total allowable lighting wattage: ```building_allowable_lighting_wattage.append(allowable_LPD * space_floor_area)```

- Calculate the total lighting power for in the Proposed model: ```For interior_lighting in P_RMR.interior_lightings: building_designed_lighting_wattage.append(interior_lighting.power)```

**Rule Assertion:** For each Proposed building_segment: ```building_designed_lighting_wattage <= building_allowable_lighting_wattage```
