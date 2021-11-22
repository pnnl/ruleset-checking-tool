
## get_building_scc_window_wall_ratios

Description: This function would determine window and envelope wall ratios for a building for residential, non-residential, mixed and semi-heated surface conditioning categories.  

Inputs:

  - **RMR**: The RMR that needs to determine window and envelope wall ratios.  

Returns:

- **building_scc_window_wall_ratios_dictionary**: A dictionary that saves each surface conditioning category (residential, non-residential, mixed and semi-heated) with its window-wall-ratios for each building in RMR.

Function Call:

- get_surface_conditioning_category()
- get_opaque_surface_type()

Logic:

- Get surface conditioning category dictionary for RMR: `scc_dictionary = get_surface_conditioning_category(RMR)`

- For each zone in building: `zone in RMR.building...zones:`

  - For each surface in zone: `for surface in zone.surfaces:`

    - Check if surface is above-grade wall: `if get_opaque_surface_type(surface) == "ABOVE-GRADE WALL" :`

      - Check if wall is exterior residential type: `if scc_dictionary[surface.id] == ["EXTERIOR RESIDENTIAL"]:`

        - Add wall area to building total envelope residential type wall area: `total_res_wall_area += surface.area`

        - For each subsurface in surface: `for subsurface in surface.subsurfaces:`

          - Check if subsurface is door: `if subsurface.classification == "DOOR":`

            - If glazed area in door is more than 50% of the total door area, add door area to building total residential type window area: `if subsurface.glazed_area > subsurface.opaque_area: total_res_window_area += subsurface.glazed_area + subsurface.opaque_area`

          - Else, subsurface is not door, add total subsurface area to building total residential type window area: `total_res_window_area += subsurface.glazed_area + subsurface.opaque_area`

      - Else if wall is exterior non-residential type: `if scc_dictionary[surface.id] == ["EXTERIOR NON-RESIDENTIAL"]:`

        - Add wall area to building total envelope non-residential type wall area: `total_nonres_wall_area += surface.area`

        - For each subsurface in surface: `for subsurface in surface.subsurfaces:`

          - Check if subsurface is door: `if subsurface.classification == "DOOR":`

            - If glazed area in door is more than 50% of the total door area, add door area to building total non-residential type window area: `if subsurface.glazed_area > subsurface.opaque_area: total_nonres_window_area += subsurface.glazed_area + subsurface.opaque_area`

          - Else, subsurface is not door, add total subsurface area to building total non-residential type window area: `total_nonres_window_area += subsurface.glazed_area + subsurface.opaque_area`

      - Else if wall is exterior mixed type: `if scc_dictionary[surface.id] == ["EXTERIOR MIXED"]:`

        - Add wall area to building total envelope mixed type wall area: `total_mixed_wall_area += surface.area`

        - For each subsurface in surface: `for subsurface in surface.subsurfaces:`

          - Check if subsurface is door: `if subsurface.classification == "DOOR":`

            - If glazed area in door is more than 50% of the total door area, add door area to building total mixed type window area: `if subsurface.glazed_area > subsurface.opaque_area: total_mixed_window_area += subsurface.glazed_area + subsurface.opaque_area`

          - Else, subsurface is not door, add total subsurface area to building total mixed type window area: `total_mixed_window_area += subsurface.glazed_area + subsurface.opaque_area`

      - Else if wall is semi-heated type: `if scc_dictionary[surface.id] == ["SEMI-HEATED"]:`

        - Add wall area to building total envelope semi-heated type wall area: `total_semiheated_wall_area += surface.area`

        - For each subsurface in surface: `for subsurface in surface.subsurfaces:`

          - Check if subsurface is door: `if subsurface.classification == "DOOR":`

            - If glazed area in door is more than 50% of the total door area, add door area to building total semi-heated type window area: `if subsurface.glazed_area > subsurface.opaque_area: total_semiheated_window_area += subsurface.glazed_area + subsurface.opaque_area`

          - Else, subsurface is not door, add total subsurface area to building total semi-heated type window area: `total_semiheated_window_area += subsurface.glazed_area + subsurface.opaque_area`

- Calculate window wall ratio for residential type surface conditioning category: `if total_res_wall_area > 0: wwr_res = total_res_window_area / total_res_wall_area; else: wwr_res = 0`

- Calculate window wall ratio for non-residential type surface conditioning category: `if total_nonres_wall_area > 0: wrr_nonres = total_nonres_window_area / total_nonres_wall_area; else: wwr_nonres = 0`

- Calculate window wall ratio for mixed type surface conditioning category: `if total_mixed_wall_area > 0: wwr_mixed = total_mixed_window_area / total_mixed_wall_area; else: wwr_mixed = 0`

- Calculate window wall ratio for semi-heated type surface conditioning category: `if total_semiheated_wall_area > 0: wwr_semiheated = total_semiheated_window_area / total_semiheated_wall_area; else: wwr_semiheated = 0`

- Save window-wall-ratio of different surface conditioning categories for building: `building_scc_window_wall_ratios_dictionary[building.id] = {"EXTERIOR RESIDENTIAL": wwr_res, "EXTERIOR NON-RESIDENTIAL": wwr_nonres, "EXTERIOR MIXED": wwr_mixed, "SEMI-EXTERIOR": wwr_semiheated}`

**Returns** `return building_scc_window_wall_ratios_dictionary`

**[Back](../_toc.md)**
