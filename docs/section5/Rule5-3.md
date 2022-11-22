
# Envelope - Rule 5-3  

**Rule ID:** 5-3  
**Rule Description:** The building shall be modeled so that it does not shade itself.  
**Rule Assertion:** Baseline RMR Building: surface.does_cast_shade = expected value  
**Appendix G Section:** Section G3.1-5(b) Building Envelope Modeling Requirements for the Baseline building  
**Appendix G Section Reference:** Table G3.1 Section 5a  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  None  

**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  

## Rule Logic:  

- For each building segment in the Baseline model: ```for building_segment_b in B_RMR.building.building_segments:```  
 
  - For each zone in building segment: ```zone_b in building_segment_b.zones:```  

      - For each surface in zone: ```for surface_b in zone_b.surfaces:```  

        - Check that surface is exterior: ```if ( surface_b.adjacent_to == "EXTERIOR" ): exterior_vertical_surface_b = surface_b```  

        **Rule Assertion:** Baseline exterior surface does not cast shade:  

        - Case 1: ```exterior_vertical_surface_b.does_cast_shade == FALSE: PASS```  

        - Case 2: ```exterior_vertical_surface_b.does_cast_shade == TRUE: FAIL```  
