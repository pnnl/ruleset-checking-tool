
## get_surface_conditioning_category
**Schema Version:** 0.0.23
Description: This function would cycle through each surface in  a zone and categorize it as exterior res, exterior non res, exterior mixed, semi-exterior or unregulated.  

Inputs:

  - **RMR**: The RMR that needs to determine surface conditioning category.  

Returns:

  - **surface_conditioning_category**: The Surface Conditioning Category [exterior residential, exterior non-residential, exterior mixed, semi-exterior, unregulated].  

Logic:  

- Get zone conditioning category dictionary for the RMR: `zone_conditioning_category_dict = get_zone_conditioning_category(RMR)`  

- For each building segment in the RMR: `for building_segment in RMR.building.building_segments:`  

  - For each zone in building segement: `for zone in building_segment.zones:`  

    - If zone is residential and conditioned: `if zone_conditioning_category_dict[zone.id] == "CONDITIONED RESIDENTIAL":`  

      - For each surface in zone: `for surface in zone.surfaces:`  

        - If surface adjacency is exterior, ground or if surface adjacency is interior and the adjacent zone is unenclosed, surface is classified as exterior residential type: `if ( surface.adjacent_to == EXTERIOR ) OR ( surface.adjacent_to == GROUND ) OR ( ( surface.adjacent_to == INTERIOR ) AND ( zone_conditioning_category_dict[surface.adjacent_zone_id] == "UNENCLOSED" ) ): surface_conditioning_category_dict[surface.id] = "EXTERIOR RESIDENTIAL"`  

        - Else if surface adjacency is interior and the adjacent zone is semi-heated or unconditioned, surface is classified as semi-exterior: `else if ( surface.adjacent_to == INTERIOR ) AND ( ( zone_conditioning_category_dict[surface.adjacent_zone_id] == "SEMI-HEATED" ) OR ( zone_conditioning_category_dict[surface.adjacent_zone_id] == "UNCONDITIONED" ) ): surface_conditioning_category_dict[surface.id] = "SEMI-EXTERIOR"`  

        - Else, surface is unregulated: `else: surface_conditioning_category_dict[surface.id] = "UNREGULATED"`  

    - Else if zone is non-residential and conditioned: `else if zone_conditioning_category_dict[zone.id] == "CONDITIONED NONRESIDENTIAL":`  

      - For each surface in zone: `for surface in zone.surfaces:`  

        - If surface adjacency is exterior, ground or if surface adjacency is interior and the adjacent zone is unenclosed, surface is classified as exterior non-residential type: `if ( surface.adjacent_to == EXTERIOR ) OR ( surface.adjacent_to == GROUND ) OR ( ( surface.adjacent_to == INTERIOR ) AND ( zone_conditioning_category_dict[surface.adjacent_zone_id] == "UNENCLOSED" ) ): surface_conditioning_category_dict[surface.id] = "EXTERIOR NON-RESIDENTIAL"`  

        - Else if surface adjacency is interior and the adjacent zone is semi-heated or unconditioned, surface is classified as semi-exterior: `else if ( surface.adjacent_to == INTERIOR ) AND ( ( zone_conditioning_category_dict[surface.adjacent_zone_id] == "SEMI-HEATED" ) OR ( zone_conditioning_category_dict[surface.adjacent_zone_id] == "UNCONDITIONED" ) ): surface_conditioning_category_dict[surface.id] = "SEMI-EXTERIOR"`  

        - Else, surface is unregulated: `else: surface_conditioning_category_dict[surface.id] = "UNREGULATED"`  

    - Else if zone is mixed and conditioned: `else if zone_conditioning_category_dict[zone.id] == "CONDITIONED MIXED":`  

      - For each surface in zone: `for surface in zone.surfaces:`  

        - If surface adjacency is exterior, ground or if surface adjacency is interior and the adjacent zone is unenclosed, surface is classified as exterior mixed type: `if ( surface.adjacent_to == EXTERIOR ) OR ( surface.adjacent_to == GROUND ) OR ( ( surface.adjacent_to == INTERIOR ) AND ( zone_conditioning_category_dict[surface.adjacent_zone_id] == "UNENCLOSED" ) ): surface_conditioning_category_dict[surface.id] = "EXTERIOR MIXED"`  

        - Else if surface adjacency is interior and the adjacent zone is semi-heated or unconditioned, surface is classified as semi-exterior: `else if ( surface.adjacent_to == INTERIOR ) AND ( ( zone_conditioning_category_dict[surface.adjacent_zone_id] == "SEMI-HEATED" ) OR ( zone_conditioning_category_dict[surface.adjacent_zone_id] == "UNCONDITIONED" ) ): surface_conditioning_category_dict[surface.id] = "SEMI-EXTERIOR"`  

        - Else, surface is unregulated: `else: surface_conditioning_category_dict[surface.id] = "UNREGULATED"`  

    - Else if zone is semi-heated: `else if zone_conditioning_category_dict[zone.id] == "SEMI-HEATED":`  

      - For each surface in zone: `for surface in zone.surfaces:`  

        - If surface adjacency is exterior, ground, or if surface adjacency is interior and the adjacent zone is conditioned, unenclosed or unconditioned, surface is classified as semi-exterior: `if ( surface.adjacent_to == EXTERIOR ) OR ( surface.adjacent_to == GROUND ) OR ( ( surface.adjacent_to == INTERIOR ) AND ( ( zone_conditioning_category_dict[surface.adjacent_zone_id] == "CONDITIONED RESIDENTIAL" ) OR ( zone_conditioning_category_dict[surface.adjacent_zone_id] == "CONDITIONED NON-RESIDENTIAL" ) OR ( zone_conditioning_category_dict[surface.adjacent_zone_id] == "CONDITIONED MIXED" ) OR ( zone_conditioning_category_dict[surface.adjacent_zone_id] == "UNENCLOSED" ) OR ( zone_conditioning_category_dict[surface.adjacent_zone_id] == "UNCONDITIONED" ) ): surface_conditioning_category_dict[surface.id] = "SEMI-EXTERIOR"`  

        - Else, surface is classified as unregulated: `else: surface_conditioning_category_dict[surface.id] = "UNREGULATED"`  

    - Else if zone is unenclosed: `else if zone_conditioning_category_dict[zone.id] == "UNENCLOSED":`  

      - For each surface in zone: `for surface in zone.surfaces:`  

        - If surface adjacency is interior and the adjacent zone is residential and conditioned, surface is classified as exterior residential: `else if ( surface.adjacent_to == INTERIOR ) AND ( zone_conditioning_category_dict[surface.adjacent_zone_id] == "CONDITIONED RESIDENTIAL" ): surface_conditioning_category_dict[surface.id] = "EXTERIOR RESIDENTIAL"`  

        - Else if surface adjacency is interior and the adjacent zone is non-residential and conditioned, surface is classified as exterior non-residential: `else if ( surface.adjacent_to == INTERIOR ) AND ( zone_conditioning_category_dict[surface.adjacent_zone_id] == "CONDITIONED NON-RESIDENTIAL" ): surface_conditioning_category_dict[surface.id] = "EXTERIOR NON-RESIDENTIAL"`  

        - Else if surface adjacency is interior and the adjacent zone is mixed and conditioned, surface is classified as exterior mixed: `else if ( surface.adjacent_to == INTERIOR ) AND ( zone_conditioning_category_dict[surface.adjacent_zone_id] == "CONDITIONED MIXED" ): surface_conditioning_category_dict[surface.id] = "EXTERIOR MIXED"`  

        - Else if surface adjacency is interior and the adjacent zone is semi-heated, surface is classified as semi-exterior: `else if ( surface.adjacent_to == INTERIOR ) AND ( zone_conditioning_category_dict[surface.adjacent_zone_id] == "SEMI-HEATED" ): surface_conditioning_category_dict[surface.id] = "SEMI-EXTERIOR"`  

        - Else, surface is classified as unregulated: `else: surface_conditioning_category_dict[surface.id] = "UNREGULATED"`  

    - Else, zone is unconditioned: `else:`  

      - For each surface in zone:  `for surface in zone.surfaces:`  

        - If surface adjacency is interior and the adjacent zone is conditioned or semi-heated, surface is classified as semi-exterior: `if ( surface.adjacent_to == INTERIOR ) AND ( ( zone_conditioning_category_dict[surface.adjacent_zone_id] == "CONDITIONED RESIDENTIAL" ) OR ( zone_conditioning_category_dict[surface.adjacent_zone_id] == "CONDITIONED NON-RESIDENTIAL" ) OR ( zone_conditioning_category_dict[surface.adjacent_zone_id] == "CONDITIONED MIXED" ) OR ( zone_conditioning_category_dict[surface.adjacent_zone_id] == "SEMI-HEATED" ) ): surface_conditioning_category_dict[surface.id] = "SEMI-EXTERIOR"`  

        - Else, surface is classified as unregulated: `else: surface_conditioning_category_dict[surface.id] = "UNREGULATED"`  

**Returns** `return surface_conditioning_category_dict`  

**Rule Assertion Table for Reference:**  
| Adjacent to  /Zone    |Conditioned Res |Conditioned Non-Res |Conditioned Mix  |Semi-heated |Unenclosed |Unconditioned |Exterior |Ground   |
| :-                    |:-:             |:-:                 |:-:              |:-:         |:-:        |:-: |:-:      |:-:      |
| Conditioned Res       |UR              |UR                  |UR               |SEMI        |E-R        |SEMI          |E-R      |E-R      |
| Conditioned Non-Res   |UR              |UR                  |UR               |SEMI        |E-NR       |SEMI          |E-NR     |E-NR     |
| Conditioned Mix       |UR              |UR                  |UR               |SEMI        |E-M        |SEMI          |E-M      |E-M      |
| Semi-heated           |SEMI            |SEMI                |SEMI             |UR          |SEMI       |SEMI          |SEMI     |SEMI     |
| Unenclosed            |E-R             |E-NR                |E-M              |SEMI        |UR         |UR            |UR       |UR       |
| Unconditioned         |SEMI            |SEMI                |SEMI             |SEMI        |UR         |UR            |UR       |UR       |

**[Back](../_toc.md)**
