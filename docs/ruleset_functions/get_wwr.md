
Description: This function would determine window wall ratio for a building segment.  

Inputs:
  - **RMR**: The RMR that needs to determine window wall ratio.  

Returns:
- **window_wall_ratio**: The window wall ratio of the building segment.  

Function Call:

- get_zone_conditioning_category()
- get_surface_conditioning_category()
- get_opaque_surface_type()

Logic:

- Get zone conditioning category dictionary for RMR: `zcc_dictionary = get_zone_conditioning_category(RMR)`

- Get surface conditioning category dictionary for RMR: `scc_dictionary = get_surface_conditioning_category(RMR)`

- For each building segment in the model: `for building_segment in RMR.building.building_segments:`

  - For each thermal_block in building segment: `for thermal_block in building_segment.thermal_blocks:`

    - For each zone in thermal block: `zone in thermal_block.zones:`

      - Check if zone is conditioned or semi-heated: `if zcc_dictionary[zone.id] in [CONDITIONED RESIDENTIAL, CONDITIONED NON-RESIDENTIAL, CONDITIONED MIXED, SEMI-HEATED]`

        - For each surface in zone: `for surface in zone.surfaces:`

          - If surface is above-grade wall and adjacent to the exterior: `if ((get_opaque_surface_type(surface) == "ABOVE-GRADE WALL") AND (surface.adjacent_to == "EXTERIOR")):`  

            - For each subsurface in surface: `for subsurface in surface.subsurfaces:`  

              - If the glazed vision area is more than 50% of the total area, add glazed vision area to building segment total fenestration area: `if ( subsurface.glazed_area > ( subsurface.glazed_area + subsurface.opaque_area ) * 50% ): total_fenestration_area += subsurface.glazed_area + subsurface.opaque_area`  

      - For each surface in zone: `for surface in zone.surfaces:`

        - If surface is above-grade wall and is regulated: `if ((get_opaque_surface_type(surface) == "ABOVE-GRADE WALL") AND (scc_dictionary[surface.id] != "UNREGULATED")):`

          - Add to envelope total above-grade wall area: `total_envelope_wall_area += surface.area`

- Calculate WWR of the building segment: `window_wall_ratio = total_fenestration_area / total_envelope_wall_area`

**Returns** ```return window_wall_ratio```  

**[Back](../_toc.md)**

