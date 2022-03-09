
# Envelope - Rule 5-44  

**Rule ID:** 5-44  
**Rule Description:** The infiltration modeling method in the baseline includes adjustment for weather and building operation.  
**Rule Assertion:** B-RMR infiltration:modeling_method = NOT "CONSTANT" for all zones  
**Appendix G Section:** Section G3.1-5(b) Building Envelope Modeling Requirements for the Proposed design and Baseline  
**Appendix G Section Reference:** None  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  None  

**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  
**Function Call:** None  

## Rule Logic:  

- For each building segment in the Baseline model: `for building_segment_b in B_RMR.building.building_segments:`  

    - For each zone in building segment, get zone infiltration: `for zone_b in building_segment_b.zones: infiltration_b = zone_b.infiltration`  

      **Rule Assertion:**  

      - Case 1: If zone infiltration is not modeled as constant: `if infiltration_b.modeling_method != "CONSTANT": PASS`  

      - Case 2: Else: `Else: FAIL`

**[Back](../_toc.md)**
