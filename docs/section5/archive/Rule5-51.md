
# Envelope - Rule 5-51  

**Rule ID:** 5-51  
**Rule Description:** Shading by adjacent structures and terrain is the same in the proposed design as in user model.  
**Rule Assertion:** P-RMR building:has_site_shading = U-RMR building:has_site_shading  
**Appendix G Section:** Section G3.1-14(a) Building Envelope Modeling Requirements for the Proposed design  
**Appendix G Section Reference:** None  

**Applicability:** All required data elements exist for P_RMR  
**Applicability Checks:**  None  

**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  
**Function Call:** None  

## Rule Logic:  

**Rule Assertion:**  

- Case 1: If shading by adjacent structure and terrain is modeled the same in P-RMR as in U-RMR: `if P_RMR.building.has_site_shading == U_RMR.building.has_site_shading: PASS`

- Case 2: Else: `else: FAIL`

**Notes:**

1. USER=PROPOSED match, archived on 10/26/2023

**[Back](../_toc.md)**
