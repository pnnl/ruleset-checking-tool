
## get_zone_conditioning_category

**Schema Version:** 0.0.23

Description: Determine the Zone Conditioning Category for each zone. This function would cycle through each zone in an RMR and categorize it as ‘conditioned’, 'semi-heated’, 'unenclosed' or ‘unconditioned’.  If ‘conditioned’ it will also categorize the space as ‘residential’ or ‘non-residential’.  

Inputs:  
  - **RMR**: The RMR that needs to determine zone conditioning category.  

Returns:  
- **zone_conditioning_category**: The Zone Conditioning Category [conditioned residential, conditioned non-residential, conditioned mixed, semi-heated, unenclosed, unconditioned].  

Function Call:
- get_hvac_zone_list_w_area()
- GET_COMPONENT_BY_ID()

Constants:
- CAPACITY_THRESHOLD = 3.4 Btu/(h*ft2))
- CRAWLSPACE_HEIGHT_THRESHOLD = 7 ft

Logic:  

- Get dictionary for the list of zones and their total floor area served by each HVAC system in RMR: `hvac_zone_list_w_area_dict = get_hvac_zone_list_w_area(RMR)`

- For each HVAC system id in dictionary: `for hvac_sys_id in hvac_zone_list_w_area_dict.keys():` (Note XC, this only gets HVAC systems serving zones. Orphan HVAC systems are not looped)

  - Get total central sensible cooling capacity for HVAC system:
  **[CH: The hvac system has at most one cooling_system, one heating_system, and one preheat_system. Also, I think we need to handle any of these systems missing.]**
   `total_central_sensible_cool_capacity = SUM(cooling_system.rated_sensible_cool_capacity for cooling_system in GET_COMPONENT_BY_ID(hvac_sys_id).cooling_system)`

  - Get total central heating capacity for HVAC system: `total_central_heat_capacity = SUM(heating_system.heat_capacity for heating_system in GET_COMPONENT_BY_ID(hvac_sys_id).heating_system) + SUM(preheat_system.heat_capacity for preheat_system in GET_COMPONENT_BY_ID(hvac_sys_id).preheat_system)`

  - Calculate and save total central sensible cooling output per floor area for HVAC system to dictionary: `hvac_cool_capacity_dict[hvac_sys_id] = total_central_sensible_cool_capacity / hvac_zone_list_w_area_dict[hvac_sys_id]["TOTAL_AREA"]`

  - Calculate and save total central heating output per floor area for HVAC system to dictionary: `hvac_heat_capacity_dict[hvac_sys_id] = total_central_heat_capacity / hvac_zone_list_w_area_dict[hvac_sys_id]["TOTAL_AREA"]`

- Get building climate zone: `climate_zone = RMR.weather.climate_zone`  

- Get heated space criteria: `system_min_heating_output = data_lookup(table_3_2,climate_zone)`

- For each zone in RMR: `for zone in RMR...zones:`

  - Get zone total floor area: `zone_area = SUM(space.floor_area for space in zone.spaces)`

  - For each terminal serving zone: `for terminal in zone.terminals:`
  
    - Get HVAC system connected to terminal: `hvac_sys = terminal.served_by_heating_ventilating_air_conditioning_system` (Note XC, will there be more than one HVAC system connecting to a terminal?)

    - Add central cooling capacity per floor area to zone capacity dictionary: `zone_capacity_dict[zone.id]["SENSIBLE_COOLING"] += hvac_cool_capacity_dict[hvac_sys.id]`

    - Add central heating capacity per floor area to zone capacity dictionary: `zone_capacity_dict[zone.id]["HEATING"] += hvac_heat_capacity_dict[hvac_sys.id]`

    - Check if terminal has heating capacity, add to zone capacity dictionary: `if terminal.heating_capacity: zone_capacity_dict[zone.id]["HEATING"] += terminal.heat_capacity / zone_area`

    - Check if terminal has cooling capacity, add to zone capacity dictionary: `if terminal.cooling_capacity: zone_capacity_dict[zone.id]["SENSIBLE_COOLING"] += terminal.cooling_capacity / zone_area`

  - Check if zone meets the criteria for directly conditioned (heated or cooled) zone, save zone as directly conditioned: `if ( zone_capacity_dict[zone.id]["SENSIBLE_COOLING"] >= CAPACITY_THRESHOLD ) OR ( zone_capacity_dict[zone.id]["HEATING"] >= system_min_heating_output ): directly_conditioned_zones.append(zone.id)`

  - Else check if zone meets the criteria for semi-heated zones, save zone as semi-heated temporarily: `else if zone_capacity_dict[zone.id]["HEATING"] >=CAPACITY_THRESHOLD: semiheated_zones.append(zone.id)`

- To determine eligibility for indirectly conditioned zones, for each zone in RMR: `for zone in RMR...zones:`  

  - If zone is not directly conditioned (heated or cooled): `if zone not in directly_conditioned_zones:`  

    - If any space in zone is atrium, zone is indirectly conditioned:: `if ( ( space.lighting_space_type == "ATRIUM_LOW_MEDIUM" ) OR ( space.lighting_space_type == "ATRIUM_HIGH" ) for space in zone.spaces ): indirectly_conditioned_zones.append(zone)`  

    - Else, no space in zone is atrium: `else:`  

      - For each surface in zone: `for surface in zone.surfaces:`  

        - Check if surface is interior, get adjacent zone: `if surface.adjacent_to == "INTERIOR": adjacent_zone = match_data_element(RMR, zones, surface.adjacent_zone_id)`  
**[CH: There is no `surface.fenestration_subsurfaces` field. There is a `surface.subsurfaces` field instead. Subsurface has `opaque_area` and `glazed_area`.]**
          - If adjacent zone is directly conditioned (heated or cooled), add the product of the U-factor and surface area to the directly conditioned type: `if adjacent_zone in directly_conditioned_zone: directly_conditioned_product_sum += sum( ( subsurface.glazed_area + subsurface.opaque_area ) * subsurface.u_factor for subsurface in surface.subsurfaces ) + ( surface.area - sum( ( subsurface.glazed_area + subsurface.opaque_area ) for subsurface in surface.subsurfaces ) * surface.construction.u_factor`  

          - Else, add the product of the U-factor and surface area to the other type: `else: other_product_sum += sum( ( subsurface.glazed_area + subsurface.opaque_area ) * subsurface.u_factor for subsurface in surface.subsurfaces ) + ( surface.area - sum( ( subsurface.glazed_area + subsurface.opaque_area ) for subsurface in surface.subsurfaces ) * surface.construction.u_factor`  

        - Else check if surface is exterior, add the product of the U-factor and surface area to the other type: `else if surface.adjacent_to == "EXTERIOR": other_product_sum += sum( ( subsurface.glazed_area + subsurface.opaque_area ) * subsurface.u_factor for subsurface in surface.subsurfaces ) + ( surface.area - sum( ( subsurface.glazed_area + subsurface.opaque_area ) for subsurface in surface.subsurfaces ) * surface.construction.u_factor`  

      - Determine if zone is indirectly conditioned: `if directly_conditioned_product_sum > other_product_sum: indirectly_conditioned_zones.append(zone)`  

- For each building segment in RMR: `for building_segment in RMR...building_segments:`

  - Get lighting building area type for building segment: `lighting_building_area_type = building_segment.lighting_building_area_type`

    - If lighting building area type is residential: `if lighting_building_area_type in ["DORMITORY" , "HOTEL_MOTEL", "MULTIFAMILY"]: segment_residential_flag = TRUE`  

    - Else if lighting building area type is specified, building segment is non-residential: `else if lighting_building_area_type: segment_nonresidential_flag = TRUE`

  - For each zone in building segment: `for zone in building_segment.zones:`  

    - If zone is directly or indirectly conditioned: `if ( zone in directly_conditioned_zones ) OR ( zone in indirectly_conditioned_zones ):`  

      - For each space in zone: `for space in zone.spaces:`  

        - Check if lighting space type is residential, space is classified as residential: `if space.lighting_space_type in ["DORMITORY_LIVING_QUARTERS" , "FIRE_STATION_SLEEPING_QUARTERS", "GUEST_ROOM", "DWELLING_UNIT", "HEALTHCARE_FACILITY_NURSERY", "HEALTHCARE_FACILITY_PATIENT_ROOM"]: space_residential_flag = TRUE`  
**[CH: I suggest replacing `space_residential_flag` with `zone_has_residential_spaces` and replacing `space_nonresidential_flag` with `zone_has_residential_spaces`.]**
        - Else if lighting space type is specified, space is classified as non-residential: `else if space.lighting_space_type: zone_has_nonresidential_spaces = TRUE`  

        - Else if lighting space type is not specified, and lighting building area type is residential, space is classified as residential: `else if segment_residential_flag: zone_has_residential_spaces = TRUE`

        - Else if lighting space type is not specified, and lighting building area type is non-residential, space is classified as non-residential: `else if segment_nonresidential_flag: zone_has_nonresidential_spaces = TRUE`

        - Else, neither lighting space type or lighting building area type is specified, space is classified as non-residential (i.e. where the space classification is unknown, the space shall be classified as an office space as per G3.1-1(c)): `else: zone_has_nonresidential_spaces = TRUE`

      - If zone has both residential and non-residential spaces, classify zone as conditioned mixed: `if zone_has_residential_spaces AND zone_has_nonresidential_spaces: zone_conditioning_category_dict[zone.id] = "CONDITIONED MIXED"`  

      - Else if zone has only residential spaces, classify zone as conditioned residential: `else if zone_has_residential_spaces: zone_conditioning_category_dict[zone.id] = "CONDITIONED RESIDENTIAL"`  

      - Else, zone has only non-residential spaces, classify zone as conditioned non-residential: `else: zone_conditioning_category_dict[zone.id] = "CONDITIONED NON-RESIDENTIAL"`  
    - Else if zone is semi-heated, classify zone as semi-heated: `else if zone in semiheated_zones: zone_conditioning_category_dict[zone.id] = "SEMI-HEATED"`  

    - Else if zone has interior parking spaces, classify zone as unenclosed: `if（ space.lighting_space_type == "PARKING_AREA_INTERIOR" for space in zone.spaces ）: zone_conditioning_category_dict[zone.id] = "UNENCLOSED"`  

    - Else if zone is crawlspace, classify zone as unenclosed: `else if ( ( zone.volume / sum( space.floor_area for space in zone.spaces ) ) < CRAWLSPACE_HEIGHT_THRESHOLD ) AND ( get_opaque_surface_type(surface) in ["HEATED SLAB-ON-GRADE", "UNHEATED SLAB-ON-GRADE"] for `**[CH: insert `any`]**` ANY surface in zone.surfaces ): zone_conditioning_category_dict[zone.id] = "UNENCLOSED"`

    - Else if zone is attic, classify zone as unenclosed: `else if ( ( get_opaque_surface_type(surface) == "ROOF"`**[CH: ROOF?]**` ) AND ( surface.adjacent_to == "EXTERIOR" ) for `**[CH: insert `any`]**` ANY surface in zone.surfaces ): zone_conditioning_category_dict[zone.id] = "UNENCLOSED"`  

    - Else, classify zone as unconditioned: `else: zone_conditioning_category_dict[zone.id] = "UNCONDITIONED"`  

**Returns** `return zone_conditioning_category_dict`  
