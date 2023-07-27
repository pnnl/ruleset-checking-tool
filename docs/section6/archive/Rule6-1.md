
# Lighting - Rule 6-1 

**Rule ID:** 6-1  
**Rule Description:** For the proposed building, each space has the same lighting power as the corresponding space in the U-RMR  
**Appendix G Section:** Section G3.1-1(a) Modeling Requirements for the Proposed design  
**Appendix G Section Reference:** None

**Applicability:** All required data elements exist for U_RMR and P_RMR  
**Applicability Checks:** None  
**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  
## Rule Logic: 

- Calculate the total lighting power for each space under each building segment in the User RMR: `for building_segment_user in U_RMR.building.building_segments:`  

  - For each zone in building segment: `zone_user in building_segment_user...zones:`

    - For each space in thermal zone: `space_user in zone_user.spaces:`

      - Get floor_area from space: `floor_area_user = space_user.floor_area`

      - Get interior_lighting in space: `interior_lighting_user = space_user.interior_lightings`

        - Get the total design power_per_area: `space_lighting_power_per_area_user = sum( lighting.power_per_area for lighting in interior_lighting_user )`

        - Calculate the total design lighting power in space: `space_total_lighting_power_user = space_lighting_power_per_area_user * floor_area_user`

- Calculate the total lighting power for each space under each building segment in the Proposed RMR: `for building_segment_proposed in P_RMR.building.building_segments:`  

  - For each zone in building segment: `zone_proposed in building_segment_proposed...zones:`

    - For each space in thermal zone: `space_proposed in zone_proposed.spaces:`

      - Get floor_area from space: `floor_area_proposed = space_proposed.floor_area`

      - Get interior_lighting in space: `interior_lighting_proposed = space_proposed.interior_lightings`

        - Get the total design power_per_area: `space_lighting_power_per_area_proposed = sum( lighting.power_per_area for lighting in interior_lighting_proposed )`

        - Calculate the total design lighting power in space: `space_total_lighting_power_proposed = space_lighting_power_per_area_proposed * floor_area_proposed`

  **Rule Assertion:** The total lighting power in each space for U_RMR and P_RMR are the same: `space_total_lighting_power_user = space_total_lighting_power_proposed`

**[Back](../_toc.md)**
