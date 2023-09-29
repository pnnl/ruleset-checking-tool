
## get_rmi_scc_window_wall_ratios

Description: This function would determine window and envelope wall ratios for a ruleset model instance for residential, non-residential, mixed and semi-heated surface conditioning categories.  

Inputs:

  - **RulesetModelInstance**: The ruleset model instance that needs to determine window and envelope wall ratios.  

Returns:

- **rmi_scc_window_wall_ratios_dictionary**: A dictionary that saves each surface conditioning category (residential, non-residential, mixed and semi-exterior) with its window-wall-ratios for the input ruleset model instance, e.g. {"EXTERIOR RESIDENTIAL": 0.30, "EXTERIOR NON-RESIDENTIAL": 0.60, "EXTERIOR MIXED": 0.10, "SEMI-EXTERIOR": 0.00}.

Function Call:

- get_surface_conditioning_category()
- get_opaque_surface_type()

Logic:

- Get surface conditioning category dictionary for ruleset model instance: `scc_dictionary = get_surface_conditioning_category(RulesetModelInstance)`

- For each zone in ruleset model instance: `zone in RulesetModelInstance...zones:`

  - For each surface in zone: `for surface in zone.surfaces:`

    - Check if surface is above-grade wall: `if get_opaque_surface_type(surface) == "ABOVE-GRADE WALL" :`

      - Check if wall is exterior residential type: `if scc_dictionary[surface.id] == ["EXTERIOR RESIDENTIAL"]:`

        - Add wall area to ruleset model instance total envelope residential type wall area: `total_res_wall_area += surface.area`

        - For each subsurface in surface: `for subsurface in surface.subsurfaces:`

          - Check if subsurface is door: `if subsurface.classification == "DOOR":`

            - If glazed area in door is more than 50% of the total door area, add door area to ruleset model instance total residential type window area: `if subsurface.glazed_area > subsurface.opaque_area: total_res_window_area += subsurface.glazed_area + subsurface.opaque_area`

          - Else, subsurface is not door, add total subsurface area to ruleset model instance total residential type window area: `total_res_window_area += subsurface.glazed_area + subsurface.opaque_area`

      - Else if wall is exterior non-residential type: `if scc_dictionary[surface.id] == ["EXTERIOR NON-RESIDENTIAL"]:`

        - Add wall area to ruleset model instance total envelope non-residential type wall area: `total_nonres_wall_area += surface.area`

        - For each subsurface in surface: `for subsurface in surface.subsurfaces:`

          - Check if subsurface is door: `if subsurface.classification == "DOOR":`

            - If glazed area in door is more than 50% of the total door area, add door area to ruleset model instance total non-residential type window area: `if subsurface.glazed_area > subsurface.opaque_area: total_nonres_window_area += subsurface.glazed_area + subsurface.opaque_area`

          - Else, subsurface is not door, add total subsurface area to ruleset model instance total non-residential type window area: `total_nonres_window_area += subsurface.glazed_area + subsurface.opaque_area`

      - Else if wall is exterior mixed type: `if scc_dictionary[surface.id] == ["EXTERIOR MIXED"]:`

        - Add wall area to ruleset model instance total envelope mixed type wall area: `total_mixed_wall_area += surface.area`

        - For each subsurface in surface: `for subsurface in surface.subsurfaces:`

          - Check if subsurface is door: `if subsurface.classification == "DOOR":`

            - If glazed area in door is more than 50% of the total door area, add door area to ruleset model instance total mixed type window area: `if subsurface.glazed_area > subsurface.opaque_area: total_mixed_window_area += subsurface.glazed_area + subsurface.opaque_area`

          - Else, subsurface is not door, add total subsurface area to ruleset model instance total mixed type window area: `total_mixed_window_area += subsurface.glazed_area + subsurface.opaque_area`

      - Else if wall is semi-heated type: `if scc_dictionary[surface.id] == ["SEMI-EXTERIOR"]:`

        - Add wall area to ruleset model instance total envelope semi-heated type wall area: `total_semi_exterior_wall_area += surface.area`

        - For each subsurface in surface: `for subsurface in surface.subsurfaces:`

          - Check if subsurface is door: `if subsurface.classification == "DOOR":`

            - If glazed area in door is more than 50% of the total door area, add door area to R total semi-heated type window area: `if subsurface.glazed_area > subsurface.opaque_area: total_semi_exterior_window_area += subsurface.glazed_area + subsurface.opaque_area`

          - Else, subsurface is not door, add total subsurface area to ruleset model instance total semi-heated type window area: `total_semi_exterior_window_area += subsurface.glazed_area + subsurface.opaque_area`

- Calculate window wall ratio for residential type surface conditioning category: `if total_res_wall_area > 0: wwr_res = total_res_window_area / total_res_wall_area; else: wwr_res = 0`

- Calculate window wall ratio for non-residential type surface conditioning category: `if total_nonres_wall_area > 0: wrr_nonres = total_nonres_window_area / total_nonres_wall_area; else: wwr_nonres = 0`

- Calculate window wall ratio for mixed type surface conditioning category: `if total_mixed_wall_area > 0: wwr_mixed = total_mixed_window_area / total_mixed_wall_area; else: wwr_mixed = 0`

- Calculate window wall ratio for semi-exterior type surface conditioning category: `if total_semi_exterior_wall_area > 0: wwr_semi_exterior = total_semi_exterior_window_area / total_semi_exterior_wall_area; else: wwr_semi_exterior = 0`

- Save window-wall-ratio of different surface conditioning categories for ruleset model instance: `rmi_scc_window_wall_ratios_dictionary = {"EXTERIOR RESIDENTIAL": wwr_res, "EXTERIOR NON-RESIDENTIAL": wwr_nonres, "EXTERIOR MIXED": wwr_mixed, "SEMI-EXTERIOR": wwr_semi_exterior}`

**Returns** `return rmi_scc_window_wall_ratios_dictionary`

**[Back](../_toc.md)**

**Notes:**

1. Potential future change to return area for each surface conditioning category instead of percentages. See notes in RDS Rule 5-26.md for details.
