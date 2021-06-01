
# Envelope - Rule 5-1-1  

**Rule ID:** 5-1-1  
**Rule Description:** Baseline Performance is the average of 4 rotations if vertical fenestration area per each orientation differ by more than 5%.  
**Rule Assertion:** Baseline RMR Building:is_rotated = expected value  
**Appendix G Section:** Section G3.1-5(b) Building Envelope Modeling Requirements for the Baseline building  
**Appendix G Section Reference:** Table G3.1 Section 5a  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  

  1. Baseline vertical fenestration area is determined correctly by Rule 5-7  

**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  

## Rule Logic:  

- **Applicability Check 1:** ```if (rule-5-7  == PASS):```  

- Get building rotation status in the Baseline model: ```is_rotated_b = B_RMR.building.is_rotated```  

- For each building segment in the Baseline model: ```for building_segment_b in B_RMR.building.building_segments:```  

  - For each thermal_block in building segment: ```thermal_block_b in building_segment_b.thermal_blocks:```  
  
  - For each zone in thermal block: ```zone_b in thermal_block_b.zones:```  

  - For each space in zone: ```space_b in zone_b.spaces:```  

    - For each surface in space: ```for surface_b in space_b.surfaces:```  

      - Check that surface is exterior and vertical: ```if ( surface_b.adjacent_to == "EXTERIOR" ) AND ( 60 <= _surface.tilt <= 90 ): exterior_vertical_surface_b = surface_b```  

      - Get the surface azimuth: ```surface_azimuth_b = surface_b.azimuth```  

      - Calculate the total fenestration area: ```fenestration_area_b = sum( fenestration.area for fenestration in exterior_vertical_surface_b.fenestration_subsurfaces)```  

      - Summarize the total fenestration area and the total surface area for each orientation for the building:  

      ```if ( surface_azimuth_b > 315 ) OR ( surface_azimuth_b <= 45 ): total_fenestration_area_north += fenestration_area_b```  

      ```elsif ( surface_azimuth_b > 45 ) AND ( surface_azimuth_b <= 135 ): total_fenestration_area_east += fenestration_area_b```  

      ```elsif ( surface_azimuth_b > 135 ) AND ( surface_azimuth_b <= 225 ): total_fenestration_area_south += fenestration_area_b```  

      ```else total_fenestration_area_west += fenestration_area_b```  

- Check if the total vertical fenestration areas for the four orientation differs by less than 5%: ```if max(total_fenestration_area_north, total_fenestration_area_east, total_fenestration_area_south, total_fenestration_area_west) >= 1.05 * min(total_fenestration_area_north, total_fenestration_area_east, total_fenestration_area_south, total_fenestration_area_west)): is_rotation_required = TRUE```

**Rule Assertion:** Baseline RMR Building:is_rotated = expected value: ```is_rotated_b == is_rotation_required```

- Case 1, the total vertical fenestration area per exposure differ by less than 5% and the baseline building is not rotated: ```( is_rotation_required == FALSE ) AND ( is_rotated_b == FALSE ): PASS```  

- Case 2, the total vertical fenestration area per exposure differ by less than 5% and the baseline building is rotated: ```( is_rotation_required == FALSE ) AND ( is_rotated_b == TRUE ): FAIL```  

- Case 3, the total vertical fenestration area per exposure differ by 5% or more and the baseline building is not rotated: ```( is_rotation_required == TRUE ) AND ( is_rotated_b == FALSE ): MANUAL_CHECK```  

- Case 4, the total vertical fenestration area per exposure differ by 5% or more and the baseline building is rotated: ```( is_rotation_required == TRUE ) AND ( is_rotated_b == TRUE ): PASS```  
