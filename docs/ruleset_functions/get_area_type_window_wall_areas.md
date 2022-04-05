
## get_area_type_window_wall_areas

Description: This function would determine fenestration and envelope above-grade wall areas for a building for each area type as per Table G3.1.1-1.  

Inputs:

- **RMR**: The RMR that needs to determine fenestration and envelope above-grade wall area.  

Returns:

- **window_wall_areas_dictionary**: A dictionary that saves each area type in a building as per Table G3.1.1-1 with its total fenestration and envelope above-grade wall areas, e.g. window_wall_areas_dictionary = {"AREA_TYPE_1": {"TOTAL_WALL_AREA": 1000, "TOTAL_WINDOW_AREA": 300}, "AREA_TYPE_2": {"TOTAL_WALL_AREA": 2000, "TOTAL_WINDOW_AREA": 100}}

Function Call:

- get_surface_conditioning_category()
- get_opaque_surface_type()

Logic:

- Get surface conditioning category dictionary for RMR: `scc_dictionary = get_surface_conditioning_category(RMR)`

- For each building segment in RMR: `for building_segment in RMR.building.building_segments:`

  - [WX: Remove this check]`Check if building segment area type is in Table G3.1.1-1`, get area type: `if building_segment.area_type_vertical_fenestration: area_type = building_segment.area_type_vertical_fenestration`

  - [WX: If area_type is Null,] set area type as NONE: `else: area_type = "NONE"` [WX: since there is 'OTHER' type, should we set it to this category? In Standard: OTHER shall be 40% WWR]

  - For each zone in building segment: `for zone in building_segment...zones:`

    - For each surface in zone: `for surface in zone.surfaces:`

      - If surface is above-grade wall and is part of exterior or semi-exterior building envelope: `if ( get_opaque_surface_type(surface) == "ABOVE-GRADE WALL" ) AND ( scc_dictionary[surface.id] in ["EXTERIOR RESIDENTIAL", "EXTERIOR NON-RESIDENTIAL", "EXTERIOR MIXED", "SEMI-EXTERIOR"] ):`

        - Add surface area to the total envelope above-grade wall area for current area type: `window_wall_areas_dictionary[area_type]["TOTAL_WALL_AREA"] += surface.area`

        - For each subsurface in surface: `for subsurface in surface.subsurfaces:`

          - Check if subsurface is door, and if the glazed vision area is more than 50% of the total area, add subsurface total area to total fenestration area for current area type: `if ( subsurface.classification == "DOOR" ) AND ( subsurface.glazed_area > subsurface.opaque_area ): window_wall_areas_dictionary[area_type]["TOTAL_WINDOW_AREA"] += subsurface.glazed_area + subsurface.opaque_area`

          - Else if subsurface is not door, add total subsurface area to building segment total fenestration area: `else if subsurface.classification != "DOOR" : window_wall_areas_dictionary[area_type]["TOTAL_WINDOW_AREA"] += subsurface.glazed_area + subsurface.opaque_area`

**Returns** `return window_wall_areas_dictionary`

**[Back](../_toc.md)**
