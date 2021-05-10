
# Envelope - Rule 5-14  

**Rule ID:** 5-14  
**Rule Description:**  Skylight SHGC properties shall match the appropriate requirements in Tables G3.4-1 through G3.4-8 using the value and the applicable skylight percentage.  
**Rule Assertion:** Baseline RMR = expected value  
**Appendix G Section:** Section G3.1-5(e) Building Envelope Modeling Requirements for the Baseline building  
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

    - Get surface in space: ```for surface_baseline in space_baseline.surfaces:```  

      - Check if surface is roof: ```if ( surface_baseline.classification == "CEILING" ) AND ( surface_baseline.adjacent_to == "AMBIENT" ): roof_surface_baseline = surface_baseline```  

        - Calculate the total roof area: ```total_roof_area_baseline += roof_surface_baseline.area```  

        - Get the U-factor for skylightss: ```skylight_performance_value_baseline.append(skylight.solar_heat_gain_coefficient for skylight in roof_surface_baseline.fenestration_subsurfaces)```  

        - Calculate the total skylight area: ```total_skylight_area_baseline += sum(skylight.area for skylight in roof_surface_baseline.fenestration_subsurfaces)```  

        - Calculate the skylight to roof ratio: ```skylight_roof_ratio_baseline = total_skylight_area_baseline / total_roof_area_baseline```  

    - Get space conditioning type: ```space_conditioning_type_baseline = space_baseline.conditioning_type```  

      - Get baseline contruction for skylight from Table G3.4-1 to G3.4-8 based on climate zone, space conditioning type, skylight to roof ratio and function type: ```skylight_performance_target = data_lookup(table_G3_4,climate_zone,space_conditioning_type_baseline,skylight_roof_ratio_baseline,"Skylight", SHGC_all)```  

      **Rule Assertion:** Baseline skylight SHGC modeled matches Table G3.4-1 to G3.4-8: ```skylight_shgc == skylight_performance_target for skylight_shgc in skylight_performance_value_baseline```  
