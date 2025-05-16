
# Lighting - Rule 6-7

**Rule ID:** 6-7  
**Rule Description:** Proposed building is modeled with daylighting controls directly or through schedule adjustments.  
**Appendix G Section:** Section 6 Lighting  
**Appendix G Section Reference:** Section G3.1-6(h) Lighting: Modeling Requirements for the Proposed design  

**Applicability:** All required data elements exist for P_RMR  
**Applicability Checks:** None  
**Manual Check:** Yes  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  
## Rule Logic: 
- List lighting space types that have no daylighting control requirements: `not_applicable_space_types = ["DORMITORY_LIVING_QUARTERS", "FIRE_STATION_SLEEPING_QUARTERS", "HEALTHCARE_FACILITY_OPERATING_ROOM", "OUTPATIENT_HEALTH_CARE_FACILITIES_CLASS_1_IMAGING_ROOMS", "DWELLING_UNIT", "GUEST_ROOM", "STORAGE_ROOM_SMALL", "PARKING_AREA_INTERIOR"]`

- Check if each zone has window or skylight in the building segment in the Proposed model: `For zone_p in P_RMR...zones:`

  - For each surfaces in zone: `surface_p in zone_p.surfaces`

    - Check if surface is exterior: `if surface_p.adjacent_to == "EXTERIOR":`

      - Check if surface has any subsurface that is not door, set daylight flag as TRUE: `if ( subsurface.classification != "DOOR" for subsurface in surface_p.subsurfaces ): daylight_flag_p == TRUE`

  - For each space in zone: `space_p in zone_p.spaces:`
  
    - Check if the lighting space type is in the list of not applicable space types: `if space_p.lighting_space_type in not_applicable_space_types: continue`

    - Get interior_lighting in space: `interior_lighting_p = space_p.interior_lighting`

      - Check if any interior_lighting has daylight control: `if ( lighting.daylighting_control_type != "NONE" for lighting in interior_lighting_p ): has_daylight_control_flag == TRUE`
      
      - Check if any interior_lighting with daylight control has it modeled using schedule adjustment: `if (lighting.are_schedules_used_for_modeling_daylighting_control==TRUE for lighting in interior_lighting_p): daylight_schedule_adjustment_flag = TRUE`
    
**Rule Assertion:** For each zone in the Proposed model:

    - Case 1, if the zone has window or skylight and daylight control, and daylight control is not modeled using schedule: `if ( daylight_flag_p == TRUE ) AND ( has_daylight_control_flag == TRUE ) AND ( NOT daylight_schedule_adjustment_flag ): UNDETERMINED and raise_warning "SOME OF THE SPACES IN ZONE ARE MODELED WITH WINDOW(S) AND/OR SKYLIGHT(S) AND HAVE DAYLIGHTING CONTROLS MODELED EXPLICITLY IN THE SIMULATION TOOL. VERIFY THAT THE MANDATORY LIGHTING CONTROL REQUIREMENTS ARE MET."`

    - Case 2, else if the zone has window or skylight and daylight control, and daylight control is modeled using schedule: `if ( daylight_flag_p == TRUE ) AND ( has_daylight_control_flag == TRUE ) AND ( daylight_schedule_adjustment_flag ): UNDETERMINED and raise_warning "SOME OF THE SPACES IN ZONE ARE MODELED WITH WINDOW(S) AND/OR SKYLIGHT(S) AND HAVE DAYLIGHTING CONTROLS MODELED VIA SCHEDULE ADJUSTMENT. VERIFY THAT THE MANDATORY LIGHTING CONTROL REQUIREMENTS ARE MET, AND THAT THE SUPPORTING DOCUMENTATION IS PROVIDED FOR THE SCHEDULE ADJUSTMENT."`

    - Case 3, else if the zone has window or skylight and daylight control is not modeled:  `else if ( daylight_flag_p == TRUE ) AND ( has_daylight_control_flag == FALSE ): FAIL and raise_warning "SOME OF THE SPACES IN ZONE ARE MODELED WITH FENESTRATION BUT NO DAYLIGHTING CONTROLS. THE DESIGN MUST INCLUDE MANDATORY DAYLIGHTING CONTROLS UNLESS ANY OF THE EXCEPTIONS TO 90.1 SECTION 9.4.1.1(E) APPLY."`

    - Case 4, else if the zone does not have window or skylight and daylight control is modeled: `else if ( daylight_flag_p == FALSE ) AND ( has_daylight_control_flag == TRUE ): FAIL`

    - Case 5, else, the zone does not have window or skylight and no daylight control is modeled: `else: PASS`

**Notes:**
  1. Updated the Rule ID from 6-12 to 6-8 on 6/3/2022
  2. Updated the Rule ID from 6-8 to 6-7 on 6/8/2022
  3. The rule has been written to apply to user RMR, it should instead be implemented to apply to P-RMR- should discuss


**[Back](../_toc.md)**
