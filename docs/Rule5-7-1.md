# Envelope - Rule 5-7-1 
**Rule ID:** 5-7-1  
**Rule Description:** Baseline WWR should be equal to User WWR or 40%, whichever is smaller.  
**Appendix G Section:** Envelope  
**Appendix G Section Reference:**
- Table G3.1, 5. Building Envelope, Baseline Building Performance, c. Vertical Fenestration Areas
- Table G3.1.1-1

**Applicability:** All required data elements exist for U_RMR and B_RMR  
**Manual Check:** None  
**Evaluation Context:**  Each Data Element  
**Data Lookup:** Table G3.1.1-1  
**Determining Expected Value:**
- Detrmine the WWR for each building segment in the User model: `For building_segment in U_RMR.building.building_segments:`
    - Get the building area type of the building segment: `building_area_type = building_segment.area_type_vertical_fenestration`
    - If building area type exists in Table G3.1.1-1 then get the allowable WWR for the building segment: `if building_area_type in table_G3_1_1_1: allowable_baseline_wwr = data_lookup(table_G3_1_1_1, building_area_type) else: allowable_baseline_wwr = 0.40`
    - Get thermal_block from building segment: `thermal_block in ...building_segment.thermal_blocks:`
    - Get thermal_zone from thermal block: `thermal_zone in ...thermal_block.thermal_zones:`
    - Get space from thermal zone: `space in …thermal_zone.spaces:`
        - Check that space is either [new, addition or alteration] and [heated and cooled, heated only, or semi-heated]: `if space.status_type in [NEW, ADDITION, ALTERATION] AND space.conditioning_type in [HEATED_AND_COOLED, HEATED_ONLY, SEMIHEATED]:` 
            - Get surface in space: `surface in space.surfaces:`
                - Check that surface is exterior and vertical: `if ( surface.adjacent_to in [AMBIENT] ) AND ( 0 <= surface.tilt <= 90 ): exterior_vertical_surfaces.append(surface)`
                - Calculate the total exterior surface area: `total_exterior_surface_area = sum(exterior_surface.area for exterior_surface in exterior_vertical_surfaces)`
                - Calculate the total fenestration area: `total_fenestration_area = sum(fenestration.area for fenestration in exterior_surface.fenestration_subsurfaces)`
                - Calculate WWR of the building_segment: `WWR_user = total_fenestration_area/total_exterior_surface_area`

**Rule Assertion:**  For each User building_segment: `WWR_baseline == min(WWR_user, building_gross_above_grade_wall_area)`

**[Back](_toc.md)**