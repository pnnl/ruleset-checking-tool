
## get_scc_skylight_roof_ratios

Description: This function would determine skylight and envelope roof ratios for a building segment for residential, non-residential and semi-heated surface categories.  

Inputs:

  - **RMR**: The RMR that needs to determine skylight and envelope roof ratios.  

Returns:

- **scc_skylight_roof_ratios_dictionary**: A dictionary that saves building segment ID with its the skylight and roof ratios for residential, non-residential and semi-heated surface categories.

Function Call:

- get_surface_conditioning_category()
- get_opaque_surface_type()

Logic:

- Get surface conditioning category dictionary for RMR: `scc_dictionary = get_surface_conditioning_category(RMR)`

- For each building segment in the model: `for building_segment in RMR.building.building_segments:`

  - For each zone in building segment: `zone in building_segment...zones:`

    - For each surface in zone: `for surface in zone.surfaces:`

      - Check if surface is roof: `if ( get_opaque_surface_type(surface) == "ROOF" ):`

        - Check if roof is exterior residential type: `if scc_dictionary[surface.id] == ["EXTERIOR RESIDENTIAL"]:`

          - Add roof area to building segment total envelope residential type roof area: `total_res_roof_area += surface.area`

          - For each subsurface in surface, add total subsurface area to building segment total residential type skylight area: `for subsurface in surface.subsurfaces: total_res_skylight_area += subsurface.glazed_area + subsurface.opaque_area`

        - Else if roof is exterior non-residential type: `if scc_dictionary[surface.id] == ["EXTERIOR NON-RESIDENTIAL"]:`

          - Add roof area to building segment total envelope non-residential type roof area: `total_nonres_roof_area += surface.area`

          - For each subsurface in surface, add total subsurface area to building segment total non-residential type skylight area: `for subsurface in surface.subsurfaces: total_nonres_skylight_area += subsurface.glazed_area + subsurface.opaque_area`

        - Else if roof is exterior mixed type: `if scc_dictionary[surface.id] == ["EXTERIOR MIXED"]:`

          - Add roof area to building segment total envelope mixed type roof area: `total_mixed_roof_area += surface.area`

          - For each subsurface in surface, add total subsurface area to building segment total mixed type skylight area: `for subsurface in surface.subsurfaces: total_mixed_skylight_area += subsurface.glazed_area + subsurface.opaque_area`

        - Else if roof is semi-heated type: `if scc_dictionary[surface.id] == ["SEMI-HEATED"]:`

          - Add roof area to building segment total envelope semi-heated type roof area: `total_semiheated_roof_area += surface.area`

          - For each subsurface in surface, add total subsurface area to building segment total semi-heated type skylight area: `for subsurface in surface.subsurfaces: total_semiheated_skylight_area += subsurface.glazed_area + subsurface.opaque_area`

  - Calculate skylight roof ratio for residential type surface conditioning category: `if total_res_roof_area > 0: srr_res = total_res_skylight_area / total_res_roof_area; else: srr_res = 0`

  - Calculate skylight roof ratio for non-residential type surface conditioning category: `if total_nonres_roof_area > 0: srr_nonres = total_nonres_skylight_area / total_nonres_roof_area; else: srr_nonres = 0`

  - Calculate skylight roof ratio for mixed type surface conditioning category: `if total_mixed_roof_area > 0: srr_mixed = total_mixed_skylight_area / total_mixed_roof_area; else: srr_mixed = 0`

  - Calculate skylight roof ratio for semi-heated type surface conditioning category: `if total_semiheated_roof_area > 0: srr_semiheated = total_semiheated_skylight_area / total_semiheated_roof_area; else: srr_semiheated = 0`

  - Save skylight-roof-ratio of different surface conditioning categories for building segment: `scc_skylight_roof_ratios_dictionary[building_segment.id] = {"EXTERIOR RESIDENTIAL": srr_res, "EXTERIOR NON-RESIDENTIAL": srr_nonres, "EXTERIOR MIXED": srr_mixed, "SEMI-EXTERIOR": srr_semiheated}`

**Returns** `return scc_skylight_roof_ratios_dictionary`

**[Back](../_toc.md)**
