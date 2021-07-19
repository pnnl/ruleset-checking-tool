
# Lighting - Rule 6-14  

**Rule ID:** 6-14  
**Rule Description:** Proposed building is modeled with other programmable lighting controls through a 10% schedule reduction in buildings less than 5,000sq.ft.  
**Rule Assertion:** Proposed RMR = expected value  
**Appendix G Section:** Section G3.1-6(i) Modeling Requirements for the Proposed design  
**Appendix G Section Reference:** None  

**Applicability:** All required data elements exist for P_RMR  
**Applicability Checks:**  

  1. Building total area is less than 5,000sq.ft.  

**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  

## Rule Logic:  

- **Applicability Check 1:** ```if sum(space.floor_area for zone.space in P_RMR) < 5000:```  

- For each building_segment in the Proposed model: ```For building_segment_p in P_RMR.building.building_segments:```  

  - For each thermal_block in building segment: ```thermal_block_p in building_segment_p.thermal_blocks:```  

    - For each zone in thermal block: ```zone_p in thermal_block_p.zones:```  

      - For each space in thermal zone: ```space_p in zone_p.spaces:```  

        - Get interior lighting in space: ```interior_lighting_p =  space_p.interior_lighting```  

          - Get the EFLH value for the associated lighting schedule: ```schedule_EFLH_p = EFLH(interior_lighting_p.lighting_schedule_name)```  

          - Get matching space from Baseline RMR: ```space_b = match_data_element(B_RMR, spaces, space_p.name)```  

          - Get interior lighting in space: ```interior_lighting_b =  space_b.interior_lighting```  

          - Get the EFLH value for the associated lighting schedule: ```schedule_EFLH_b = EFLH(interior_lighting_b.lighting_schedule_name)```  

            **Rule Assertion:** For each interior_lighting in P_RMR: ```if ( schedule_EFLH_p / schedule_EFLH_b ) <> 90%: CAUTION```  
