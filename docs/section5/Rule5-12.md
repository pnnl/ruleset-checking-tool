
# Envelope - Rule 5-12  

**Rule ID:** 5-12  
**Rule Description:**  Skylight area shall be equal to that in the proposed design or 3%, whichever is smaller. If the skylight area of the proposed design is greater than 3%, baseline skylight area shall be decreased by an identical percentage in all roof components in which skylights are located to reach 3%.  
**Rule Assertion:** Baseline RMR = expected value  
**Appendix G Section:** Section G3.1-5(e) Building Envelope Modeling Requirements for the Baseline building  
**Appendix G Section Reference:** None  

**Applicability:** All required data elements exist for P_RMR and B_RMR  
**Applicability Checks:**  None  

**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  

## Rule Logic:  

- For each building segment in the Proposed model: ```for building_segment_proposed in P_RMR.building.building_segments:```  

  - For each thermal_block in building segment: ```for thermal_block_proposed in building_segment_proposed.thermal_blocks:```  

  - For each zone in thermal block: ```for zone_proposed in thermal_block_proposed.zones:```  

  - For each space in thermal zone: ```for space_proposed in zone_proposed.spaces:```  

    - Get surfaces in space: ```for surface_proposed in space_proposed.surfaces:```  

    - Check if surface is roof: ```if ( surface_proposed.classification == "CEILING" ) AND ( surface_proposed.adjacent_to == "AMBIENT" ): roof_surface_proposed = surface_proposed```  

      - Calculate the total skylight area in surface: ```skylight_area_proposed = sum(skylight.area for skylight in roof_surface_proposed.fenestration_subsurfaces)```  

      - Calculate the building total roof area: ```total_roof_area_proposed += roof_surface_proposed.area```  

      - Calculate the building total skylight area: ```total_skylight_area_proposed += skylight_area_proposed```  

      - Calculate the building skylight to roof ratio: ```skylight_roof_ratio_proposed = total_skylight_area_proposed / total_roof_area_proposed```  

    - Get matching space from Baseline RMR: ```space_baseline = match_data_element(B_RMR, spaces, space_proposed.name)```  (Note XC, getting space in baseline, or the surface or subsurface name will match? do we need to check skylight one to one, or only checking total skylight area in B_RMR?)

      - Get surfaces in space: ```for surface_baseline in space_proposed.surfaces:```  

      - Check if surface is roof: ```if ( surface_baseline.classification == "CEILING" ) AND ( surface_baseline.adjacent_to == "AMBIENT" ): roof_surface_baseline = surface_baseline```  

      - Calculate the total skylight area in Baseline RMR surface: ```skylight_area_baseline = sum(skylight.area for skylight in roof_surface_baseline.fenestration_subsurfaces)```  

      **Rule Assertion:** Baseline skylight area is equal to that in the Proposed design or 3%, whichever is smaller.  

      - Case 1: The skylight to roof ratio in the Proposed model is less than or equal to 3%: ```if skylight_roof_ratio_proposed <= 3%: skylight_area_baseline == skylight_area_proposed```  

      - Case 2: The skylight to roof ratio in the Proposed model is more than 3%: ```else: skylight_area_baseline == skylight_area_proposed * ( 3% / skylight_roof_ratio_proposed )```  
