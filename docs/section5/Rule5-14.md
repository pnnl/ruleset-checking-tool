
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

- For each building segment in the Baseline model: ```for building_segment_b in B_RMR.building.building_segments:```  

  - Calculate the skylight to roof ratio: ```skylight_roof_ratio_b = opening_surface_ratio_calc(building_segment_b, "skylight")```  (Note XC, pending confirmation on whether the ratio is per building segment or building)

  - For each thermal_block in building segment: ```for thermal_block_b in building_segment_b.thermal_blocks:```  

  - For each zone in thermal block: ```for zone_b in thermal_block_b.zones:```  

  - For each space in thermal zone: ```for space_b in zone_b.spaces:```  

    - Get space category (residential or non-residential): ```space_category_b = space_category_lookup(space_b.lighting_space_type)```  

    - Get space conditioning type: ```space_conditioning_type_b = space_b.conditioning_type```  

    - If space is conditioned or semiheated, get baseline SHGC for skylight from Table G3.4-1 to G3.4-8 based on climate zone, space category, space conditioning type, skylight to roof ratio and function type: ```skylight_performance_target = data_lookup(table_G3_4,climate_zone,space_category_b,space_conditioning_type_b,skylight_roof_ratio_b,"Skylight", SHGC_all)```  

    - For each surface in space: ```for surface_b in space_b.surfaces:```

      - Check if surface is roof: ```if ( surface_b.classification == "CEILING" ) AND ( 0 <= surface_b.tilt < 60) AND ( surface_b.adjacent_to == "AMBIENT" ): roof_surface_b = surface_b```  

      - For each skylight in roof, get SHGC: ```for skylight_b in roof_surface_b.fenestration_subsurfaces: skylight_shgc_b = skylight_b.solar_heat_gain_coefficient```  

        **Rule Assertion:** Baseline SHGC modeled for each skylight matches Table G3.4-1 to G3.4-8: ```skylight_shgc_b == skylight_performance_target```  (Note XC, assuming unconditioned spaces do not follow Table G3.4 and will have a different rule to compare both area and thermal performance)
