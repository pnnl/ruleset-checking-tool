
# Envelope - Rule 5-43  

**Rule ID:** 5-43  
**Rule Description:** The  proposed roof surfaces shall be modeled using the same solar reflectance as in the user model if the aged test data are available, or equal to 0.7 default reflectance.  
**Rule Assertion:** P-RMR SurfaceOpticalProperties:absorptance_solar_exterior = U-RMR SurfaceOpticalProperties:absorptance_solar_exterior for regulated surfaces or P-RMR SurfaceOpticalProperties:absorptance_solar_exterior = 0.3 for unregulated surfaces  
**Appendix G Section:** Section 5 Envelope  
**Appendix G Section Reference:** Section G3.1-1(a) Building Envelope Modeling Requirements for the Proposed design  

**Applicability:** All required data elements exist for P_RMR  
**Applicability Checks:**  None  

**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  
**Function Call:**  

  1. get_opaque_surface_type()
  2. match_data_element()
  3. get_surface_conditioning_category()

## Rule Logic:  

- Get surface conditioning category dictionary for P_RMR: `scc_dictionary_p = get_surface_conditioning_category(P_RMR)`

- For each zone in B_RMR: `for zone_p in B_RMR...zones:`

  - For each surface in zone: `for surface_p in zone_p.surfaces;`

    - Check if surface is roof, get matching surface in U_RMR: `if get_opaque_surface_type(surface_p.id) == "ROOF": surface_u = match_data_element(U_RMR, Surfaces, surface_p.id)`

      **Rule Assertion:**  

      - Case 1: For each roof surface, if surface is unregulated and surface solar reflectance is equal to 0.3: `if ( scc_dictionary_p[surface_p.id] == "UNREGULATED" ) AND ( surface_p.surface_optical_properties.absorptance_solar_exterior == 0.7 ): PASS`

      - Case 2: Else if roof surface solar reflectance in P_RMR matches U_RMR and is equal to 0.3: `if ( surface_p.surface_optical_properties.absorptance_solar_exterior == surface_u.surface_optical_properties.absorptance_solar_exterior ) AND ( surface_p.surface_optical_properties.absorptance_solar_exterior == 0.7 ): PASS`

      - Case 3: Else if roof surface solar reflectance in P_RMR matches U_RMR and is not equal to 0.3: `else if ( surface_p.surface_optical_properties.absorptance_solar_exterior == surface_u.surface_optical_properties.absorptance_solar_exterior ) AND ( surface_p.surface_optical_properties.absorptance_solar_exterior != 0.7 ): CAUTION and raise_warning "ROOF SURFACE SOLAR REFLECTANCE IN P-RMR MATCHES THAT IN U-RMR BUT IS NOT EQUAL TO 0.3. VERIFY THAT REFLECTANCE WAS ESTABLISHED USING AGED TEST DATA AS REQUIRED IN SECTION 5.5.3.1(a).`

      - Case 4: Else if roof surface solar reflectance in P_RMR does not match U_RMR but is equal to 0.3: `else if surface_p.surface_optical_properties.absorptance_solar_exterior == 0.7: PASS and show_message "ROOF SURFACE SOLAR REFLECTANCE IS EQUAL TO THE PRESCRIBED DEFAULT VALUE OF 0.3 BUT DIFFERS FROM THE SOLAR REFLECTANCE IN THE USER MODEL."`

      - Case 5: Else, roof surface solar reflectance in P_RMR does not match that in U_RMR and is not equal to 0.3: `Else: FAIL`

**[Back](../_toc.md)**

**Rule Assertion Table:**
|Cases|Unregulated Roof Surface|Regulated Roof Surface|
|:----|:-:|:-:|
|P=0.3, P=U|Case#1|Case#2|
|P=0.3, P!=U|Case#1|Case#5|
|P!=0.3, P=U|Case#5|Case#3|
|P!=0.3, P!U|Case#5|Case#4|
