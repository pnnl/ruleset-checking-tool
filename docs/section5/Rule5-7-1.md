# Envelope - Rule 5-7-1 
**Rule ID:** 5-7-1  
**Rule Description:** Baseline WWR should be equal to User WWR or 40%, whichever is smaller.  
**Rule Assertion:** Baseline RMR = expected value  
**Appendix G Section:** Section G3.1-5(c) Building Envelope Modeling Requirements for the Baseline building  
**Appendix G Section Reference:**
- Table G3.1, 5. Building Envelope, Baseline Building Performance, c. Vertical Fenestration Areas
- Table G3.1.1-1

**Data Lookup:** Table G3.1.1-1  
**Evaluation Context:**  Each Data Element  

**Applicability Checks:** 
1. Building has spaces that are NEW, ADDITION or ALTERATION.

**Manual Checks:** None  

## Rule Logic:
- **Applicability Check 1:** `length( [ if _space.status_type for _space in U_RMR...spaces is in [NEW, ADDITION, ALTERATION] ] ) > 0:`  
- For each building segment in the Baseline model: `For _building_segment in B_RMR.building.building_segments:`
    - Get the building area type of the building segment: `_building_area_type = _building_segment.area_type_vertical_fenestration`
    - If building area type exists in Table G3.1.1-1 then get the allowable WWR for the building segment: `if _building_area_type in table_G3_1_1_1: _allowable_baseline_wwr = data_lookup(table_G3_1_1_1, _building_area_type) else: _allowable_baseline_wwr = 0.40`
    - Get thermal_block from building segment: `_thermal_block in building_segment.thermal_blocks:`
    - Get thermal_zone from thermal block: `_thermal_zone in _thermal_block.thermal_zones:`
    - Get space from thermal zone: `_space in _thermal_zone.spaces:`
        - Check that space is either [new, addition or alteration] and [heated and cooled, heated only, or semi-heated]: `if ( _space.status_type in [NEW, ADDITION, ALTERATION] ) AND ( _space.conditioning_type in [HEATED_AND_COOLED, HEATED_ONLY, SEMIHEATED] ):` 
            - Get surface in space: `_surface in space.surfaces:`
                - Check that surface is exterior and vertical: `if ( _surface.adjacent_to in [AMBIENT] ) AND ( 60 <= _surface.tilt <= 90 ): _exterior_vertical_surface = _surface`  
                - Calculate the total fenestration area: `_fenestration_area = sum(_fenestration.area for _fenestration in _exterior_vertical_surface.fenestration_subsurfaces)`
                - Calculate the total surface area: `_surface_area = _surface.area`  
                - Calculate WWR of the building area type and space: `_WWR_baseline = _fenestration_area/_surface_area`
                - Get matching space from User RMR: `_user_space = match_data_element(U_RMR, spaces, _space.name)`
                - Repeat WWR calculation for User RMR space: `_WWR_user = _calculate_wwr(_user_space)`
                - **Rule Assertion:** `_WWR_baseline == min(_WWR_user, _allowable_baseline_wwr)`

**[Back](../_toc.md)**
