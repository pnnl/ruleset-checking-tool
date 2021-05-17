
# Envelope - Rule 5-4

**Rule ID:** 5-4  
**Rule Description:** Opaque Assemblies used for new buildings, existing buildings, or additions shall conform with assemblies detailed in Appendix A and shall match the appropriate assembly maximum U-factors in Tables G3.4-1 through G3.4-8: Above-grade walls—Steel-framed (A3.3).  
**Rule Assertion:** Baseline RMR Surface:U_factor = expected value  
**Appendix G Section:** Section G3.1-5(b) Building Envelope Modeling Requirements for the Baseline building  
**Appendix G Section Reference:** Tables G3.4-1 to G3.4-8  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  

  1. Baseline space conditioning category (conditioned, semiheated, unconditioned), residential vs non-residential occupancy type and surface type (wall vs floor vs roof) are determined correctly  

**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** Tables G3.4-1 to G3.4-8  

## Rule Logic:  

- **Applicability Check 1:** Baseline space conditioning category (conditioned, semiheated, unconditioned), residential vs non-residential occupancy type and surface type (wall vs floor vs roof) are determined correctly.  

- Get building climate zone: ```climate_zone = B_RMR.weather.climate_zone```  

- For each building segment in the Baseline model: ```for building_segment_b in B_RMR.building.building_segments:```  

  - For each thermal_block in building segment: ```for thermal_block_b in building_segment_b.thermal_blocks:```  

  - For each zone in thermal block: ```for zone_b in thermal_block_b.zones:```  

  - For each space in thermal zone: ```for space_b in zone_b.spaces:```  

    - Get space category (residential or non-residential): ```space_category_b = space_category_lookup(space_b.lighting_space_type)```  

    - Get space conditioning type: ```space_conditioning_type_b = space_b.conditioning_type```  

    - Get baseline construction from Table G3.4-1 to G3.4-8 based on climate zone, space category, space conditioning type and function type: ```surface_performance_target_u_factor, surface_performance_target_layers = data_lookup(table_G3_4,climate_zone,space_category_b,space_conditioning_type_b,"Walls, Above-Grade")```  

    - For each surface in space: ```for surface_b in space_b.surfaces:```  

      - Get the surface construction if the surface is above-grade wall: ```if ( 60<= surface_b.tilt <= 90 ) AND ( surface_b.adjacent_to == "AMBIENT" ): surface_construction_b = surface_b.construction```  

      - Get the surface construction input option: ```surface_input_option_b = surface_construction_b.surface_construction_input_option```  

      - Case 1. If the input option is "layer-by-layer", get the layers of the construction: ```if surface_input_option_b == "layer-by-layer": construction_layers_b = surface_construction_b.layers```  

        **Rule Assertion:** Baseline above-grade wall construction modeled matches Normative Appendix A for above-grade steel-framed walls: ```construction_layers_b == surface_performance_target_layers```  

      - Case 2. If the input option is "simplified (R-value)" and u-factor is reported: ```else if surface_construction_b.u_factor: construction_u_factor = surface_construction_b.u_factor```  

        **Rule Assertion:** Baseline above-grade wall construction modeled matches Table G3.4-1 to G3.4-8: ```construction_u_factor == surface_performance_target_u_factor```  

      - Case 3. If the input option is "simplified (R-value)" and r-value reported: ```else if surface_construction_b.r_value: construction_r_value = surface_construction_b.r_value```  

        **Rule Assertion:** Baseline above-grade wall construction modeled matches Table G3.4-1 to G3.4-8: ```construction_r_value == 1 / surface_performance_target_u_factor```  (Note XC, assumes the R-value includes air film?)
