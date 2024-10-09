
## get_rmi_scc_skylight_roof_ratios

Description: This function would determine skylight and envelope roof ratios for a ruleset model instance for residential, non-residential, mixed and semi-heated surface conditioning categories.  

Inputs:

  - **RulesetModelInstance**: The ruleset model instance that needs to determine skylight and envelope roof ratios.  

Returns:

- **rmi_scc_skylight_roof_ratios_dictionary**: A dictionary that saves each surface conditioning category (residential, non-residential, mixed and semi-heated) with its skylight-roof-ratios for the input ruleset model instance, e.g. {"EXTERIOR RESIDENTIAL": 0.02, "EXTERIOR NON-RESIDENTIAL": 0.05, "EXTERIOR MIXED": 0.00, "SEMI-EXTERIOR": 0.00}.

Function Call:

- get_surface_conditioning_category()
- get_opaque_surface_type()

Logic:

- Get surface conditioning category dictionary for ruleset model instance: `scc_dictionary = get_surface_conditioning_category(RulesetModelInstance)`

- For each zone in ruleset model instance: `for zone in RulesetModelInstance...zones:`

  - For each surface in zone: `for surface in zone.surfaces:`

    - Check if surface is roof: `if ( get_opaque_surface_type(surface) == "ROOF" ):`

      - Check if roof is exterior residential type: `if scc_dictionary[surface.id] == ["EXTERIOR RESIDENTIAL"]:`

        - Add roof area to ruleset model instance total envelope residential type roof area: `total_res_roof_area += surface.area`

        - For each subsurface in surface: `for subsurface in surface.subsurfaces:`

          - Check if subsurface is door: `if subsurface.classification == "DOOR":`

            - If glazed area in door is more than 50% of the total door area, add door area to ruleset model instance total residential type skylight area: `if subsurface.glazed_area > subsurface.opaque_area: total_res_skylight_area += subsurface.glazed_area + subsurface.opaque_area`

          - Else, subsurface is not door, add total subsurface area to ruleset model instance total residential type skylight area: `total_res_skylight_area += subsurface.glazed_area + subsurface.opaque_area`

      - Else if roof is exterior non-residential type: `if scc_dictionary[surface.id] == ["EXTERIOR NON-RESIDENTIAL"]:`

        - Add roof area to ruleset model instance total envelope non-residential type roof area: `total_nonres_roof_area += surface.area`

        - For each subsurface in surface: `for subsurface in surface.subsurfaces:`

          - Check if subsurface is door: `if subsurface.classification == "DOOR":`

            - If glazed area in door is more than 50% of the total door area, add door area to ruleset model instance total non-residential type skylight area: `if subsurface.glazed_area > subsurface.opaque_area: total_nonres_skylight_area += subsurface.glazed_area + subsurface.opaque_area`

          - Else, subsurface is not door, add total subsurface area to ruleset model instance total non-residential type skylight area: `total_nonres_skylight_area += subsurface.glazed_area + subsurface.opaque_area`

      - Else if roof is exterior mixed type: `if scc_dictionary[surface.id] == ["EXTERIOR MIXED"]:`

        - Add roof area to ruleset model instance total envelope mixed type roof area: `total_mixed_roof_area += surface.area`

        - For each subsurface in surface: `for subsurface in surface.subsurfaces:`

          - Check if subsurface is door: `if subsurface.classification == "DOOR":`

            - If glazed area in door is more than 50% of the total door area, add door area to ruleset model instance total mixed type skylight area: `if subsurface.glazed_area > subsurface.opaque_area: total_mixed_skylight_area += subsurface.glazed_area + subsurface.opaque_area`

          - Else, subsurface is not door, add total subsurface area to ruleset model instance total mixed type skylight area: `total_mixed_skylight_area += subsurface.glazed_area + subsurface.opaque_area`

      - Else if roof is semi-heated type: `if scc_dictionary[surface.id] == ["SEMI-HEATED"]:`

        - Add roof area to ruleset model instance total envelope semi-heated type roof area: `total_semiheated_roof_area += surface.area`

        - For each subsurface in surface: `for subsurface in surface.subsurfaces:`

          - Check if subsurface is door: `if subsurface.classification == "DOOR":`

            - If glazed area in door is more than 50% of the total door area, add door area to ruleset model instance total semi-heated type skylight area: `if subsurface.glazed_area > subsurface.opaque_area: total_semiheated_skylight_area += subsurface.glazed_area + subsurface.opaque_area`

          - Else, subsurface is not door, add total subsurface area to ruleset model instance total semi-heated type skylight area: `total_semiheated_skylight_area += subsurface.glazed_area + subsurface.opaque_area`

- Calculate skylight roof ratio for residential type surface conditioning category: `if total_res_roof_area > 0: srr_res = total_res_skylight_area / total_res_roof_area; else: srr_res = 0`

- Calculate skylight roof ratio for non-residential type surface conditioning category: `if total_nonres_roof_area > 0: srr_nonres = total_nonres_skylight_area / total_nonres_roof_area; else: srr_nonres = 0`

- Calculate skylight roof ratio for mixed type surface conditioning category: `if total_mixed_roof_area > 0: srr_mixed = total_mixed_skylight_area / total_mixed_roof_area; else: srr_mixed = 0`

- Calculate skylight roof ratio for semi-heated type surface conditioning category: `if total_semiheated_roof_area > 0: srr_semiheated = total_semiheated_skylight_area / total_semiheated_roof_area; else: srr_semiheated = 0`

- Save skylight-roof-ratio of different surface conditioning categories for ruleset model instance: `rmi_scc_skylight_roof_ratios_dictionary = {"EXTERIOR RESIDENTIAL": srr_res, "EXTERIOR NON-RESIDENTIAL": srr_nonres, "EXTERIOR MIXED": srr_mixed, "SEMI-EXTERIOR": srr_semiheated}`
[WX: I am not sure what is the usefulness of adding building.id in the dictionary as key]

**Returns** `return rmi_scc_skylight_roof_ratios_dictionary`

**[Back](../_toc.md)**

**Notes:**

1. The skylight-roof ratios are calculated for each ruleset model instance and not for each building.
