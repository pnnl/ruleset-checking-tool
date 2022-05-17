
## get_lighting_status_type

Description: This function would determine whether the space lighting status type is 1). not-yet designed or match Table 9_5_1, 2). as-designed or as-existing.  

Applicability: P_RMR Only

Inputs:
  - **building_segment**: The building segment that needs to determine lighting status type.  

Returns:
- **space_lighting_status_type**: The Lighting Status Type Category [not-yet designed or match Table_9_5_1, as-designed or as-existing].    

Data Lookup:
- Table 9.5.1  

Function Call: None

Logic:  

- Get lighting power density allowance for building segment: `allowable_LPD = data_lookup(table_9_5_1, building_segment.lighting_building_area_type)`   

  - For each zone in building segment: `zone in building_segment.zones:`  

    - For each space in zone: `space in zone.spaces:`  

      - Get total lighting power density in space: `total_space_LPD = sum(interior_lighting.power_per_area for interior_lighting in space.interior_lighting)`

      - If space total lighting power density equals to allowance, save space interior lighting as not-yet designed: `if total_space_LPD == allowable_LPD: space_lighting_status_type_dict[space.id] = "NOT-YET DESIGNED OR MATCH TABLE_9_5_1"`  

      - Else, save space interior lighting as as-designed or as-existing: `else: space_lighting_status_type_dict[space.id] = "AS-DESIGNED OR AS-EXISTING"`  

**Returns** `return space_lighting_status_type_dict`  

**Notes:**
  1. If building_segment.lighting_building_area_type is not specified, all space in building segment will be classified as "AS-DESIGNED OR AS-EXISTING".

**[Back](../_toc.md)**
