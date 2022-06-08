
# Lighting - Rule 6-7

**Rule ID:** 6-7  
**Rule Description:** User building is modeled with daylighting controls directly or through schedule adjustments.  
**Appendix G Section:** Section 6 Lighting  
**Appendix G Section Reference:** Section G3.1-6(h) Lighting: Modeling Requirements for the Proposed design  

**Applicability:** All required data elements exist for U_RMR  
**Applicability Checks:** None  
**Manual Check:** Yes  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  
## Rule Logic: 

- Check if each zone has window or skylight in the building segment in the User model: `For zone_u in U_RMR...zones:`

  - For each surfaces in zone: `surface_u in zone_u.surfaces`

    - Check if surface is exterior: `if surface_u.adjacent_to == "EXTERIOR":`

      - Check if surface has any subsurface that is not door, set daylight flag as TRUE: `if ( subsurface.classification != "DOOR" for subsurface in surface_u.subsurfaces ): daylight_flag_u == TRUE`

  - For each space in zone: `space_u in zone_u.spaces:`

    - Get interior_lighting in space: `interior_lighting_u = space_u.interior_lighting`

      - Check if any interior_lighting has daylight control: `if ( lighting.daylighting_control_type != "NONE" for lighting in interior_lighting_u ): has_daylight_control_flag == TRUE`

    **Rule Assertion:** For each zone in the User model:

    - Case 1, if the zone has window or skylight and daylight control, and daylight control is not modeled using schedule: `if ( daylight_flag_u == TRUE ) AND ( has_daylight_control_flag == TRUE ) AND ( NOT interior_lighting_u.are_schedules_used_for_modeling_daylighting_control ): UNDETERMINED and raise_warning "SOME OF THE SPACES IN ZONE ARE MODELED WITH WINDOW OR SKYLIGHT AND SOME OF THE SPACES IN ZONE ARE MODELED WITH DAYLIGHTING CONTROL DIRECTLY THROUGH SIMULATION. VERIFY IF THE MANDATORY LIGHTING CONTROL REQUIREMENTS ARE MODELED CORRECTLY IN ZONE."`

    - Case 2, else if the zone has window or skylight and daylight control, and daylight control is modeled using schedule: `if ( daylight_flag_u == TRUE ) AND ( has_daylight_control_flag == TRUE ) AND ( interior_lighting_u.are_schedules_used_for_modeling_daylighting_control ): UNDETERMINED and raise_warning "SOME OF THE SPACES IN ZONE ARE MODELED WITH WINDOW OR SKYLIGHT AND SOME OF THE SPACES IN ZONE ARE MODELED WITH DAYLIGHTING CONTROL WITH SCHEDULE. VERIFY IF SCHEDULE ADJUSTMENT IS MODELED CORRECTLY."`

    - Case 3, else if the zone has window or skylight and daylight control is not modeled:  `else if ( daylight_flag_u == TRUE ) AND ( has_daylight_control_flag == FALSE ): FAIL and raise_warning "SOME OF THE SPACES IN ZONE ARE MODELED WITH FENESTRATION BUT NO DAYLIGHTING CONTROLS. THE DESIGN MUST INCLUDE MANDATORY DAYLIGHTING CONTROLS UNLESS ANY OF THE EXCEPTIONS TO 90.1 SECTION 9.4.1.1(E) APPLY."`

    - Case 4, else if the zone does not have window or skylight and daylight control is modeled: `else if ( daylight_flag_u == FALSE ) AND ( has_daylight_control_flag == TRUE ): FAIL`

    - Case 5, else, the zone does not have window or skylight and no daylight control is modeled: `else: PASS`

**Notes:**
  1. Updated the Rule ID from 6-12 to 6-8 on 6/3/2022
  2. Updated the Rule ID from 6-8 to 6-7 on 6/8/2022
  3. The rule has been written to apply to user RMR, it should instead be implemented to apply to P-RMR- should discuss


**[Back](../_toc.md)**
