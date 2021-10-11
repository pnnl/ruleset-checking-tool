
## get_scc_window_wall_ratios

Description: This function would determine window and envelope wall ratios for each area classification for vertical fenestration as per Table G3.1.1-1 for residential, non-residential and semi-heated surface categories.  

Inputs:

  - **RMR**: The RMR that needs to determine window and envelope wall ratios.  

Returns:

- **scc_window_wall_ratios_dictionary**: A dictionary that saves area classification with its the window and wall ratios for residential, non-residential and semi-heated surface categories.

Function Call:

- get_surface_conditioning_category()
- get_opaque_surface_type()

Logic:

- Get surface conditioning category dictionary for RMR: `scc_dictionary = get_surface_conditioning_category(RMR)`

- For each building segment in the model: `for building_segment in RMR.building.building_segments:`

  - Get building segment area classification used for vertical fenestration: `area_type = building_segment.area_type_vertical_fenestration`

  - For each zone in building segment: `zone in building_segment...zones:`

    - For each surface in zone: `for surface in zone.surfaces:`

      - Check if surface is above-grade wall: `if get_opaque_surface_type(surface) == "ABOVE-GRADE WALL" :`

        - Check if wall is exterior residential type: `if scc_dictionary[surface.id] == ["EXTERIOR RESIDENTIAL"]:`

          - Add wall area to total envelope residential type wall area under the current area classification: `scc_window_wall_area_dictionary[area_type]["RESIDENTIAL WALL"] += surface.area`

          - For each subsurface in wall, add total subsurface area to total residential type window area under the current area classification: `for subsurface in surface.subsurfaces: scc_window_wall_area_dictionary[area_type]["RESIDENTIAL WINDOW"] += subsurface.glazed_area + subsurface.opaque_area`

        - Else if wall is exterior non-residential type: `if scc_dictionary[surface.id] == ["EXTERIOR NON-RESIDENTIAL"]:`

          - Add wall area to total envelope non-residential type wall area under the current area classification: `scc_window_wall_area_dictionary[area_type]["NON-RESIDENTIAL WALL"] += surface.area`

          - For each subsurface in wall, add total subsurface area to total non-residential type window area under the current area classification: `for subsurface in surface.subsurfaces: scc_window_wall_area_dictionary[area_type]["NON-RESIDENTIAL WINDOW"] += subsurface.glazed_area + subsurface.opaque_area`

        - Else if wall is exterior mixed type: `if scc_dictionary[surface.id] == ["EXTERIOR MIXED"]:`

          - Add wall area to total envelope mixed type wall area under the current area classification: `scc_window_wall_area_dictionary[area_type]["MIXED WALL"] += surface.area`

          - For each subsurface in wall, add total subsurface area to total mixed type window area under the current area classification: `for subsurface in surface.subsurfaces: scc_window_wall_area_dictionary[area_type]["MIXED WINDOW"] += subsurface.glazed_area + subsurface.opaque_area`

        - Else if wall is semi-heated type: `if scc_dictionary[surface.id] == ["SEMI-HEATED"]:`

          - Add wall area to total envelope semi-heated type wall area under the current area classification: `scc_window_wall_area_dictionary[area_type]["SEMI-HEATED WALL"] += surface.area`

          - For each subsurface in wall, add total subsurface area to total semi-heated type window area under the current area classification: `for subsurface in surface.subsurfaces: scc_window_wall_area_dictionary[area_type]["SEMI-HEATED WINDOW"] += subsurface.glazed_area + subsurface.opaque_area`

- For each area type in scc_window_wall_area_dictionary: `for area_type in scc_window_wall_area_dictionary.keys():`

  - Calculate window wall ratio for residential type surface conditioning category: `if scc_window_wall_area_dictionary[area_type]["RESIDENTIAL WALL"] > 0: srr_res = scc_window_wall_area_dictionary[area_type]["RESIDENTIAL WINDOW"] / scc_window_wall_area_dictionary[area_type]["RESIDENTIAL WALL"]; else: srr_res = 0`

  - Calculate window wall ratio for non-residential type surface conditioning category: `if scc_window_wall_area_dictionary[area_type]["NON-RESIDENTIAL WALL"] > 0: srr_nonres = scc_window_wall_area_dictionary[area_type]["NON-RESIDENTIAL WINDOW"] / scc_window_wall_area_dictionary[area_type]["NON-RESIDENTIAL WALL"]; else: srr_nonres = 0`

  - Calculate window wall ratio for mixed type surface conditioning category: `if scc_window_wall_area_dictionary[area_type]["MIXED WALL"] > 0: srr_mixed = scc_window_wall_area_dictionary[area_type]["MIXED WINDOW"] / scc_window_wall_area_dictionary[area_type]["MIXED WALL"]; else: srr_mixed = 0`

  - Calculate window wall ratio for semi-heated type surface conditioning category: `if scc_window_wall_area_dictionary[area_type]["SEMI-HEATED WALL"] > 0: srr_semiheated = scc_window_wall_area_dictionary[area_type]["SEMI-HEATED WINDOW"] / scc_window_wall_area_dictionary[area_type]["SEMI-HEATED WALL"]; else: srr_semiheated = 0`

  - Save window-wall-ratio of different surface conditioning categories for area type: `scc_window_wall_ratios_dictionary[area_type] = {"EXTERIOR RESIDENTIAL": srr_res, "EXTERIOR NON-RESIDENTIAL": srr_nonres, "EXTERIOR MIXED": srr_mixed, "SEMI-EXTERIOR": srr_semiheated}`

**Returns** `return scc_window_wall_ratios_dictionary`

**[Back](../_toc.md)**
