
# Envelope - Rule 5-6  

**Rule ID:** 5-6  
**Rule Description:** Opaque Assemblies used for new buildings, existing buildings, or additions shall conform with assemblies detailed in Appendix A and shall match the appropriate assembly maximum U-factors in Tables G3.4-1 through G3.4-8: Slab-on-grade floors shall match the F-factor for unheated slabs from the same tables (A6)..  
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

- For each building segment in the Baseline model: ```for building_segment_baseline in B_RMR.building.building_segments:```  

  - For each thermal_block from building segment: ```for thermal_block_baseline in building_segment_baseline.thermal_blocks:```  

  - For each zone in thermal block: ```zone_baseline in thermal_block_baseline.zones:```  

  - For each space in thermal zone: ```space_baseline in zone_baseline.spaces:```  

    - Get space conditioning type: ```space_conditioning_type_baseline = space_baseline.conditioning_type```  

      - Get baseline contruction from Table G3.4-1 to G3.4-8 based on space conditioning type, status type and function type: ```surface_performance_target = data_lookup(climate_zone,space_conditioning_type_baseline,"Slab-on-Grade Floors")```  

    - For each surface in space: ```for surface_baseline in space_baseline.surfaces:```  

      - Get the surface construction if the surface is slab-on-grade floor: ```if ( surface_baseline.classification == "FLOOR" ) AND ( surface_baseline.adjacent_to == "GROUND" ): surface_construction_baseline = surface_baseline.construction```  

      - Get the performance values for the construction: ```surface_performance_value_baseline = surface_construction_baseline.f_factor```  (Note XC, assumes for slab on grade, RMR reports f-factor not u-factor)

    **Rule Assertion:** Baseline slab-on-grade floor consruction modeled matches Table G3.4-1 to G3.4-8: ```surface_performance_value_baseline == surface_performance_target```  
