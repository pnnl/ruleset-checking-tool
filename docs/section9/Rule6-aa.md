
# Lighting - Rule 6-aa

**Rule ID:** 6-aa  
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

- For each building_segment in the Proposed model: ```For building_segment_proposed in P_RMR.building.building_segments:```  

  - For each thermal_block in building segment: ```thermal_block_proposed in building_segment_proposed.thermal_blocks:```  

  - For each zone in thermal block: ```zone_proposed in thermal_block_proposed.zones:```  

  - For each space in thermal zone: ```space_proposed in zone_proposed.spaces:```  

    - Get interior lighting in space: ```interior_lighting_proposed =  space_proposed.interior_lightings```  

    - Get the EFLH value for the associated lighting schedule: ```schedule_EFLH_proposed = EFLH(interior_lighting_proposed.lighting_schedule_name)```  

    - Get matching space from Baseline RMR: ```space_baseline = match_data_element(B_RMR, spaces, space_proposed.name)```  

      - Get interior lighting in space: ```interior_lighting_baseline =  space_baseline.interior_lightings```  

      - Get the EFLH value for the associated lighting schedule: ```schedule_EFLH_baseline = EFLH(interior_lighting_baseline.lighting_schedule_name)```  

      **Rule Assertion:** For each interior_lighting in P_RMR: ```if ( schedule_EFLH_proposed / schedule_EFLH_baseline ) <> 90%: CAUTION```  
