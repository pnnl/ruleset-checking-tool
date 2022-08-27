
# Lighting - Rule 6-2

**Rule ID:** 6-2  
**Rule Description:** Spaces in proposed building with hardwired lighting, including Hotel/Motel Guest Rooms, Dormitory Living Quarters, Interior Lighting Power >= Table 9.6.1; For Dwelling Units, Interior Lighting Power >= 0.6W/sq.ft.  
**Appendix G Section:** Table G3.1 Part 6 Lighting under Proposed Building Performance paragraph (e)  
**Appendix G Section Reference:**  

- Table 9.6.1, Lighting Power Density Allowances Using the Space-by-Space Method and Minimum Control Requirements Using Either Method  

**Applicability:** All required data elements exist for P_RMR  
**Applicability Checks:**  

  1. Building has Hotel/Model Guestroom or Dormitory Living Quarters, Dwelling Units space types  

**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** Table 9.6.1 and Table G3.7  
## Rule Logic:


- For each building segment in the proposed model: ```for building_segment_p in P_RMR.building.building_segments:```  

    - For each zone in building segment: ```zone_p in building_segment_p.zones:```  

      - For each space in zone: ```space_p in zone_p.spaces:```  

        - Check if lighting_space_type of the space is "Guest Room", "Dormitory Living Quarters" or "Dwelling Units": ```if ( space_p.lighting_space_type == "Guest Room" ) OR ( space_p.lighting_space_type == "Dormitory Living Quarters" ) OR ( space_p.lighting_space_type == "Dwelling Units" ):```  

          - If lighting_space_type of the space is "Guest Room" or "Dormitory Living Quarters", get the lighting power density allowance for the proposed model from Table 9.6.1: ```if ( space_p.lighting_space_type == "Guest Room" ) OR ( space_p.lighting_space_type == "Dormitory Living Quarters" ): lighting_power_allowance_p = data_lookup(table_9_6_1, space_p.lighting_space_type)```  

          - Else if the lighting_space_type is "Dwelling Unit", get the lighting power density allowance from Table G3.1-6-e as 0.6W/sq.ft.: ```elseif ( space_p.lighting_space_type == "Dwelling Unit" ): lighting_power_allowance_p = 0.6```  

          - Get the total design power_per_area for the space: ```space_lighting_power_per_area_p = sum( lighting.power_per_area for lighting in space_p.interior_lighting )```  

          - Get the matching space in U_RMR: ```space_u = match_data_element(U_RMR, spaces, space_p.id)```  

            - Get the total design power_per_area for the space in U_RMR: ```space_lighting_power_per_area_u = sum( lighting.power_per_area for lighting in space_u.interior_lighting )```  

            **Rule Assertion:** For each space that is Hotel/Motel Guestroom or Dormitory Living Quarters in the proposed model, lighting power used in the simulation shall be equal to the lighting power allowance in Table 9.6.1 or as designed, whichever is larger; for each space that is Dwelling Units in the proposed model, lighting power used in the simulation shall be equal to 0.6W/sq.ft. or as designed, whichever is larger: ```space_lighting_power_per_area_p == max( lighting_power_allowance_p, space_lighting_power_per_area_u)```  

**Notes:**
  1. Updated the Rule ID from 6-3 to 6-2 on 6/8/2022
  2. Removed the Applicability Check on 8/27/2022

**[Back](../_toc.md)**
