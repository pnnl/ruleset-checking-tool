# Envelope - Rule 5-41  
**Schema Version** 0.0.23  
**Primary Rule:** False
**Rule ID:** 5-41  
**Rule Description:** The proposed roof surfaces shall be modeled using the same thermal emittance as in the user model if the aged test data are available, or equal to 0.9 default emittance.
**Appendix G Section:** Section G3.1-1(a) Building Envelope Modeling Requirements for the Proposed design  
**Appendix G Section Reference:** None  

**Applicability:** All required data elements exist for P_RMR  
**Applicability Checks:**  
  1. The proposed building has a roof surface

**Evaluation Context:** Each Data Element  
**Data Lookup:** None  
**Function Call:**  

  1. get_opaque_surface_type()
  2. match_data_element()

## Rule Logic:  

- For each building segment in the Proposed model: ```for building_segment_p in P_RMR.building.building_segments:```

  - For each zone in building segment: ```for zone_p in building_segment_p.zones:```

    - For each space in zone: ```for space_p in zone_p.spaces:``` 

      - For each surface in space: ```for surface_p in space_p.surfaces;```

        - Check if surface is roof, set rule applicability check to True: ```if get_opaque_surface_type(surface_p.id) == "ROOF": rule_applicability_check = TRUE```

          - Get matching surface in U_RMR : ```surface_u = match_data_element(U_RMR, Surfaces, surface_p.id)```
          **Rule Assertion:**  

          - Case 1: If roof surface thermal emittance in P_RMR matches that in U_RMR and is equal to 0.9, outcome is PASS: ```if ( surface_p.surface_optical_properties.absorptance_thermal_exterior == surface_u.surface_optical_properties.absorptance_thermal_exterior ) AND ( surface_p.surface_optical_properties.absorptance_thermal_exterior == 0.9 ):
            outcome = PASS```

          - Case 2: Else if roof surface thermal emittance in P_RMR matches that in U_RMR but is not equal to 0.9, outcome is UNDETERMINED: ```else if ( surface_p.surface_optical_properties.absorptance_thermal_exterior == surface_u.surface_optical_properties.absorptance_thermal_exterior ) AND ( surface_p.surface_optical_properties.absorptance_thermal_exterior != 0.9 ):
            outcome = UNDETERMINED and raise_message "ROOF SURFACE EMITTANCE IN P-RMR (${surface_p.surface_optical_properties.absorptance_thermal_exterior}) MATCHES THAT IN U-RMR BUT IS NOT EQUAL TO THE PRESCRIBED DEFAULT VALUE OF 0.9."```

          - Case 3: Else if roof surface thermal emittance in P_RMR does not match that in U_RMR but is equal to 0.9, outcome is UNDETERMINED: ```else if surface_p.surface_optical_properties.absorptance_thermal_exterior == 0.9:
            outcome = UNDETERMINED and raise_message "ROOF THERMAL EMITTANCE IS EQUAL TO THE PRESCRIBED DEFAULT VALUE OF 0.9 BUT DIFFERS FROM THE THERMAL EMITTANCE IN THE USER MODEL (${surface_u.surface_optical_properties.absorptance_thermal_exterior})."```

          - Case 4: Else, roof surface thermal emittance in P_RMR does not match that in U_RMR and is not equal to 0.9, outcome is FAIL: ```Else: outcome = FAIL```
          
- Case 5: If no surface in building is roof, outcome is NOT_APPLICABLE: ```if NOT rule_applicability_check: outcome = NOT_APPLICABLE```
**[Back](../_toc.md)**
