
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

- For each building segment in the Baseline model: ```for building_segment_b in B_RMR.building.building_segments:```  

  - For each thermal block in building segment: ```for thermal_block_b in building_segment_b:```

    - For each zone in thermal block: ```for zone_b in thermal_block_b.zones:```  

      - Determine the zone  conditioning catergory ```zone_b.zone_conditioning_catergory = #function.zone_conditioning_catergory```
    - For each surface in zone: ```for surface_b in zone_b.surface:```  
    - Determine the surface type  
    - for each surface = roof, determine the surface conditioning catergory  
    - for exterior roof surfaces, verify the U factor
    -   


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
