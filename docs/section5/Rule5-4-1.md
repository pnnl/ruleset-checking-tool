
# Envelope - Rule 5-4

**Rule ID:** 5-4
**Rule Description:** Baseline opaque Assemblies used for new buildings, existing buildings, or additions shall match the appropriate assembly maximum U-factors in Tables G3.4-1 through G3.4-8: Roofs—Insulation entirely above deck (A2.2) 
**Rule Assertion:** Baseline RMR Surface:U_factor = expected value  
**Appendix G Section:** Section G3.1-5(b) Building Envelope Modeling Requirements for the Baseline building  
**Appendix G Section Reference:** Tables G3.4-1 to G3.4-8  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:** None  

**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** Tables G3.4-1 to G3.4-8 
**Functions:** Zone Conditioning Catergory, Opaque Surface Type, Surface Conditioning Catergory

## Rule Logic:   

- Get building climate zone: ```climate_zone = B_RMR.weather.climate_zone```  

  - Get heated space criteria: ```system_min_heating_output = data_lookup(table_3_2,climate_zone)```  

- For each building segment in the Baseline model: ```for building_segment_b in B_RMR.building.building_segments:```  

  - For each HVAC system in building segment: ```for hvac_system_b in building_segment_b.heating_ventilation_air_conditioning_systems:```  

    - Check if the system meets the criteria for serving directly conditioned space: ```if ( hvac_system_b.simulation_result_sensible_cool_capacity >= 3.4 ) OR ( hvac_system_b.simulation_result_heat_capacity >= system_min_heating_output ):```  

      - Save all spaces served by the system as conditioned spaces: ```for zone_b in hvac_system_b.zones_served: directly_conditioned_spaces_b.append(space_b for space in zone_b.spaces)```  

    - Else check if the system meets the criteria for serving semiheated space: ```else if ( hvac_system_b.simulation_result_heat_capacity >= 3.4 ):```  

      - Save all spaces served by the system as semiheated spaces: ```for zone_b in hvac_system_b.zones_served: semiheated_spaces_b.append(space_b for space in zone_b.spaces)```  

    - Else save all spaces served by the system as unconditioned spaces: ```else: for zone_b in hvac_system_b.zones_served: unconditioned_spaces_b.append(space_b for space in zone_b.spaces)```  

  - For each thermal block in building segment: ```for thermal_block_b in building_segment_b:```

    - For each zone in thermal block: ```for zone_b in thermal_block_b.zones:```  

      - For each space in zone: ```for space_b in zone_b.spaces:```  

        - If the space is not served by any hvac system: ```if ( space_b not in directly_conditioned_spaces_b ) AND ( space_b not in semiheated_spaces_b ) AND ( space_b not in unconditioned_spaces_b ):```  

          - For each surface in space: ```for surface_b in space_b.surfaces:```  

            - Check if surface is interior, get the adjacent space: ```if surface_b.adjacent_to == "INTERIOR": surface_adjacent_space_b = match_data_element(B_RMR, spaces, surface_b.adjacent_space_id)```  

              - If the adjacent space is directly conditioned, add the product of the U-factor and surface area to the directly conditioned type: ```if surface_adjacent_space_b in directly_conditioned_spaces_b: directly_conditioned_product_sum += sum( fenestration.glazed_area * fenestration.glazed_u_factor + fenestration.opaque_area * fenestration.opaque_u_factor for fenestration in surface_b.fenestration_subsurfaces ) + ( surface_b.area - sum( fenestration.glazed_area + fenestration.opaque_area for fenestration in surface_b.fenestration_subsurfaces ) * surface.construction.u_factor```  

              - Else, add the product of the U-factor and surface area to the other type: ```else: other_product_sum += sum( ( fenestration.glazed_area * fenestration.glazed_u_factor + fenestration.opaque_area * fenestration.opaque_u_factor ) for fenestration in surface_b.fenestration_subsurfaces ) + ( surface_b.area - sum( ( fenestration.glazed_area + fenestration.opaque_area ) for fenestration in surface_b.fenestration_subsurfaces ) ) * surface.construction.u_factor```  

            - Check if surface is exterior, add the product of the U-factor and surface area to the other type: ```else if surface.adjacent_to == "EXTERIOR": other_product_sum += sum( ( fenestration.glazed_area * fenestration.glazed_u_factor + fenestration.opaque_area * fenestration.opaque_u_factor ) for fenestration in surface_b.fenestration_subsurfaces ) + ( surface_b.area - sum( ( fenestration.glazed_area + fenestration.opaque_area ) for fenestration in surface_b.fenestration_subsurfaces ) ) * surface.construction.u_factor```  

          - Determine if the space is indirectly conditioned: ```if directly_conditioned_product_sum > other_product_sum: indirectly_conditioned_spaces_b.append(space)```  

          - Else, the space is unconditioned: ```else: unconditioned_spaces_b.append(space)```  

- For each building segment in the Baseline model: ```for building_segment_b in B_RMR.building.building_segments:```  

  - For each thermal block in building segment: ```for thermal_block_b in building_segment_b.thermal_blocks:```  

    - For each zone in thermal block: ```for zone_b in thermal_block_b.zones:```  

      - For each space in thermal zone: ```for space_b in zone_b.spaces:```  

        - For each surface in space: ```for surface_b in space_b.surfaces:```  

          - If the surface is roof or ceiling, get surface adjacency: ```if 0 <= surface_b.tilt < 60: surface_adjacency_b = surface_b.adjacent_to```  

            - If the space is directly or indirectly conditioned: ```if ( space_b in directly_conditioned_spaces_b ) OR ( space_b in indirectly_conditioned_spaces_b ):```  

              - If the surface adjacency is exterior, get baseline construction from Table G3.4-1 to G3.4-8 based on climate zone for Residential or Nonresidential: ```if surface_adjacency_b == "EXTERIOR": target_u_factor = data_lookup(table_G3_4,climate_zone,space_category_lookup(space_b.lighting_space_type),"Roofs")```  

              - Else if surface adjacency is interior, get the adjacent space: ```else if surface_adjacency_b == "INTERIOR": adjacent_space_b = match_data_element(B_RMR, spaces, surface_b.adjacent_space_id)```  

                - If the adjacent space is conditioned, the surface is unregulated and shall have the same properties as P-RMR: ```if ( adjacent_space_b in directly_conditioned_spaces_b ) OR ( adjacent_space_b in indirectly_conditioned_spaces_b ): target_surface_p = match_data_element(P_RMR, surfaces, surface_b.id)```  

                  - Get baseline construction from P-RMR: ```target_u_factor = target_surface_p.construction.u_factor```  

                - If the adjacent space is semiheated or unconditioned, get baseline construction from Table G3.4-1 to G3.4-8 based on climate zone for semiheated spaces: ```if ( adjacent_space_b in semiheated_spaces_b ) OR ( adjacent_space_b in unconditioned_spaces_b ): target_u_factor = data_lookup(table_G3_4,climate_zone,"Semiheated","Roofs")```  

              - Else, surface adjacency is ground, the surface is unregulated and shall have the same properties as P-RMR: ```else: target_surface_p = match_data_element(P_RMR, surfaces, surface_b.id)```  

                - Get baseline construction from P-RMR: ```target_u_factor = target_surface_p.construction.u_factor```  

            - Else if the space is semiheated: ```else if space_b in semiheated_spaces_b:```  

              - If the surface adjacency is exterior, get baseline construction from Table G3.4-1 to G3.4-8 based on climate zone for semiheated spaces: ```if surface_adjacency_b == "EXTERIOR": target_u_factor = data_lookup(table_G3_4,climate_zone,"Semiheated","Roofs")```  

              - Else if the surface adjacency is interior, get the adjacent space: ```else if surface_adjacency_b == "INTERIOR", adjacent_space_b = match_data_element(B_RMR, spaces, surface_b.adjacent_space_id)```  

                - If the adjacent space is conditioned, get baseline construction from Table G3.4-1 to G3.4-8 based on climate zone for semiheated spaces: ```if ( adjacent_space_b in directly_conditioned_spaces_b ) OR ( adjacent_space_b in indirectly_conditioned_spaces_b ): target_u_factor = data_lookup(table_G3_4,climate_zone,"Semiheated","Roofs")```  

                - Else if the adjacent space is semiheated or unconditioned, the surface is unregulated and shall have the same properties as P-RMR: ```else if ( adjacent_space_b in semiheated_spaces_b ) OR ( adjacent_space_b in unconditioned_spaces_b ): target_surface_p = match_data_element(P_RMR, surfaces, surface_b.id)```  

                  - Get baseline construction from P-RMR: ```target_u_factor = target_surface_p.construction.u_factor```  

              - Else, surface adjacency is ground, the surface is unregulated and shall have the same properties as P-RMR: ```else: target_surface_p = match_data_element(P_RMR, surfaces, surface_b.id)```  

                - Get baseline construction from P-RMR: ```target_u_factor = target_surface_p.construction.u_factor```  

            - Else, the space is unconditioned: ```else:```  

              - If the surface adjacency is exterior, the surface is unregulated and shall have the same properties as P-RMR: ```if surface_adjacency_b == "EXTERIOR": target_surface_p = match_data_element(P_RMR, surfaces, surface_b.id)```  

                - Get baseline construction from P-RMR: ```target_u_factor = target_surface_p.construction.u_factor```  

              - Else if the surface adjacency is interior, get the adjacent space: ```else if surface_adjacency_b == "INTERIOR": adjacent_space_b = match_data_element(B_RMR, spaces, surface_b.adjacent_space_id)```  

                - If the adjacent space is conditioned, get baseline construction from Table G3.4-1 to G3.4-8 based on climate zone for semiheated spaces: ```if adjacent_space_b in conditioned_spaces_b: target_u_factor = data_lookup(table_G3_4,climate_zone,"Semiheated","Roofs")```  

                - Else, the surface is unregulated and shall have the same properties as P-RMR: ```else: target_surface_p = match_data_element(P_RMR, surfaces, surface_b.id)```  

                  - Get baseline construction from P-RMR: ```target_u_factor = target_surface_p.construction.u_factor```  

              - Else, surface adjacency is ground, the surface is unregulated and shall have the same properties as P-RMR: ```else: target_surface_p = match_data_element(P_RMR, surfaces, surface_b.id)```  

                - Get baseline construction from P-RMR: ```target_u_factor = target_surface_p.construction.u_factor```  

          **Rule Assertion:** Baseline roof and ceiling construction modeled matches Normative Appendix A for roof insulation entirely above deck or P-RMR: ```surface_b.construction.u_factor == target_u_factor```  
