## get_zone_conditioning_category
Description: Determine the Zone Conditioning Category for each zone. This function would cycle through each zone in an RMR and categorize it as ‘conditioned’, 'semi-heated’ or ‘unconditioned’.  If ‘conditioned’ it will also categorize the space as ‘residential’ or ‘non-residential’.  

Inputs:
  - **RMR**: The RMR that needs to determine zone conditioning category.  

Returns:
- **zone_conditioning_category**: The Zone Conditioning Category [conditioned residential, conditioned non-residential, semi-heated, unconditioned].  


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

        - For each surface in zone: ```for surface in zone.surfaces:```  

          - Check if surface is interior, get adjacent zone: ```if surface.adjacent_to == "INTERIOR": adjacent_zone = match_data_element(RMR, zones, surface.adjacent_zone_id)```  

            - If adjacent zone is directly conditioned (heated or cooled), add the product of the U-factor and surface area to the directly conditioned type: ```if adjacent_zone in directly_conditioned_zone: directly_conditioned_product_sum += sum( ( fenestration.glazed_area + fenestration.opaque_area ) * fenestration.u_factor for fenestration in surface.fenestration_subsurfaces ) + ( surface.area - sum( ( fenestration.glazed_area + fenestration.opaque_area ) for fenestration in surface.fenestration_subsurfaces ) * surface.construction.u_factor```  

            - Else, add the product of the U-factor and surface area to the other type (outdoor, semi-heated or unconditioned): ```else: other_product_sum += sum( ( fenestration.glazed_area + fenestration.opaque_area ) * fenestration.u_factor for fenestration in surface.fenestration_subsurfaces ) + ( surface.area - sum( ( fenestration.glazed_area + fenestration.opaque_area ) for fenestration in surface.fenestration_subsurfaces ) * surface.construction.u_factor```  

          - Else check if surface is exterior, add the product of the U-factor and surface area to the other type (outdoor, semi-heated or unconditioned): ```else if surface.adjacent_to == "EXTERIOR": other_product_sum += sum( ( fenestration.glazed_area + fenestration.opaque_area ) * fenestration.u_factor for fenestration in surface.fenestration_subsurfaces ) + ( surface.area - sum( ( fenestration.glazed_area + fenestration.opaque_area ) for fenestration in surface.fenestration_subsurfaces ) * surface.construction.u_factor```  

        - Determine if zone is indirectly conditioned: ```if directly_conditioned_product_sum > other_product_sum: indirectly_conditioned_zones.append(zone)```  

  - Check if building segment is residential: ```if ( building_segment.lighting_building_area_type == "Dormitory" ) OR ( building_segment.lighting_building_area_type == "Hotel/Motel" ) OR ( building_segment.lighting_building_area_type == "Multifamily" ):```  

    - For each thermal block in building segment: ```for thermal_block in building_segment.thermal_blocks:```  

      - For each zone in thermal block: ```for zone in thermal_block.zones:```  

        - If zone is directly or indirectly conditioned, classify zone as conditioned residential: ```if ( zone in directly_conditioned_zones ) OR ( zone in indirectly_conditioned_zones ): zone_conditioning_category_dict[zone.id] = "CONDITIONED RESIDENTIAL"```

        - Else if zone is semi-heated, classify zone as semi-heated: ```else if zone in semiheated_zones: zone_conditioning_category_dict[zone.id] = "SEMI-HEATED"```

        - Else, classify zone as unconditioned: ```else: zone_conditioning_category_dict[zone.id] = "UNCONDITIONED"```  

  - Else check if building segment is non-residential: ```else if building_segment.lighting_building_area_type:```  

    - For each thermal block in building segment: ```for thermal_block in building_segment.thermal_blocks:```  

    - For each zone in thermal block: ```for zone in thermal_block.zones:```  

      - If zone is directly or indirectly conditioned, classify zone as conditioned non-residential: ```if ( zone in directly_conditioned_zones ) OR ( zone in indirectly_conditioned_zones ): zone_conditioning_category_dict[zone.id] = "CONDITIONED NON-RESIDENTIAL"```

      - Else if zone is semi-heated, classify zone as semi-heated: ```else if zone in semiheated_zones: zone_conditioning_category_dict[zone.id] = "SEMI-HEATED"```

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

      - Else, classify zone as unconditioned: ```else: zone_conditioning_category_dict[zone.id] = "UNCONDITIONED"```  

**Returns** ```return zone_conditioning_category_dict```  

## get_surface_conditioning_category
Description: Determine Surface Conditioning Category for each Surface of all Zones in RMR.  

Inputs:

  - **RMR**: The RMR that needs to determine surface conditioning category.  

Returns:

  - **surface_conditioning_category**: The Surface Conditioning Category [conditioned, semi-heated, unregulated].  

Logic:  

- Get zone conditioning category dictionary for the RMR: ```zone_conditioning_category_dict = get_zone_conditioning_category(RMR)```  

- For each building segment in the RMR: ```for building_segment in RMR.building.building_segments:```  

  - For each thermal block in building segment: ```for thermal_block in building_segment.thermal_blocks:```  

    - For each zone in thermal block: ```for zone in thermal_block.zones:```  

      - If zone is conditioned: ```if zone_conditioning_category_dict[zone.id] == "CONDITIONED":```  

        - For each surface in zone: ```for surface in zone.surfaces:```  

          - Check if surface adjacency is exterior or ground, surface is classified as conditioned: ```if ( surface.adjacent_to == "EXTERIOR" ) OR ( surface.adjacent_to == "GROUND" ): surface_conditioning_category_dict[surface.id] = "CONDITIONED"```  

          - Else if surface adjacency is interior, get adjacent zone: ```else if surface.adjacent_to == "INTERIOR": adjacent_zone = match_data_element(RMR, zones, surface.adjacent_zone_id)```  

            - Check if adjacent zone is conditioned, surface is classified as unregulated: ```if zone_conditioning_category_dict(adjacent_zone) == "CONDITIONED": surface_conditioning_category_dict[surface.id] = "UNREGULATED"```  

            - Else, adjacent zone is semi-heated or unconditioned, surface is classified as semi-heated: ```else: surface_conditioning_category_dict[surface.id] = "SEMI-HEATED"```  

          - Else, surface adjacency is identical or undefined, surface is classified as unregulated: ```else: surface_conditioning_category_dict[surface.id] = "UNREGULATED"```  

      - Else if zone is semi-heated: ```else if: zone_conditioning_category_dict[zone.id] == "SEMI-HEATED":```  

        - For each surface in zone: ```for surface in zone.surfaces:```  

          - Check if surface adjacency is exterior or ground, surface is classified as semi-heated: ```if ( surface.adjacent_to == "EXTERIOR" ) OR ( surface.adjacent_to == "GROUND" ): surface_conditioning_category_dict[surface.id] = "SEMI-HEATED"```  

          - Else if surface adjacency is interior, get adjacent zone: ```else if surface.adjacent_to == "INTERIOR": adjacent_zone = match_data_element(RMR, zones, surface.adjacent_zone_id)```  

            - Check if adjacent zone is conditioned or unconditioned, surface is classified as semi-heated: ```if ( zone_conditioning_category_dict(adjacent_zone) == "CONDITIONED" ) OR ( zone_conditioning_category_dict(adjacent_zone) == "UNCONDITIONED" ): surface_conditioning_category_dict[surface.id] = "SEMI-HEATED"```  

            - Else, adjacent zone is semi-heated, surface is classified as unregulated: ```else: surface_conditioning_category_dict[surface.id] = "UNREGULATED"```  

          - Else, surface adjacency is identical or undefined, surface is classified as unregulated: ```else: surface_conditioning_category_dict[surface.id] = "UNREGULATED"```  

      - Else, zone is unconditioned: ```else:```  

        - For each surface in zone: ```for surface in zone.surfaces:```  

          - Check if surface adjacency is exterior or ground, surface is classified as unregulated: ```if ( surface.adjacent_to == "EXTERIOR" ) OR ( surface.adjacent_to == "GROUND" ): surface_conditioning_category_dict[surface.id] = "UNREGULATED"```  

          - Else if surface adjacency is interior, get adjacent zone: ```else if surface.adjacent_to == "INTERIOR": adjacent_zone = match_data_element(RMR, zones, surface.adjacent_zone_id)```  

            - Check if adjacent zone is conditioned or semi-heated, surface is classified as semi-heated: ```if ( zone_conditioning_category_dict(adjacent_zone) == "CONDITIONED" ) OR ( zone_conditioning_category_dict(adjacent_zone) == "SEMI-HEATED" ): surface_conditioning_category_dict[surface.id] = "SEMI-HEATED"```  

            - Else, adjacent zone is unconditioned, surface is classified as unregulated: ```else: surface_conditioning_category_dict[surface.id] = "UNREGULATED"```  

          - Else, surface adjacency is identical or undefined, surface is classified as unregulated: ```else: surface_conditioning_category_dict[surface.id] = "UNREGULATED"```  

**Returns** ```return surface_conditioning_category_dict```  

## get_opaque_surface_type
Description: This function would determine whether it is a wall, ceiling or floor.  

Inputs:
  - **Surface**: The surface that needs to determine surface type.  

Returns:
- **opaque_surface_type**: The Opaque Surface Type [wall, ceiling, floor].  


Logic:  

- If surface tilt is more than or equal to 0 degree and less than 60 degrees, surface is classified as ceiling: ```if 0 <= surface.tilt < 60: surface_type == "CEILING"```  

- Else if surface tile is more than 120 degrees and less than or equal to 180 degrees, surface is classified as floor: ```else if 120 < surface.tilt <= 180: surface_type == "FLOOR"```  

- Else, surface is classified as wall: ```else: surface_type == "WALL"```

**Returns** ```return surface_type```

