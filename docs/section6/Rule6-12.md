
# Lighting - Rule 6-12

**Rule ID:** 6-12  
**Rule Description:** Proposed building is modeled with daylighting controls  
**Appendix G Section:** Section 6 Lighting  
**Appendix G Section Reference:** Section G3.1-6(h) Lighting: Modeling Requirements for the Proposed design  

**Applicability:** All required data elements exist for U_RMR  
**Applicability Checks:** None  
**Manual Check:** Yes  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  
## Rule Logic: 

- Check if each zone has window or skylight in the building segment in the User model: `For zone_p in U_RMR...zones:`

  - For each surfaces in zone: `surface_p in zone_p.surfaces`

    - Check if surface is exterior: `if surface_p.adjacent_to == "EXTERIOR":`

      - Check if surface has any subsurface that is not door, set daylight flag as TRUE: `if ( subsurface.classification != "DOOR" for subsurface in surface_p.subsurfaces ): daylight_flag_p == TRUE`

  - For each space in zone: `space_p in zone_p.spaces:`

    - Get interior_lighting in space: `interior_lighting_p = space_p.interior_lighting`

      - Check if any interior_lighting has daylight control: `if ( lighting.daylighting_control_type != "NONE" for lighting in interior_lighting_p ): has_daylight_control_flag == TRUE`

    **Rule Assertion:** For each zone in the User model:

    - Case 1, if the zone has window or skylight and daylight control is modeled: `if ( daylight_control_flag == TRUE ) AND ( has_daylight_control_flag ) == TRUE: CAUTION and raise_warning "SOME OF THE SPACES IN ZONE ARE MODELED WITH WINDOW OR SKYLIGHT AND SOME OF THE SPACES IN ZONE ARE MODELED WITH DAYLIGHTING CONTROL. VERIFY IF THE MANDATORY LIGHTING CONTROL REQUIREMENTS ARE MODELED CORRECTLY IN ZONE."`

    - Case 2, else if the zone has window or skylight and daylight control is not modeled:  `else if ( daylight_control_flag == TRUE ) AND ( has_daylight_control_flag == FALSE ): FAIL and raise_warning "SOME OF THE SPACES IN ZONE ARE MODELED WITH FENESTRATION BUT NO DAYLIGHTING CONTROLS. THE DESIGN MUST INCLUDE MANDATORY DAYLIGHTING CONTROLS UNLESS ANY OF THE EXCEPTIONS TO 90.1 SECTION 9.4.1.1(E) APPLY."`

    - Case 3, else if the zone does not have window or skylight and daylight control is modeled: `else if ( daylight_control_flag == FALSE ) AND ( has_daylight_control_flag == TRUE ): FAIL`

    - Case 4, else, the zone does not have window or skylight and no daylight control is modeled: `else: PASS`

**[Back](../_toc.md)**
