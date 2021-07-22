
# Envelope - Rule 5-17  

**Rule ID:** 5-17  
**Rule Description:** Opaque surfaces that are not regulated (not part of opaque building envelope) must be modeled the same in the baseline as in the proposed design.  
**Appendix G Section:** Section G3.1-5 Building Envelope Modeling Requirements for the Baseline building  
**Appendix G Section Reference:** None  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:** None  

**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  

## Rule Logic:  

- Get surface conditioning category dictionary for B_RMR: ```scc_dictionary_b = get_surface_conditioning_category(B_RMR)```  

- For each building segment in the Proposed model: ```for building_segment_b in B_RMR.building.building_segments:```  

  - For each thermal_block in building segment: ```for thermal_block_b in building_segment_b.thermal_blocks:```  

    - For each zone in thermal block: ```for zone_b in thermal_block_b.zones:```  

      - For each surface in zone: ```for surface_b in zone_b.surfaces:```  

        - Check if surface is unregulated: ```if ( scc_dictionary_b[surface_b.id] == UNREGULATED ):```  

          - Get matching surface from P_RMR: ```surface_p = match_data_element(P_RMR, surfaces, surface_b.id)```  

            **Rule Assertion:**  

            Case 1: Surface construction in B_RMR matches P_RMR: ```if surface_b.construction == surface_p.construction: PASS```  

            Case 2: Else: ```else: FAIL```  
