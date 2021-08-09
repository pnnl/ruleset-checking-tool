
## get_lighting_status_type

Description: This function would determine whether the space lighting status type is not-yet designed, as-designed or as-existing.  

Inputs:
  - **building_segment**: The building segment that needs to determine lighting status type.  

Returns:
- **space_lighting_status_type**: The Lighting Status Type Category [not-yet designed, as-designed or as-existing].    

Data Lookup:
- Table 9.5.1  

Function Call: None  

Logic:  

- Get lighting power density allowance for building segment: `allowable_LPD = data_lookup(table_9_5_1, building_segment.lighting_building_area_type)`  

- For each thermal block in building segment: `thermal_block in building_segment.thermal_blocks:`  

  - For each zone in thermal block: `zone in thermal_block.zones:`  

    - For each space in zone: `space in zone.spaces:`  

      - If space lighting power density equals to allowance, save space interior lighting as not-yet designed: `if space.interior_lighting.power_per_area == allowable_LPD: space_lighting_status_type_dict[space.id] = "NOT-YET DESIGNED"`  

      - Else, save space interior lighting as as-designed or as-existing: `else: space_lighting_status_type_dict[space.id] = "AS-DESIGNED OR AS-EXISTING"`  

**Returns** `return space_lighting_status_type_dict`  
