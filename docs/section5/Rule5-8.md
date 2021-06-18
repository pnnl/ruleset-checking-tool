
# Envelope - Rule 5-8  

**Rule ID:** 5-8  
**Rule Description:**  Fenestration U-factors for new buildings, existing buildings, and additions shall match the appropriate requirements in Tables G3.4-1 through G3.4-8 for the applicable glazing percentage for Uall.  
**Rule Assertion:** Baseline RMR = expected value  
**Appendix G Section:** Section G3.1-5(d) Building Envelope Modeling Requirements for the Baseline building  
**Appendix G Section Reference:** Tables G3.4-1 to G3.4-8  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  None  

**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** Tables G3.4-1 to G3.4-8  

## Rule Logic:  

- Get building climate zone: ```climate_zone = B_RMR.weather.climate_zone```  

- For each building segment in the Baseline model: ```for building_segment_baseline in B_RMR.building.building_segments:```  

  - For each thermal_block in building segment: ```for thermal_block_baseline in building_segment_baseline.thermal_blocks:```  

  - For each zone in thermal block: ```for zone_baseline in thermal_block_baseline.zones:```  

  - For each space in thermal zone: ```for space_baseline in zone_baseline.spaces:```  

    - Get surfaces in space: ```for surface_baseline in space_baseline.surfaces:```  

      - Check if surface is exterior wall: ```if ( surface_baseline.classification == "WALL" ) AND ( surface_baseline.adjacent_to == "AMBIENT" ): wall_surface_baseline = surface_baseline```  

        - Calculate the total wall area: ```total_wall_area_baseline += wall_surface_baseline.area```  

        - Get the U-factor for vertical glazings: ```window_performance_value_baseline.append(window.u_factor for window in wall_surface_baseline.fenestration_subsurfaces)```  

        - Calculate the total vertical glazing area: ```total_window_area_baseline += sum(window.area for window in wall_surface_baseline.fenestration_subsurfaces)```  

        - Calculate the window to wall ratio: ```window_wall_ratio_baseline = total_window_area_baseline / total_wall_area_baseline```  (Note XC, can we get the WWR and skylight roof ratio from Rule 5-7 instead of calculating it here?)

    - Get space conditioning type: ```space_conditioning_type_baseline = space_baseline.conditioning_type```  

      - Get baseline contruction for vertical glazing from Table G3.4-1 to G3.4-8 based on climate zone, space conditioning type, window wall ratio and function type: ```window_performance_target = data_lookup(table_G3_4,climate_zone,space_conditioning_type_baseline,window_wall_ratio_baseline,"Vertical Glazing", "U_all")```  

      **Rule Assertion:** Baseline vertical glazing u_factor modeled matches Table G3.4-1 to G3.4-8: ```window_u_factor == window_performance_target for window_u_factor in window_performance_value_baseline```  
