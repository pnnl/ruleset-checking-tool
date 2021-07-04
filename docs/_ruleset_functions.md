## get_zone_conditioning_category
Description: Determine the Zone Conditioning Category for each zone. This function would cycle through each zone in an RMR and categorize it as ‘conditioned’, 'semi-heated’, 'unenclosed' or ‘unconditioned’.  If ‘conditioned’ it will also categorize the space as ‘residential’ or ‘non-residential’.  

Inputs:
  - **RMR**: The RMR that needs to determine zone conditioning category.  

Returns:
- **zone_conditioning_category**: The Zone Conditioning Category [conditioned residential, conditioned non-residential, conditioned mixed, semi-heated, unenclosed, unconditioned].  


Logic:  

- Get building climate zone: ```climate_zone = RMR.weather.climate_zone```  

  - Get heated space criteria: ```system_min_heating_output = data_lookup(table_3_2,climate_zone)```  

- For each building segment in the RMR: ```for building_segment in RMR.building.building_segments:```  

  - To determine eligibility for directly conditioned (heated or cooled) and semi-heated zones, for each HVAC system in building segment: ```for hvac_system in building_segment.heating_ventilation_air_conditioning_systems:```  

    - Check if the system meets the criteria for serving directly conditioned (heated or cooled) zones, save all zones served by the system as directly conditioned: ```if ( hvac_system.simulation_result_sensible_cool_capacity >= 3.4 ) OR ( hvac_system.simulation_result_heat_capacity >= system_min_heating_output ):  for zone in hvac_system.zones_served: directly_conditioned_zones.append(zone)```  

    - Else check if the system meets the criteria for serving semi-heated zones, save all zones served by the system as semi-heated: ```else if hvac_system.simulation_result_heat_capacity >= 3.4: for zone in hvac_system.zones_served: semiheated_zones.append(zone)```  

  - To determine eligibility for indirectly conditioned zones, for each thermal block in building segment: ```for thermal_block in building_segment.thermal_blocks:```  

    - For each zone in thermal block: ```for zone in thermal_block.zones:```  

      - If zone is not directly conditioned (heated or cooled): ```if zone not in directly_conditioned_zones:```  

        - If any space in zone is atrium, zone is indirectly conditioned:: ```if ( ( space.lighting_space_type == "Atrium, <= 40ft in height" ) OR ( space.lighting_space_type == "Atrium, > 40ft in height" ) for space in zone.spaces ): indirectly_conditioned_zones.append(zone)```  

        - Else, no space in zone is atrium: ```else:```  

          - For each surface in zone: ```for surface in zone.surfaces:```  

            - Check if surface is interior, get adjacent zone: ```if surface.adjacent_to == "INTERIOR": adjacent_zone = match_data_element(RMR, zones, surface.adjacent_zone_id)```  

              - If adjacent zone is directly conditioned (heated or cooled), add the product of the U-factor and surface area to the directly conditioned type: ```if adjacent_zone in directly_conditioned_zone: directly_conditioned_product_sum += sum( ( fenestration.glazed_area + fenestration.opaque_area ) * fenestration.u_factor for fenestration in surface.fenestration_subsurfaces ) + ( surface.area - sum( ( fenestration.glazed_area + fenestration.opaque_area ) for fenestration in surface.fenestration_subsurfaces ) * surface.construction.u_factor```  

              - Else, add the product of the U-factor and surface area to the other type: ```else: other_product_sum += sum( ( fenestration.glazed_area + fenestration.opaque_area ) * fenestration.u_factor for fenestration in surface.fenestration_subsurfaces ) + ( surface.area - sum( ( fenestration.glazed_area + fenestration.opaque_area ) for fenestration in surface.fenestration_subsurfaces ) * surface.construction.u_factor```  

            - Else check if surface is exterior, add the product of the U-factor and surface area to the other type: ```else if surface.adjacent_to == "EXTERIOR": other_product_sum += sum( ( fenestration.glazed_area + fenestration.opaque_area ) * fenestration.u_factor for fenestration in surface.fenestration_subsurfaces ) + ( surface.area - sum( ( fenestration.glazed_area + fenestration.opaque_area ) for fenestration in surface.fenestration_subsurfaces ) * surface.construction.u_factor```  

          - Determine if zone is indirectly conditioned: ```if directly_conditioned_product_sum > other_product_sum: indirectly_conditioned_zones.append(zone)```  

  - Check if building segment is residential: ```if ( building_segment.lighting_building_area_type == "Dormitory" ) OR ( building_segment.lighting_building_area_type == "Hotel/Motel" ) OR ( building_segment.lighting_building_area_type == "Multifamily" ):```  

    - For each thermal block in building segment: ```for thermal_block in building_segment.thermal_blocks:```  

      - For each zone in thermal block: ```for zone in thermal_block.zones:```  

        - If zone is directly or indirectly conditioned, classify zone as conditioned residential: ```if ( zone in directly_conditioned_zones ) OR ( zone in indirectly_conditioned_zones ): zone_conditioning_category_dict[zone.id] = "CONDITIONED RESIDENTIAL"```

        - Else if zone is semi-heated, classify zone as semi-heated: ```else if zone in semiheated_zones: zone_conditioning_category_dict[zone.id] = "SEMI-HEATED"```  

        - Else if zone is crawlspace, classify zone as unenclosed: ```else if ( ( zone.volume / sum( space.floor_area for space in zone.spaces ) ) < 7 ) AND ( ( get_opaque_surface_type(surface) == "FLOOR" ) AND ( surface.adjacent_to == "GROUND" ) for surface in zone.surfaces ): zone_conditioning_category_dict[zone.id] = "UNENCLOSED"```  

        - Else if zone is attic, classify zone as unenclosed: ```else if ( ( get_opaque_surface_type(surface) == "CEILING" ) AND ( surface.adjacent_to == "EXTERIOR" ) for surface in zone.surfaces ): zone_conditioning_category_dict[zone.id] = "UNENCLOSED"```  

        - Else, classify zone as unconditioned: ```else: zone_conditioning_category_dict[zone.id] = "UNCONDITIONED"```  

  - Else check if building segment is non-residential: ```else if building_segment.lighting_building_area_type:```  

    - For each thermal block in building segment: ```for thermal_block in building_segment.thermal_blocks:```  

    - For each zone in thermal block: ```for zone in thermal_block.zones:```  

      - If zone is directly or indirectly conditioned, classify zone as conditioned non-residential: ```if ( zone in directly_conditioned_zones ) OR ( zone in indirectly_conditioned_zones ): zone_conditioning_category_dict[zone.id] = "CONDITIONED NON-RESIDENTIAL"```

      - Else if zone is semi-heated, classify zone as semi-heated: ```else if zone in semiheated_zones: zone_conditioning_category_dict[zone.id] = "SEMI-HEATED"```  

      - Else if zone is crawlspace, classify zone as unenclosed: ```else if ( ( zone.volume / sum( space.floor_area for space in zone.spaces ) ) < 7 ) AND ( ( get_opaque_surface_type(surface) == "FLOOR" ) AND ( surface.adjacent_to == "GROUND" ) for surface in zone.surfaces ): zone_conditioning_category_dict[zone.id] = "UNENCLOSED"```  

      - Else if zone is attic, classify zone as unenclosed: ```else if ( ( get_opaque_surface_type(surface) == "CEILING" ) AND ( surface.adjacent_to == "EXTERIOR" ) for surface in zone.surfaces ): zone_conditioning_category_dict[zone.id] = "UNENCLOSED"```  

      - Else, classify zone as unconditioned: ```else: zone_conditioning_category_dict[zone.id] = "UNCONDITIONED"```  
  
  - Else, building segment uses space-by-space type method, for each thermal block in building segment: ```for thermal_block in building_segment.thermal_blocks:```  

    - For each zone in thermal block: ```for zone in thermal_block.zones:```  

      - If zone is directly or indirectly conditioned: ```if ( zone in directly_conditioned_zones ) OR ( zone in indirectly_conditioned_zones ):```  

        - For each space in zone: ```for space in zone.spaces:```  

          - Check if space is residential: ```if ( space.lighting_space_type ==  "Dormitory - Living Quarters" ) OR ( space.lighting_space_type ==  "Fire Station - Sleeping Quarters" ) OR ( space.lighting_space_type ==  "Guest Room" ) OR ( space.lighting_space_type ==  "Dwelling Unit" ) OR ( space.lighting_space_type ==  "Healthcare Facility - Nursery" ) OR ( space.lighting_space_type ==  "Healthcare Facility - Patient Room" ): residential_flag = TRUE```  

          - Else, space is non-residential: ```else: nonresidential_flag = TRUE```  

        - If zone has both residential and non-residential spaces, classify zone as conditioned mixed: ```if residential_flag AND nonresidential_flag: zone_conditioning_category_dict[zone.id] = "CONDITIONED MIXED"```  

        - Else if zone has only residential spaces, classify zone as conditioned residential: ```else if residential_flag: zone_conditioning_category_dict[zone.id] = "CONDITIONED RESIDENTIAL"```  

        - Else, zone has only non-residential spaces, classify zone as conditioned non-residential: ```else: zone_conditioning_category_dict[zone.id] = "CONDITIONED NON-RESIDENTIAL"```  

      - Else if zone is semi-heated, classify zone as semi-heated: ```else if zone in semiheated_zones: zone_conditioning_category_dict[zone.id] = "SEMI-HEATED"```  

      - Else if zone has interior parking spaces, classify zone as unenclosed: ```if（ space.lighting_space_type == "Parking Area, Interior" for space in zone.spaces ）: zone_conditioning_category_dict[zone.id] = "UNENCLOSED"```  

      - Else if zone is crawlspace, classify zone as unenclosed: ```else if ( ( zone.volume / sum( space.floor_area for space in zone.spaces ) ) < 7 ) AND ( ( get_opaque_surface_type(surface) == "FLOOR" ) AND ( surface.adjacent_to == "GROUND" ) for surface in zone.surfaces ): zone_conditioning_category_dict[zone.id] = "UNENCLOSED"```  

      - Else if zone is attic, classify zone as unenclosed: ```else if ( ( get_opaque_surface_type(surface) == "CEILING" ) AND ( surface.adjacent_to == "EXTERIOR" ) for surface in zone.surfaces ): zone_conditioning_category_dict[zone.id] = "UNENCLOSED"```  

      - Else, classify zone as unconditioned: ```else: zone_conditioning_category_dict[zone.id] = "UNCONDITIONED"```  

**Returns** ```return zone_conditioning_category_dict```  

## get_surface_conditioning_category
Description: This function would cycle through each surface in  a zone and categorize it as exterior res, exterior non res, exterior mixed, semi-exterior or unregulated.  

Inputs:

  - **RMR**: The RMR that needs to determine surface conditioning category.  

Returns:

  - **surface_conditioning_category**: The Surface Conditioning Category [exterior residential, exterior non-residential, exterior mixed, semi-exterior, unregulated].  

Logic:  

- Get zone conditioning category dictionary for the RMR: ```zone_conditioning_category_dict = get_zone_conditioning_category(RMR)```  

- For each building segment in the RMR: ```for building_segment in RMR.building.building_segments:```  

  - For each thermal block in building segment: ```for thermal_block in building_segment.thermal_blocks:```  

    - For each zone in thermal block: ```for zone in thermal_block.zones:```  

      - If zone is residential and conditioned: ```if zone_conditioning_category_dict[zone.id] == "CONDITIONED RESIDENTIAL":```  

        - For each surface in zone: ```for surface in zone.surfaces:```  

          - If surface adjacency is exterior, ground or if surface adjacency is interior and the adjacent zone is unenclosed, surface is classified as exterior residential type: ```if ( surface.adjacent_to == "EXTERIOR" ) OR ( surface.adjacent_to == "GROUND" ) OR ( ( surface.adjacent_to == "INTERIOR" ) AND ( zone_conditioning_category_dict[surface.adjacent_zone_id] == "UNENCLOSED" ) ): surface_conditioning_category_dict[surface.id] = "EXTERIOR RESIDENTIAL"```  

          - Else if surface adjacency is interior and the adjacent zone is semi-heated or unconditioned, surface is classified as semi-exterior: ```else if ( surface.adjacent_to == "INTERIOR" ) AND ( ( zone_conditioning_category_dict[surface.adjacent_zone_id] == "SEMI-HEATED" ) OR ( zone_conditioning_category_dict[surface.adjacent_zone_id] == "UNCONDITIONED" ) ): surface_conditioning_category_dict[surface.id] = "SEMI-EXTERIOR"```  

          - Else, surface is unregulated: ```else: surface_conditioning_category_dict[surface.id] = "UNREGULATED"```  

      - Else if zone is non-residential and conditioned: ```else if zone_conditioning_category_dict[zone.id] == "CONDITIONED NONRESIDENTIAL":```  

        - For each surface in zone: ```for surface in zone.surfaces:```  

          - If surface adjacency is exterior, ground or if surface adjacency is interior and the adjacent zone is unenclosed, surface is classified as exterior non-residential type: ```if ( surface.adjacent_to == "EXTERIOR" ) OR ( surface.adjacent_to == "GROUND" ) OR ( ( surface.adjacent_to == "INTERIOR" ) AND ( zone_conditioning_category_dict[surface.adjacent_zone_id] == "UNENCLOSED" ) ): surface_conditioning_category_dict[surface.id] = "EXTERIOR NON-RESIDENTIAL"```  

          - Else if surface adjacency is interior and the adjacent zone is semi-heated or unconditioned, surface is classified as semi-exterior: ```else if ( surface.adjacent_to == "INTERIOR" ) AND ( ( zone_conditioning_category_dict[surface.adjacent_zone_id] == "SEMI-HEATED" ) OR ( zone_conditioning_category_dict[surface.adjacent_zone_id] == "UNCONDITIONED" ) ): surface_conditioning_category_dict[surface.id] = "SEMI-EXTERIOR"```  

          - Else, surface is unregulated: ```else: surface_conditioning_category_dict[surface.id] = "UNREGULATED"```  

      - Else if zone is mixed and conditioned: ```else if zone_conditioning_category_dict[zone.id] == "CONDITIONED MIXED":```  

        - For each surface in zone: ```for surface in zone.surfaces:```  

          - If surface adjacency is exterior, ground or if surface adjacency is interior and the adjacent zone is unenclosed, surface is classified as exterior mixed type: ```if ( surface.adjacent_to == "EXTERIOR" ) OR ( surface.adjacent_to == "GROUND" ) OR ( ( surface.adjacent_to == "INTERIOR" ) AND ( zone_conditioning_category_dict[surface.adjacent_zone_id] == "UNENCLOSED" ) ): surface_conditioning_category_dict[surface.id] = "EXTERIOR MIXED"```  

          - Else if surface adjacency is interior and the adjacent zone is semi-heated or unconditioned, surface is classified as semi-exterior: ```else if ( surface.adjacent_to == "INTERIOR" ) AND ( ( zone_conditioning_category_dict[surface.adjacent_zone_id] == "SEMI-HEATED" ) OR ( zone_conditioning_category_dict[surface.adjacent_zone_id] == "UNCONDITIONED" ) ): surface_conditioning_category_dict[surface.id] = "SEMI-EXTERIOR"```  

          - Else, surface is unregulated: ```else: surface_conditioning_category_dict[surface.id] = "UNREGULATED"```  

      - Else if zone is semi-heated: ```else if zone_conditioning_category_dict[zone.id] == "SEMI-HEATED":```  

        - For each surface in zone: ```for surface in zone.surfaces:```  

          - If surface adjacency is exterior, ground, or if surface adjacency is interior and the adjacent zone is conditioned, unenclosed or unconditioned, surface is classified as semi-exterior: ```if ( surface.adjacent_to == "EXTERIOR" ) OR ( surface.adjacent_to == "GROUND" ) OR ( ( surface.adjacent_to == "INTERIOR" ) AND ( ( zone_conditioning_category_dict[surface.adjacent_zone_id] == "CONDITIONED RESIDENTIAL" ) OR ( zone_conditioning_category_dict[surface.adjacent_zone_id] == "CONDITIONED NON-RESIDENTIAL" ) OR ( zone_conditioning_category_dict[surface.adjacent_zone_id] == "CONDITIONED MIXED" ) OR ( zone_conditioning_category_dict[surface.adjacent_zone_id] == "UNENCLOSED" ) OR ( zone_conditioning_category_dict[surface.adjacent_zone_id] == "UNCONDITIONED" ) ): surface_conditioning_category_dict[surface.id] = "SEMI-EXTERIOR"```  

          - Else, surface is classified as unregulated: ```else: surface_conditioning_category_dict[surface.id] = "UNREGULATED"```  

      - Else if zone is unenclosed: ```else if zone_conditioning_category_dict[zone.id] == "UNENCLOSED":```  

        - For each surface in zone: ```for surface in zone.surfaces:```  

          - If surface adjacency is interior and the adjacent zone is residential and conditioned, surface is classified as exterior residential: ```else if ( surface.adjacent_to == "INTERIOR" ) AND ( zone_conditioning_category_dict[surface.adjacent_zone_id] == "CONDITIONED RESIDENTIAL" ): surface_conditioning_category_dict[surface.id] = "EXTERIOR RESIDENTIAL"```  

          - Else if surface adjacency is interior and the adjacent zone is non-residential and conditioned, surface is classified as exterior non-residential: ```else if ( surface.adjacent_to == "INTERIOR" ) AND ( zone_conditioning_category_dict[surface.adjacent_zone_id] == "CONDITIONED NON-RESIDENTIAL" ): surface_conditioning_category_dict[surface.id] = "EXTERIOR NON-RESIDENTIAL"```  

          - Else if surface adjacency is interior and the adjacent zone is mixed and conditioned, surface is classified as exterior mixed: ```else if ( surface.adjacent_to == "INTERIOR" ) AND ( zone_conditioning_category_dict[surface.adjacent_zone_id] == "CONDITIONED MIXED" ): surface_conditioning_category_dict[surface.id] = "EXTERIOR MIXED"```  

          - Else if surface adjacency is interior and the adjacent zone is semi-heated, surface is classified as semi-exterior: ```else if ( surface.adjacent_to == "INTERIOR" ) AND ( zone_conditioning_category_dict[surface.adjacent_zone_id] == "SEMI-HEATED" ): surface_conditioning_category_dict[surface.id] = "SEMI-EXTERIOR"```  

          - Else, surface is classified as unregulated: ```else: surface_conditioning_category_dict[surface.id] = "UNREGULATED"```  

      - Else, zone is unconditioned: ```else:```  

        - For each surface in zone:  ```for surface in zone.surfaces:```  

          - If surface adjacency is interior and the adjacent zone is conditioned or semi-heated, surface is classified as semi-exterior: ```if ( surface.adjacent_to == "INTERIOR" ) AND ( ( zone_conditioning_category_dict[surface.adjacent_zone_id] == "CONDITIONED RESIDENTIAL" ) OR ( zone_conditioning_category_dict[surface.adjacent_zone_id] == "CONDITIONED NON-RESIDENTIAL" ) OR ( zone_conditioning_category_dict[surface.adjacent_zone_id] == "CONDITIONED MIXED" ) OR ( zone_conditioning_category_dict[surface.adjacent_zone_id] == "SEMI-HEATED" ) ): surface_conditioning_category_dict[surface.id] = "SEMI-EXTERIOR"```  

          - Else, surface is classified as unregulated: ```else: surface_conditioning_category_dict[surface.id] = "UNREGULATED"```  

**Returns** ```return surface_conditioning_category_dict```  

## get_opaque_surface_type
Description: This function would determine whether it is a wall, ceiling or floor.  

Inputs:
  - **Surface**: The surface that needs to determine surface type.  

Returns:
- **opaque_surface_type**: The Opaque Surface Type [roof, heated slab-on-grade, unheated slab-on-grade, floor, above-grade wall, below-grade wall, unregulated].  


Logic:  

- If surface tilt is more than or equal to 0 degree and less than 60 degrees, surface is classified as roof: ```if 0 <= surface.tilt < 60:```  

  - Determine if surface is roof: ```if surface.adjacent_to == "EXTERIOR": surface_type = "ROOF"```  

  - Else, surface is unregulated: ```else: surface_type = "UNREGULATED"```  

- Else if surface tile is more than 120 degrees and less than or equal to 180 degrees, surface is classified as floor: ```else if 120 < surface.tilt <= 180:```  

  - Determine if surface is heated slab-on-grade: ```if ( surface.construction.has_radiant_heating ) AND ( surface.adjacent_to == "GROUND" ): surface_type = "HEATED SLAB-ON-GRADE"```  

  - Else determine if surface is unheated slab-on-grade: ```else if surface.adjacent_to == "GROUND": surface_type = "UNHEATED SLAB-ON-GRADE"```  

  - Else determine if surface is exposed floor: ```else if surface.adjacent_to == "EXTERIOR": surface_type = "FLOOR"```  

  - Else, surface is unregulated: ```else: surface_type = "UNREGULATED"```  

- Else, surface is classified as wall: ```else:```  

  - Determine if surface is below grade wall: ```if surface.adjacent_to == "GROUND": surface_type = "BELOW-GRADE WALL"```  

  - Else determine if surface is above grade wall: ```else if surface.adjacent_to == "EXTERIOR": surface_type = "ABOVE-GRADE WALL"```  

  - Else, surface is unregulated: ```else: surface_type = "UNREGULATED"```  

**Returns** ```return surface_type```  
