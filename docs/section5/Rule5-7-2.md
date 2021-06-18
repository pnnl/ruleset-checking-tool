# Envelope - Rule 5-7-2  
**Rule ID:** 5-7-2  
**Rule Description:** Baseline RMR WWR is distributed in the same proportion as User RMR.  
**Rule Assertion:** Baseline RMR = expected value  
**Appendix G Section:** Section G3.1-5(c) Building Envelope Modeling Requirements for the Baseline building    
**Appendix G Section Reference:**
- Table G3.1, 5. Building Envelope, Baseline Building Performance, c. Vertical Fenestration Areas

**Data Lookup:** None
**Evaluation Context:**  Each Data Element  

**Applicability Checks:** 
1. Building has spaces that are NEW, ADDITION or ALTERATION.

**Manual Checks:** None  

## Rule Logic:
- **Applicability Check 1:** `length( [ if _space.status_type for _space in U_RMR...spaces is in [NEW, ADDITION, ALTERATION] ] ) > 0:`  
- For each building segment in the Baseline model: `For building_segment in B_RMR.building.building_segments:`
    - Get the building area type of the building segment: `_building_area_type = building_segment.area_type_vertical_fenestration`
    - Get thermal_block from building segment: `_thermal_block in building_segment.thermal_blocks:`
    - Get thermal_zone from thermal block: `_thermal_zone in _thermal_block.thermal_zones:`
    - Get space from thermal zone: `_space in _thermal_zone.spaces:`
        - Check that space is either [new, addition or alteration] and [heated and cooled, heated only, or semi-heated]: `if ( _space.status_type in [NEW, ADDITION, ALTERATION] ) AND ( _space.conditioning_type in [HEATED_AND_COOLED, HEATED_ONLY, SEMIHEATED] ):` 
        - For surface orientation in each orientation (East = 90, South = 180, West = 270, North = 0): `for _surface_orienation in [90, 180, 270, 0]:`  
        - Get surface in space: `_surface in space.surfaces:`
            - Check surface azimuth is within +/- 45 deg of surface orientation: `( _surface.azimuth > _surface_orientation - 45) and ( _surface.azimuth <= _surface_azimuth + 45):`  
            - Check that surface is exterior and vertical: `if ( _surface.adjacent_to in [AMBIENT] ) AND ( 60 <= _surface.tilt <= 90 ): _exterior_vertical_surfaces.append(_surface)`
            - Calculate the total exterior surface area: `_total_exterior_surface_area = sum(_exterior_surface.area for _exterior_surface in _exterior_vertical_surfaces)`
            - Calculate the total fenestration area: `_total_fenestration_area = sum(_fenestration.area for _fenestration in _exterior_surface.fenestration_subsurfaces)`
            - Calculate Baseline WWR for each orientation (East = 90, South = 180, West = 270, North = 0) for the building area type: `_WWR_baseline = _total_fenestration_area/_total_exterior_surface_area`  
            - Repeat previous steps to calculate the User WWR for each orientation and building area type: `_WWR_user = _calculate_wwr(U_RMR)`  
            - **Rule Assertion** For each building area type and orientation the WWR is equal between the Baseline and User RMRs: `_WWR_baseline_ == _WWR_user`

**[Back](../_toc.md)**
