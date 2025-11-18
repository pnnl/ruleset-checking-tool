
# Lighting - Rule 6-7

**Rule ID:** 6-7  
**Rule Description:** Proposed building is modeled with daylighting controls directly or through schedule adjustments.  
**Appendix G Section:** Section 6 Lighting  
**Appendix G Section Reference:** Section G3.1-6(h) Lighting: Modeling Requirements for the Proposed design  

**Applicability:** All required data elements exist for P_RMD  
**Applicability Checks:** None  

**Manual Check:** Yes  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  
## Rule Logic: 

- Check if each zone has window or skylight in the building segment in the Proposed model: `For zone_p in P_RMD...zones:`
- 
  - Initialize plenum/crawlspace/interstitial space lighting flag as FALSE: `plenum_crawl_interstitial_space_lighting_flag = FALSE`

  - For each surfaces in zone: `surface_p in zone_p.surfaces`

    - Check if surface is exterior: `if surface_p.adjacent_to == "EXTERIOR":`

      - Check if surface has any subsurface that is not door, set daylight flag as TRUE: `if ( subsurface.classification != "DOOR" for subsurface in surface_p.subsurfaces ): daylight_flag_p == TRUE`

  - For each space in zone: `space_p in zone_p.spaces:`

    - Get total lighting power density: `total_space_LPD = sum(interior_lighting.power_per_area for interior_lighting in space_p.interior_lighting)`

    - Set plenum/crawl/interstitial space lighting flag based on space function and sum of lighting power: `if total_space_LPD > 0 and space_p.function in [PLENUM, CRAWL_SPACE, INTERSTITIAL_SPACE]: plenum_crawl_interstitial_space_lighting_flag = TRUE`

    - Get interior_lighting in space: `interior_lighting_p = space_p.interior_lighting`  
    
    - Check if any interior_lighting has daylight control: `if ( lighting.daylighting_control_type != "NONE" for lighting in interior_lighting_p ): has_daylight_control_flag == TRUE`
      
    - Check if any interior_lighting with daylight control has it modeled using schedule adjustment: `if (lighting.are_schedules_used_for_modeling_daylighting_control==TRUE for lighting in interior_lighting_p): daylight_schedule_adjustment_flag = TRUE`
    
  **Rule Assertion:** For each zone in the Proposed model:

  - Case 1, if the zone has a space that is a plenum, crawl space, or interstitial space with lighting power: `if plenum_crawl_interstitial_space_lighting_flag: UNDETERMINED and raise_warning "The zone contains a space that is a plenum, crawl space, or interstitial space with lighting power. Verify that the design includes mandatory daylighting control requirements, if applicable."`
  
  - Case 2, if the zone has window or skylight and daylight control, and daylight control is not modeled using schedule: `if ( daylight_flag_p == TRUE ) AND ( has_daylight_control_flag == TRUE ) AND ( NOT daylight_schedule_adjustment_flag ): UNDETERMINED and raise_warning "The zone contains space(s) modeled with window(s) and/or skylight(s) and have daylighting controls modeled explicitly in the simulation tool. Verify that the mandatory lighting control requirements are met."`

  - Case 3, else if the zone has window or skylight and daylight control, and daylight control is modeled using schedule: `if ( daylight_flag_p == TRUE ) AND ( has_daylight_control_flag == TRUE ) AND ( daylight_schedule_adjustment_flag ): UNDETERMINED and raise_warning "The zone contains space(s) modeled with window(s) and/or skylight(s) and have daylighting controls modeled via schedule adjustment. Verify that the mandatory lighting control requirements are met, and that the supporting documentation is provided for the schedule adjustment."`

  - Case 4, else if the zone has window or skylight and daylight control is not modeled:  `else if ( daylight_flag_p == TRUE ) AND ( has_daylight_control_flag == FALSE ): FAIL and raise_warning "The zone contains space(s) modeled with window(s) and/or skylight(s) but no daylighting controls. The design must include mandatory daylighting controls unless any of the exceptions to 90.1 Section 9.4.1.1(e) apply."`

  - Case 5, else if the zone does not have window or skylight and daylight control is modeled: `else if ( daylight_flag_p == FALSE ) AND ( has_daylight_control_flag == TRUE ): FAIL`
    
  - Case 6, else, the zone does not have window or skylight and no daylight control is modeled: `else: PASS`

**Notes:**
  1. Updated the Rule ID from 6-12 to 6-8 on 6/3/2022
  2. Updated the Rule ID from 6-8 to 6-7 on 6/8/2022
  3. The rule has been written to apply to user RMR, it should instead be implemented to apply to P-RMR- should discuss
  4. Updated to exclude crawl space, plenum or interstitial space on 9/29/2025


**[Back](../_toc.md)**
