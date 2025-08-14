
## get_building_segment_skylight_roof_areas

Description: This function would determine skylight and envelope roof area for a building segment.  

Inputs:

  - **RMR**: The RMR that needs to determine skylight and envelope roof area.  

Returns:

- **skylight_roof_areas_dictionary**: A dictionary that saves building segment ID with the total area of skylights and total area of all envelope roofs in the building segment.

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

          - If surface is roof and adjacent to the exterior: `if ( get_opaque_surface_type(surface) == "ROOF" ) AND ( scc_dictionary[surface.id] in ["EXTERIOR RESIDENTIAL", "EXTERIOR NON-RESIDENTIAL", "EXTERIOR MIXED", "SEMI-EXTERIOR"] ):`  

            - Add roof area to building segment total envelope roof area: `total_envelope_roof_area += surface.area`

            - For each subsurface in surface, add total subsurface area to building segment total skylight area: `for subsurface in surface.subsurfaces: total_skylight_area += subsurface.glazed_area + subsurface.opaque_area`  

  - Save total skylight area and total roof area of building segment: `skylight_roof_areas_dictionary[building_segment.id] = [total_skylight_area, total_envelope_roof_area]`

**Returns** `return skylight_roof_areas_dictionary`  

**[Back](../_toc.md)**
