
# Envelope - Rule 5-1

**Rule ID:** 5-1  
**Rule Description:** Baseline Performance is the average of 4 rotations if vertical fenestration area per each orientation differ by more than 5%  
**Rule Assertion:** Baseline RMR Building:is_rotated = expected value  
**Appendix G Section:** Envelope  
**Appendix G Section Reference:** Table G3.1 Section 5a  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  

  1. Baseline vertical fenestration area is determined correctly by Rule 5-7  

**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  

## Rule Logic:  

- **Applicability Check 1:** ```if (rule-5-7  == PASS):```
- Get building rotation status in the Baseline model: ```_is_rotated = B_RMR.building.is_rotated```
- For each building segment in the Baseline model: ```for _building_segment in B_RMR.building.building_segments:```
  - Get thermal_block from building segment: ```_thermal_block in building_segment.thermal_blocks:```
  - Get thermal_zone from thermal block: ```_thermal_zone in thermal_block.zones:```
  - Get space from thermal zone: ```_space in thermal_zone.spaces:```  
    - Get surface in space: ```_surface = space.surfaces```
    - Check that surface is exterior and vertical: ```if ( _surface.adjacent_to in [AMBIENT] ) AND ( 60 <= _surface.tilt <= 90 ): _exterior_vertical_surface = _surface```
    - Get the surface azimuth: ```_surface_azimuth = surface.azimuth```  
    - Calculate the total fenestration area: ```_fenestration_area = sum( _fenestration.area for _fenestration in _exterior_vertical_surface.fenestration_subsurfaces)```
    - Calculate the total surface area: ```_surface_area = surface.area```
    - Summarize the total fenestration area and the total surface area for each orientation: ```if ( _surface_azimuth > 315 ) OR ( _surface_azimuth <= 45 ): _total_fenestration_area_north += _fenestration_area```  
    ```elsif ( _surface_azimuth > 45 ) AND ( _surface_azimuth <= 135 ): _total_fenestration_area_east += _fenestration_area```
    ```elsif ( _surface_azimuth > 135 ) AND ( _surface_azimuth <= 225 ): _total_fenestration_area_south += _fenestration_area```
    ```else _total_fenestration_area_west += _fenestration_area```  
- Check if the total vertical fenestration areas for the four orientation differs by less than 5%: ```if max(_total_fenestration_area_north, _total_fenestration_area_east, _total_fenestration_area_south, _total_fenestration_area_west) >= 1.05 * min(_total_fenestration_area_north, _total_fenestration_area_east, _total_fenestration_area_south, _total_fenestration_area_west)): _is_rotation_required = TRUE```

**Rule Assertion:** Baseline RMR Building:is_rotated = expected value: ```is_rotated == _is_rotation_required```

- Case 1, the total vertical fenestration area per exposure differ by less than 5% and the baseline building is not rotated: ```( _is_rotation_required == FALSE ) AND ( _is_rotated == FALSE ): PASS```  
- Case 2, the total vertical fenestration area per exposure differ by less than 5% and the baseline building is rotated: ```( _is_rotation_required == FALSE ) AND ( _is_rotated == TRUE ): FAIL```  
- Case 3, the total vertical fenestration area per exposure differ by 5% or more and the baseline building is not rotated: ```( _is_rotation_required == TRUE ) AND ( _is_rotated == FALSE ): MANUAL_CHECK```  
- Case 4, the total vertical fenestration area per exposure differ by 5% or more and the baseline building is rotated: ```( _is_rotation_required == TRUE ) AND ( _is_rotated == TRUE ): PASS```  
