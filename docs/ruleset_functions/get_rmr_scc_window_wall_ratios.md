
## get_rmr_scc_window_wall_ratios

Description: This function would determine window and envelope wall ratios for a RMR for residential, non-residential, mixed and semi-heated surface conditioning categories.  

Inputs:

  - **RMR**: The RMR that needs to determine window and envelope wall ratios.  

Returns:

- **rmr_scc_window_wall_ratios_dictionary**: A dictionary that saves each surface conditioning category (residential, non-residential, mixed and semi-exterior) with its window-wall-ratios for the input RMR, e.g. {"EXTERIOR RESIDENTIAL": 0.30, "EXTERIOR NON-RESIDENTIAL": 0.60, "EXTERIOR MIXED": 0.10, "SEMI-EXTERIOR": 0.00}.

Function Call:

- get_surface_conditioning_category()
- get_opaque_surface_type()

Logic:

- Get surface conditioning category dictionary for RMR: `scc_dictionary = get_surface_conditioning_category(RMR)`

- For each zone in RMR: `zone in RMR...zones:`

  - For each surface in zone: `for surface in zone.surfaces:`

    - Check if surface is above-grade wall: `if get_opaque_surface_type(surface) == "ABOVE-GRADE WALL" :`

      - Check if wall is exterior residential type: `if scc_dictionary[surface.id] == ["EXTERIOR RESIDENTIAL"]:`

        - Add wall area to RMR total envelope residential type wall area: `total_res_wall_area += surface.area`

        - For each subsurface in surface: `for subsurface in surface.subsurfaces:`

          - Check if subsurface is door: `if subsurface.classification == "DOOR":`

            - If glazed area in door is more than 50% of the total door area, add door area to RMR total residential type window area: `if subsurface.glazed_area > subsurface.opaque_area: total_res_window_area += subsurface.glazed_area + subsurface.opaque_area`

          - Else, subsurface is not door, add total subsurface area to RMR total residential type window area: `total_res_window_area += subsurface.glazed_area + subsurface.opaque_area`

      - Else if wall is exterior non-residential type: `if scc_dictionary[surface.id] == ["EXTERIOR NON-RESIDENTIAL"]:`

        - Add wall area to RMR total envelope non-residential type wall area: `total_nonres_wall_area += surface.area`

        - For each subsurface in surface: `for subsurface in surface.subsurfaces:`

          - Check if subsurface is door: `if subsurface.classification == "DOOR":`

            - If glazed area in door is more than 50% of the total door area, add door area to RMR total non-residential type window area: `if subsurface.glazed_area > subsurface.opaque_area: total_nonres_window_area += subsurface.glazed_area + subsurface.opaque_area`

          - Else, subsurface is not door, add total subsurface area to RMR total non-residential type window area: `total_nonres_window_area += subsurface.glazed_area + subsurface.opaque_area`

      - Else if wall is exterior mixed type: `if scc_dictionary[surface.id] == ["EXTERIOR MIXED"]:`

        - Add wall area to RMR total envelope mixed type wall area: `total_mixed_wall_area += surface.area`

        - For each subsurface in surface: `for subsurface in surface.subsurfaces:`

          - Check if subsurface is door: `if subsurface.classification == "DOOR":`

            - If glazed area in door is more than 50% of the total door area, add door area to RMR total mixed type window area: `if subsurface.glazed_area > subsurface.opaque_area: total_mixed_window_area += subsurface.glazed_area + subsurface.opaque_area`

          - Else, subsurface is not door, add total subsurface area to RMR total mixed type window area: `total_mixed_window_area += subsurface.glazed_area + subsurface.opaque_area`

      - Else if wall is semi-heated type: `if scc_dictionary[surface.id] == ["SEMI-EXTERIOR"]:`

        - Add wall area to RMR total envelope semi-heated type wall area: `total_semi_exterior_wall_area += surface.area`

        - For each subsurface in surface: `for subsurface in surface.subsurfaces:`

          - Check if subsurface is door: `if subsurface.classification == "DOOR":`

            - If glazed area in door is more than 50% of the total door area, add door area to R total semi-heated type window area: `if subsurface.glazed_area > subsurface.opaque_area: total_semi_exterior_window_area += subsurface.glazed_area + subsurface.opaque_area`

          - Else, subsurface is not door, add total subsurface area to RMR total semi-heated type window area: `total_semi_exterior_window_area += subsurface.glazed_area + subsurface.opaque_area`

- Calculate window wall ratio for residential type surface conditioning category: `if total_res_wall_area > 0: wwr_res = total_res_window_area / total_res_wall_area; else: wwr_res = 0`

- Calculate window wall ratio for non-residential type surface conditioning category: `if total_nonres_wall_area > 0: wrr_nonres = total_nonres_window_area / total_nonres_wall_area; else: wwr_nonres = 0`

- Calculate window wall ratio for mixed type surface conditioning category: `if total_mixed_wall_area > 0: wwr_mixed = total_mixed_window_area / total_mixed_wall_area; else: wwr_mixed = 0`

- Calculate window wall ratio for semi-exterior type surface conditioning category: `if total_semi_exterior_wall_area > 0: wwr_semi_exterior = total_semi_exterior_window_area / total_semi_exterior_wall_area; else: wwr_semi_exterior = 0`

- Save window-wall-ratio of different surface conditioning categories for RMR: `rmr_scc_window_wall_ratios_dictionary = {"EXTERIOR RESIDENTIAL": wwr_res, "EXTERIOR NON-RESIDENTIAL": wwr_nonres, "EXTERIOR MIXED": wwr_mixed, "SEMI-EXTERIOR": wwr_semi_exterior}`

**Returns** `return rmr_scc_window_wall_ratios_dictionary`

**[Back](../_toc.md)**
