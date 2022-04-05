
## get_building_scc_skylight_roof_ratios

Description: This function would determine skylight and envelope roof ratios for a building for residential, non-residential, mixed and semi-heated surface conditioning categories.  

Inputs:

  - **RMR**: The RMR that needs to determine skylight and envelope roof ratios.  

Returns:

- **building_scc_skylight_roof_ratios_dictionary**: A dictionary that saves each surface conditioning category (residential, non-residential, mixed and semi-heated) with its skylight-roof-ratios for each building in RMR.

Function Call:

- get_surface_conditioning_category()
- get_opaque_surface_type()

Logic:

- Get surface conditioning category dictionary for RMR: `scc_dictionary = get_surface_conditioning_category(RMR)`

- For each zone in building: `zone in RMR.building...zones:`

  - For each surface in zone: `for surface in zone.surfaces:`

    - Check if surface is roof: `if ( get_opaque_surface_type(surface) == "ROOF" ):`

      - Check if roof is exterior residential type: `if scc_dictionary[surface.id] == ["EXTERIOR RESIDENTIAL"]:`

        - Add roof area to building total envelope residential type roof area: `total_res_roof_area += surface.area`

        - For each subsurface in surface: `for subsurface in surface.subsurfaces:`

          - Check if subsurface is door: `if subsurface.classification == "DOOR":`

            - If glazed area in door is more than 50% of the total door area, add door area to building total residential type skylight area: `if subsurface.glazed_area > subsurface.opaque_area: total_res_skylight_area += subsurface.glazed_area + subsurface.opaque_area`

          - Else, subsurface is not door, add total subsurface area to building total residential type skylight area: `total_res_skylight_area += subsurface.glazed_area + subsurface.opaque_area`

      - Else if roof is exterior non-residential type: `if scc_dictionary[surface.id] == ["EXTERIOR NON-RESIDENTIAL"]:`

        - Add roof area to building total envelope non-residential type roof area: `total_nonres_roof_area += surface.area`

        - For each subsurface in surface: `for subsurface in surface.subsurfaces:`

          - Check if subsurface is door: `if subsurface.classification == "DOOR":`

            - If glazed area in door is more than 50% of the total door area, add door area to building total non-residential type skylight area: `if subsurface.glazed_area > subsurface.opaque_area: total_nonres_skylight_area += subsurface.glazed_area + subsurface.opaque_area`

          - Else, subsurface is not door, add total subsurface area to building total non-residential type skylight area: `total_nonres_skylight_area += subsurface.glazed_area + subsurface.opaque_area`

      - Else if roof is exterior mixed type: `if scc_dictionary[surface.id] == ["EXTERIOR MIXED"]:`

        - Add roof area to building total envelope mixed type roof area: `total_mixed_roof_area += surface.area`

        - For each subsurface in surface: `for subsurface in surface.subsurfaces:`

          - Check if subsurface is door: `if subsurface.classification == "DOOR":`

            - If glazed area in door is more than 50% of the total door area, add door area to building total mixed type skylight area: `if subsurface.glazed_area > subsurface.opaque_area: total_mixed_skylight_area += subsurface.glazed_area + subsurface.opaque_area`

          - Else, subsurface is not door, add total subsurface area to building total mixed type skylight area: `total_mixed_skylight_area += subsurface.glazed_area + subsurface.opaque_area`

      - Else if roof is semi-heated type: `if scc_dictionary[surface.id] == ["SEMI-HEATED"]:`

        - Add roof area to building total envelope semi-heated type roof area: `total_semiheated_roof_area += surface.area`

        - For each subsurface in surface: `for subsurface in surface.subsurfaces:`

          - Check if subsurface is door: `if subsurface.classification == "DOOR":`

            - If glazed area in door is more than 50% of the total door area, add door area to building total semi-heated type skylight area: `if subsurface.glazed_area > subsurface.opaque_area: total_semiheated_skylight_area += subsurface.glazed_area + subsurface.opaque_area`

          - Else, subsurface is not door, add total subsurface area to building total semi-heated type skylight area: `total_semiheated_skylight_area += subsurface.glazed_area + subsurface.opaque_area`

- Calculate skylight roof ratio for residential type surface conditioning category: `if total_res_roof_area > 0: srr_res = total_res_skylight_area / total_res_roof_area; else: srr_res = 0`

- Calculate skylight roof ratio for non-residential type surface conditioning category: `if total_nonres_roof_area > 0: srr_nonres = total_nonres_skylight_area / total_nonres_roof_area; else: srr_nonres = 0`

- Calculate skylight roof ratio for mixed type surface conditioning category: `if total_mixed_roof_area > 0: srr_mixed = total_mixed_skylight_area / total_mixed_roof_area; else: srr_mixed = 0`

- Calculate skylight roof ratio for semi-heated type surface conditioning category: `if total_semiheated_roof_area > 0: srr_semiheated = total_semiheated_skylight_area / total_semiheated_roof_area; else: srr_semiheated = 0`

- Save skylight-roof-ratio of different surface conditioning categories for building: `building_scc_skylight_roof_ratios_dictionary[building.id] = {"EXTERIOR RESIDENTIAL": srr_res, "EXTERIOR NON-RESIDENTIAL": srr_nonres, "EXTERIOR MIXED": srr_mixed, "SEMI-EXTERIOR": srr_semiheated}`
[WX: I am not sure what is the usefulness of adding building.id in the dictionary as key]
**Returns** `return building_scc_skylight_roof_ratios_dictionary`

**[Back](../_toc.md)**
