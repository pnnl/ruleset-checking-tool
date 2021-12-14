
## get_zone_conditioning_category

Description: Determine the Zone Conditioning Category for each zone. This function would cycle through each zone in an RMR and categorize it as ‘conditioned’, 'semi-heated’, 'unenclosed' or ‘unconditioned’.  If ‘conditioned’ it will also categorize the space as ‘residential’ or ‘non-residential’.  

Inputs:  
  - **RMR**: The RMR that needs to determine zone conditioning category.  

Returns:  
- **zone_conditioning_category**: The Zone Conditioning Category [conditioned residential, conditioned non-residential, conditioned mixed, semi-heated, unenclosed, unconditioned].  

Constants:
- CAPACITY_THRESHOLD = 3.4 Btu/(h*ft2))
- CRAWLSPACE_HEIGHT_THRESHOLD = 7 ft

Logic:  

- Get building climate zone: `climate_zone = RMR.weather.climate_zone`  

  - Get heated space criteria: `system_min_heating_output = data_lookup(table_3_2,climate_zone)`  

- For each building segment in the RMR: `for building_segment in RMR.building.building_segments:`  

  - To determine eligibility for directly conditioned (heated or cooled) and semi-heated zones, for each HVAC system in building segment: `for hvac_system in building_segment.heating_ventilation_air_conditioning_systems:`  

    - Check if the system meets the criteria for serving directly conditioned (heated or cooled) zones, save all zones served by the system as directly conditioned: `if ( hvac_system.simulation_result_sensible_cool_capacity >= CAPACITY_THRESHOLD ) OR ( hvac_system.simulation_result_heat_capacity >= system_min_heating_output ):  for zone in hvac_system.zones_served: directly_conditioned_zones.append(zone)`  

    - Else check if the system meets the criteria for serving semi-heated zones, save all zones served by the system as semi-heated: `else if hvac_system.simulation_result_heat_capacity >= CAPACITY_THRESHOLD: for zone in hvac_system.zones_served: semiheated_zones.append(zone)`  

  - To determine eligibility for indirectly conditioned zones, for each zone in building_segment: `for zone in building_segment.zones:`  

    - If zone is not directly conditioned (heated or cooled): `if zone not in directly_conditioned_zones:`  

      - If any space in zone is atrium, zone is indirectly conditioned:: `if ( ( space.lighting_space_type == "ATRIUM_LOW_MEDIUM" ) OR ( space.lighting_space_type == "ATRIUM_HIGH" ) for space in zone.spaces ): indirectly_conditioned_zones.append(zone)`  

      - Else, no space in zone is atrium: `else:`  

        - For each surface in zone: `for surface in zone.surfaces:`  

          - Check if surface is interior, get adjacent zone: `if surface.adjacent_to == "INTERIOR": adjacent_zone = match_data_element(RMR, zones, surface.adjacent_zone_id)`  

            - If adjacent zone is directly conditioned (heated or cooled), add the product of the U-factor and surface area to the directly conditioned type: `if adjacent_zone in directly_conditioned_zone: directly_conditioned_product_sum += sum( ( fenestration.glazed_area + fenestration.opaque_area ) * fenestration.u_factor for fenestration in surface.fenestration_subsurfaces ) + ( surface.area - sum( ( fenestration.glazed_area + fenestration.opaque_area ) for fenestration in surface.fenestration_subsurfaces ) * surface.construction.u_factor`  

            - Else, add the product of the U-factor and surface area to the other type: `else: other_product_sum += sum( ( fenestration.glazed_area + fenestration.opaque_area ) * fenestration.u_factor for fenestration in surface.fenestration_subsurfaces ) + ( surface.area - sum( ( fenestration.glazed_area + fenestration.opaque_area ) for fenestration in surface.fenestration_subsurfaces ) * surface.construction.u_factor`  

          - Else check if surface is exterior, add the product of the U-factor and surface area to the other type: `else if surface.adjacent_to == "EXTERIOR": other_product_sum += sum( ( fenestration.glazed_area + fenestration.opaque_area ) * fenestration.u_factor for fenestration in surface.fenestration_subsurfaces ) + ( surface.area - sum( ( fenestration.glazed_area + fenestration.opaque_area ) for fenestration in surface.fenestration_subsurfaces ) * surface.construction.u_factor`  

        - Determine if zone is indirectly conditioned: `if directly_conditioned_product_sum > other_product_sum: indirectly_conditioned_zones.append(zone)`  

  - Get lighting building area type for building segment: `lighting_building_area_type = building_segment.lighting_building_area_type`

    - If lighting building area type is residential: `if lighting_building_area_type in ["DORMITORY" , "HOTEL_MOTEL", "MULTIFAMILY"]: segment_residential_flag = TRUE`  

    - Else if lighting building area type is specified, building segment is non-residential: `else if lighting_building_area_type: segment_nonresidential_flag = TRUE`

  - For each thermal block in building segment: `for thermal_block in building_segment.thermal_blocks:`  

    - For each zone in thermal block: `for zone in thermal_block.zones:`  

      - If zone is directly or indirectly conditioned: `if ( zone in directly_conditioned_zones ) OR ( zone in indirectly_conditioned_zones ):`  

        - For each space in zone: `for space in zone.spaces:`  

          - Check if lighting space type is residential, space is classified as residential: `if space.lighting_space_type in ["DORMITORY_LIVING_QUARTERS" , "FIRE_STATION_SLEEPING_QUARTERS", "GUEST_ROOM", "DWELLING_UNIT", "HEALTHCARE_FACILITY_NURSERY", "HEALTHCARE_FACILITY_PATIENT_ROOM"]: space_residential_flag = TRUE`  

          - Else if lighting space type is specified, space is classified as non-residential: `else if space.lighting_space_type: space_nonresidential_flag = TRUE`  

          - Else if lighting space type is not specified, and lighting building area type is residential, space is classified as residential: `else if segment_residential_flag: space_residential_flag = TRUE`

          - Else if lighting space type is not specified, and lighting building area type is non-residential, space is classified as non-residential: `else if segment_nonresidential_flag: space_nonresidential_flag = TRUE`

          - Else, neither lighting space type or lighting building area type is specified, space is classified as non-residential (i.e. where the space classification is unknown, the space shall be classified as an office space as per G3.1-1(c)): `else: space_nonresidential_flag = TRUE`

        - If zone has both residential and non-residential spaces, classify zone as conditioned mixed: `if residential_flag AND nonresidential_flag: zone_conditioning_category_dict[zone.id] = "CONDITIONED MIXED"`  

        - Else if zone has only residential spaces, classify zone as conditioned residential: `else if residential_flag: zone_conditioning_category_dict[zone.id] = "CONDITIONED RESIDENTIAL"`  

        - Else if zone has only non-residential spaces, classify zone as conditioned non-residential: `else: zone_conditioning_category_dict[zone.id] = "CONDITIONED NON-RESIDENTIAL"`  

      - Else if zone is semi-heated, classify zone as semi-heated: `else if zone in semiheated_zones: zone_conditioning_category_dict[zone.id] = "SEMI-HEATED"`  

      - Else if zone has interior parking spaces, classify zone as unenclosed: `if（ space.lighting_space_type == "Parking Area, Interior" for space in zone.spaces ）: zone_conditioning_category_dict[zone.id] = "UNENCLOSED"`  

      - Else if zone is crawlspace, classify zone as unenclosed: `else if ( ( zone.volume / sum( space.floor_area for space in zone.spaces ) ) < CRAWLSPACE_HEIGHT_THRESHOLD ) AND ( ( get_opaque_surface_type(surface) == "HEATED SLAB-ON-GRADE" OR get_opaque_surface_type(surface) == "UNHEATED SLAB-ON-GRADE") AND ( surface.adjacent_to == "GROUND" ) for surface in zone.surfaces ): zone_conditioning_category_dict[zone.id] = "UNENCLOSED"`  

      - Else if zone is attic, classify zone as unenclosed: `else if ( ( get_opaque_surface_type(surface) == "CEILING" ) AND ( surface.adjacent_to == "EXTERIOR" ) for surface in zone.surfaces ): zone_conditioning_category_dict[zone.id] = "UNENCLOSED"`  

      - Else, classify zone as unconditioned: `else: zone_conditioning_category_dict[zone.id] = "UNCONDITIONED"`  

**Returns** `return zone_conditioning_category_dict`  

**[Back](../_toc.md)**
