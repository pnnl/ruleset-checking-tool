
# Lighting - Rule 6-6

**Rule ID:** 6-6  
**Rule Description:** Baseline building is not modeled with daylighting control  
**Appendix G Section:** Section G3.1-6 Modeling Requirements for the baseline building  
**Appendix G Section Reference:**  

**Applicability:** All required data elements exist for B_RMD    
**Applicability Checks:**   
1. Space is not a crawl space, plenum or interstitial space.  

**Manual Check:** No  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  
## Rule Logic:

- Check if any space has daylight control in the Baseline model: ```For building_segment_b in B_RMD.building.building_segments:```  

  - For each thermal_block in building segment: ```thermal_block_b in building_segment_b.thermal_blocks:```

  - For each zone in thermal block: ```zone_b in thermal_block_b.zones:```

  - For each space in zone: ```space_b in zone_b.spaces:```  
    - **Applicability Check 1:** Check if the space is a crawl space, plenum or interstitial space: `if space_b.function in [PLENUM, CRAWL_SPACE, INTERSTITIAL_SPACE]:`  
      - Space is not applicable because space function is crawl space, plenum or interstitial space, rule outcome for space is NOT_APPLICABLE: `continue`  

    - Get interior_lighting in space: ```interior_lighting_b = space_b.interior_lighting```  

      **Rule Assertion:** 
    - Case 1: If no daylighting control in the baseline then PASS: ```if interior_lighting_b.daylighting_control_type == NONE: PASS```  
    - Case 2: ELse then fail: `Else: FAIL`  

**Notes:**
  1. Updated the Rule ID from 6-11 to 6-7 on 6/3/2022
  2. Updated the Rule ID from 6-7 to 6-6 on 6/8/2022
  3. Updated to make crawl space, plenum or interstitial space not applicable.  

**[Back](../_toc.md)**
