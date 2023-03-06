# Envelope - Rule 5-43  
**Schema Version** 0.0.23  
**Primary Rule:** False
**Rule ID:** 5-43  
**Rule Description:** The  proposed roof surfaces shall be modeled using the same solar reflectance as in the user model if the aged test data are available, or equal to 0.7 default reflectance.
**Appendix G Section:** Section 5 Envelope  
**Appendix G Section Reference:** Section G3.1-1(a) Building Envelope Modeling Requirements for the Proposed design  

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
    
    - For each surface in zone: ```for surface_p in zone_p.surfaces:```

      - Check if surface is roof, set rule applicability check to True: ```if get_opaque_surface_type(surface_p.id) == "ROOF": rule_applicability_check = TRUE```
  
        - Get matching surface in U_RMR: ```surface_u = match_data_element(U_RMR, Surfaces, surface_p.id)```
        **Rule Assertion:**

        - Case 1: If roof surface solar reflectance in P_RMR matches U_RMR and is equal to 0.3, outcome is PASS: ```if ( surface_p.surface_optical_properties.absorptance_solar_exterior == surface_u.surface_optical_properties.absorptance_solar_exterior ) AND ( surface_p.surface_optical_properties.absorptance_solar_exterior == 0.7 ):
          outcome = PASS```

        - Case 2: Else if roof surface solar reflectance in P_RMR matches U_RMR and is not equal to 0.3, outcome is UNDETERMINED: ```else if ( surface_p.surface_optical_properties.absorptance_solar_exterior == surface_u.surface_optical_properties.absorptance_solar_exterior ) AND ( surface_p.surface_optical_properties.absorptance_solar_exterior != 0.7 ):
          outcome = UNDETERMINED and raise_message "ROOF SURFACE SOLAR REFLECTANCE IN P-RMR (${1 - surface_p.surface_optical_properties.absorptance_solar_exterior}) MATCHES THAT IN U-RMR BUT IS NOT EQUAL TO THE PRESCRIBED DEFAULT VALUE OF 0.3. VERIFY THAT REFLECTANCE WAS ESTABLISHED USING AGED TEST DATA AS REQUIRED IN SECTION 5.5.3.1(a).```

        - Case 3: Else if roof surface solar reflectance in P_RMR does not match U_RMR but is equal to 0.3, outcome is UNDETERMINED: ```else if surface_p.surface_optical_properties.absorptance_solar_exterior == 0.7:
          outcome = UNDETERMINED and raise_message "ROOF SURFACE SOLAR REFLECTANCE IS EQUAL TO THE PRESCRIBED DEFAULT VALUE OF 0.3 BUT DIFFERS FROM THE SOLAR REFLECTANCE IN THE USER MODEL (${1 - surface_u.surface_optical_properties.absorptance_solar_exterior})."```

        - Case 4: Else, roof surface solar reflectance in P_RMR does not match that in U_RMR and is not equal to 0.3, outcome is FAIL: ```Else: outcome = FAIL```

- Case 5: If no surface in building is roof, outcome is NOT_APPLICABLE: ```if NOT rule_applicability_check: outcome = NOT_APPLICABLE```
**[Back](../_toc.md)**
