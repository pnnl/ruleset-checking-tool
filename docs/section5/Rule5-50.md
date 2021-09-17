
# Envelope - Rule 5-50  

**Rule ID:** 5-50  
**Rule Description:** Shading by adjacent structures and terrain is the same in the baseline and proposed.  
**Rule Assertion:** B-RMR building:has_site_shading = P-RMR building:has_site_shading  
**Appendix G Section:** Section G3.1-14(a) Building Envelope Modeling Requirements for the Proposed design and Baseline  
**Appendix G Section Reference:** None  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  None  

**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  
**Function Call:** None  

## Rule Logic:  

**Rule Assertion:**  

- Case 1: If shading by adjacent structure and terrain is modeled the same in B-RMR as in P-RMR: `if B_RMR.building.has_site_shading == P_RMR.building.has_site_shading: PASS`

- Case 2: Else: `else: FAIL`

**[Back](../_toc.md)**

**Notes:**

1. Did not find building.has_site_shading in the current schema.
