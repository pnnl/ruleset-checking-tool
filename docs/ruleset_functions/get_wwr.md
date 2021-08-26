
## get_overall_building_segment_wwr

Description: This function would determine window wall ratio for a building segment.  

Inputs:
  - **RMR**: The RMR that needs to determine window wall ratio.  

Returns:
- **building_wwr_dictionary**: A dictionary that saves window wall ratio for all building segments in building.  

Function Call:

- get_zone_conditioning_category()
- get_surface_conditioning_category()
- get_opaque_surface_type()

Logic:

- Get zone conditioning category dictionary for RMR: `zcc_dictionary = get_zone_conditioning_category(RMR)`

- Get surface conditioning category dictionary for RMR: `scc_dictionary = get_surface_conditioning_category(RMR)`

- For each building segment in the model: `for building_segment in RMR.building.building_segments:`

  - For each thermal block in building segment: `for thermal_block in building_segment.thermal_blocks:`

    - For each zone in thermal block: `zone in thermal_block.zones:`

      - Check if zone is conditioned or semi-heated: `if zcc_dictionary[zone.id] in ["CONDITIONED RESIDENTIAL", "CONDITIONED NON-RESIDENTIAL“, ”CONDITIONED MIXED", "SEMI-HEATED"]:`

        - For each surface in zone: `for surface in zone.surfaces:`

          - If surface is above-grade wall and adjacent to the exterior: `if ( get_opaque_surface_type(surface) == "ABOVE-GRADE WALL" ) AND ( scc_dictionary[surface.id] in ["EXTERIOR RESIDENTIAL", "EXTERIOR NON-RESIDENTIAL", "EXTERIOR MIXED", "SEMI-EXTERIOR"] ):`  

            - Add surface area to building segment total envelope above-grade wall area: `total_envelope_wall_area += surface.area`

            - For each subsurface in surface: `for subsurface in surface.subsurfaces:`  

              - Check if subsurface is door, and if the glazed vision area is more than 50% of the total area, add subsurface total area to building segment total fenestration area: `if ( subsurface.classification == "DOOR" ) AND ( subsurface.glazed_area > ( subsurface.glazed_area + subsurface.opaque_area ) * 50% ): total_fenestration_area += subsurface.glazed_area + subsurface.opaque_area`  

              - Else if subsurface is not door, add total subsurface area to building segment total fenestration area: `else if subsurface.classification != "DOOR" : total_fenestration_area += subsurface.glazed_area + subsurface.opaque_area`

  - Calculate and save WWR of building segment: `building_wwr_dictionary[building_segment.id] = total_fenestration_area / total_envelope_wall_area`

**Returns** `return building_wwr_dictionary`  

**[Back](../_toc.md)**
