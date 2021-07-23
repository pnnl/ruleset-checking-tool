
# Envelope - Rule 5-1  

**Rule ID:** 5-1  
**Rule Description:** Baseline Performance is the average of 4 rotations if vertical fenestration area per each orientation differ by more than or equal to 5%.  
**Rule Assertion:** Baseline RMR Building:is_rotated = expected value  
**Appendix G Section:** Section G3.1-5(b) Building Envelope Modeling Requirements for the Baseline building  
**Appendix G Section Reference:** Table G3.1 Section 5a  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  

  1. Baseline vertical fenestration area is determined correctly by Rule 5-18 and 5-19  

**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  

## Rule Logic:  

- **Applicability Check 1:** ```if ( ( rule-5-18  == PASS ) AND ( rule-5-19 == PASS ) ):```  

- Get building rotation angles in the Baseline model: ```rotation_angles_b = B_RMR.ASHRAE229.building_rotation_angles```  

- Get surface conditioning category dictionary: ```scc_dictionary = get_surface_conditioning_category(B_RMR)```  

- For each building segment in the Baseline model: ```for building_segment_b in B_RMR.building.building_segments:```  

  - For each thermal_block in building segment: ```thermal_block_b in building_segment_b.thermal_blocks:```  
  
    - For each zone in thermal block: ```zone_b in thermal_block_b.zones:```  

      - For each surface in zone: ```for surface_b in zone_b.surfaces:```  

        - If surface is part of envelope and vertical: ```if ( ( get_opaque_surface_type(surface) == "ABOVE-GRADE WALL" ) AND ( scc_dictionary[surface.id] != "UNREGULATED" ) ):```  

          - For each fenestration in surface: ```for fenestration_b in surface_b.fenestration_subsurfaces:```  

            - If the glazed vision area is less than 50% of the total area, fenestration area is the glazed vision area: ```if ( fenestration_b.glazed_area < ( fenestration_b.glazed_area + fenestration_b.opaque_area ) * 50% ): fenestration_area_b += fenestration_b.glazed_area```  

            - Else, fenestration area is the total area: ```else: fenestration_area_b += fenestration_b.glazed_area + fenestration_b.opaque_area```  

        - Summarize the total fenestration area for each azimuth for the building:  ```fenestration_area_dictionary[surface_b.azimuth] += fenestration_area_b```  

- Check if the maximum and minimum fenestration area per each azimuth differ by more than or equal to 5%: ```if max(fenestration_area_dictionary.values()) >= 1.05 * min(fenestration_area_dictionary.values()): is_rotation_required = TRUE```  

**Rule Assertion:** 

- Case 1, the total vertical fenestration area per azimuth differ by less than 5% and the baseline building performance is not the average of four orientations: ```( is_rotation_required == FALSE ) AND (): PASS```  

- Case 2, the total vertical fenestration area per azimuth differ by less than 5% and the baseline building performance is the average of four orientations: ```( is_rotation_required == FALSE ) AND (): FAIL```  

- Case 3, the total vertical fenestration area per azimuth differ by 5% or more and the baseline building performance is not the average of four orientations: ```( is_rotation_required == TRUE ) AND (): MANUAL_CHECK```  

- Case 4, the total vertical fenestration area per azimuth differ by 5% or more and the baseline building performance is the average of four orientations: ```( is_rotation_required == TRUE ) AND (): PASS```  
