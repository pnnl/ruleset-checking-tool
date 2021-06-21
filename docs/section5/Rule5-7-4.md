# Envelope - Rule 5-7-4   
**Rule ID:** 5-7-4  
**Rule Description:** Fenestration area is equal for Proposed RMR and User RMR.  
**Rule Assertion:** Proposed RMR = expected value  
**Appendix G Section:** Section G3.1-5(c) Building Envelope Modeling Requirements for the Baseline building    
**Appendix G Section Reference:**
- Table G3.1, 5. Building Envelope, Baseline Building Performance, c. Vertical Fenestration Areas

**Data Lookup:** None  
**Evaluation Context:**  Each Data Element  

**Applicability Checks:** None  
**Manual Checks:** None  

## Rule Logic:
- For each building segment in the User model: `For building_segment in U_RMR.building.building_segments:`
    - Get the building area type of the building segment: `_building_area_type = building_segment.area_type_vertical_fenestration`
    - Get thermal_block from building segment: `_thermal_block in building_segment.thermal_blocks:`
    - Get thermal_zone from thermal block: `_thermal_zone in _thermal_block.thermal_zones:`
    - Get space from thermal zone: `_space in _thermal_zone.spaces:`
        - For surface orientation in each orientation (East = 90, South = 180, West = 270, North = 0): `for _surface_orienation in [90, 180, 270, 0]:`  
        - Get surface in space: `_surface in space.surfaces:`
            - Check surface azimuth is within +/- 45 deg of surface orientation: `( _surface.azimuth > _surface_orientation - 45) and ( _surface.azimuth <= _surface_azimuth + 45):`  
            - Check that surface is exterior and vertical: `if ( _surface.adjacent_to in [AMBIENT] ) AND ( 60 <= _surface.tilt <= 90 ): _exterior_vertical_surfaces.append(_surface)`
            - Calculate the total exterior surface area: `_total_exterior_surface_area = sum(_exterior_surface.area for _exterior_surface in _exterior_vertical_surfaces)`
            - Calculate the total fenestration area for each orientation and building area type for the User RMR: `_user_fenestration_area = sum(_fenestration.area for _fenestration in _exterior_surface.fenestration_subsurfaces)`  
            - Repeat calculating the total fenestration area for each orientation and building area type for the Proposed RMR: `_proposed_fenestration_area = = sum(_fenestration.area for _fenestration in _exterior_surface.fenestration_subsurfaces)`  
            - **Rule Assertion** The fenestration area for each building area type and orientation is equal between the Proposed and User RMRs: `_proposed_fenestration_area == _user_fenestration_area`

**[Back](../_toc.md)**
