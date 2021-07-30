
# Lighting - Rule 6-9

**Rule ID:** 6-9  
**Rule Description:** Baseline building is modeled with automatic shutoff controls in buildings >5000 sq.ft.  
**Appendix G Section:** Section G3.1-6 Modeling Requirements for the Baseline building  
**Appendix G Section Reference:**  None  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  

  1. Building total area is more than 5,000sq.ft.  

**Manual Check:**  

  1. Where building total area is more than 5,000sq.ft., manual review is required to verify automatic shutoff controls are modeled correctly in the Baseline.  

**Function Call:** None  

**Evaluation Context:** Each Data Element  
**Data Lookup:** None  

## Rule Logic: 

- For each building_segment in the Baseline model: ```for building_segment_b in B_RMR.building.building_segments:```  
  - For each thermal_block in building segment: ```for thermal_block_b in building_segment.thermal_blocks:```  
    - For each zone in thermal block: ```for zone_b in thermal_block_b.zones:```  
      - For each space in zone: ```for space_b in zone.spaces:```  
        - Add space floor area to building total floor area: ```building_total_area_b += space_b.floor_area```  
- **Applicability Check 1:**```if building_total_area_b > 5000:```  

- **Manual Check 1:** Manual review is required where building total area is more than 5,000sq.ft. to verify automatic shutoff controls are modeled correctly in the Baseline.  
