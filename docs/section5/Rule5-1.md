
# Envelope - Rule 5-1  

**Schema Version:** 0.0.16  
**Mandatory Rule:** True
**Rule ID:** 5-1  
**Rule Description:** Baseline Performance is the average of 4 rotations if vertical fenestration area per each orientation differ by more than or equal to 5%.  
**Rule Assertion:** Baseline RMR Building:is_rotated = expected value  
**Appendix G Section:** Section G3.1-5(b) Building Envelope Modeling Requirements for the Baseline building  
**90.1 Section Reference:** Table G3.1 Section 5a  
**Data Lookup:** None  
**Evaluation Context:** Each Data Element  
**Applicability Checks:**  

1. Vertical fenestration area per each orientation differ by more than or equal to 5% in baseline ruleset model instance.

**Function Calls:** None  

## Rule Logic:  

- For each ruleset model instance: `for ruleset_model_instance in ASHRAE229.ruleset_model_instances:`

  - If ruleset model instance is baseline: `if ruleset_model_instance == 'baseline':`

    - Get surface conditioning category dictionary: `scc_dictionary = get_surface_conditioning_category(ruleset_model_instance)`  

    - For each zone in Baseline: `for zone_b in ruleset_model_instance...zones:`

      - For each surface in zone: `for surface_b in zone_b.surfaces:`  

        - If surface is part of envelope and vertical: `if ( ( get_opaque_surface_type(surface) == "ABOVE-GRADE WALL" ) AND ( scc_dictionary[surface.id] != "UNREGULATED" ) ):`  

          - For each subsurface in surface: `for subsurface_b in surface_b.subsurfaces:`  

            - If the glazed vision area is less than 50% of the total area, fenestration area is the glazed vision area: `if ( subsurface_b.glazed_area < ( subsurface_b.glazed_area + subsurface_b.opaque_area ) * 50% ): fenestration_area_b += subsurface_b.glazed_area`  

            - Else, fenestration area is the total subsurface area: `else: fenestration_area_b += subsurface_b.glazed_area + subsurface_b.opaque_area`  

        - Summarize the total fenestration area for each azimuth for the building:  `fenestration_area_dictionary[surface_b.azimuth] += fenestration_area_b`  

- Check if the maximum and minimum fenestration area per each azimuth differ by more than or equal to 5%, continue to rule logic: `if max(fenestration_area_dictionary.values()) >= 1.05 * min(fenestration_area_dictionary.values()): is_rotation_required = TRUE`

  - Calculate the average annual energy cost for 4 baseline instances: `average_annual_energy_cost_b = AVERAGE(output_instance.annual_source_results.annual_cost for output_instance in Output2019ASHRAE901.output_instance if output_instance.ruleset_model_type in ['BASELINE_0', 'BASELINE_90', 'BASELINE_180', 'BASELINE_270'])`

- Else, get annual energy cost for baseline with no rotation: `else: annual_energy_cost_b0 = output_instance.annual_source_results.annual_cost for output_instance in Output2019ASHRAE901.output_instance if output_instance.ruleset_model_type == 'BASELINE_0'`

**Rule Assertion:** 

- Case 1. the total vertical fenestration area per azimuth differ by 5% or more and the baseline building performance is the average of four orientations: `( is_rotation_required == TRUE ) AND ( average_annual_energy_cost_b == Output2019ASHRAE901.baseline_building_performance_energy_cost ): PASS`

- Case 2. the total vertical fenestration area per azimuth differ by 5% or more and the baseline building performance is not the average of four orientations: `( is_rotation_required == TRUE ) AND ( average_annual_energy_cost_b == Output2019ASHRAE901.baseline_building_performance_energy_cost ): FAIL`

- Case 3. the total vertical fenestration area per azimuth differ by less than 5% and the baseline building performance equals to baseline with no rotation: `( is_rotation_required == FALSE ) AND ( annual_energy_cost_b0 == Output2019ASHRAE901.baseline_building_performance_energy_cost ): PASS`

- Case 4. the total vertical fenestration area per azimuth differ by less than 5% and the baseline building performance is not equal to baseline with no rotation: `( is_rotation_required == FALSE ) AND ( annual_energy_cost_b0 != Output2019ASHRAE901.baseline_building_performance_energy_cost ): FAIL`  

**Notes:**

1. Do we need to pass 5-18 and 5-19 as applicability check? (Baseline vertical fenestration area is determined correctly by Rule 5-18 and 5-19)
2. Currently assuming all surfaces in a model instance are in one building to be consistent with other RDS.
