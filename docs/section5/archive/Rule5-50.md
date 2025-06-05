
# Envelope - Rule 5-50  

**Rule ID:** 5-50  
**Rule Description:** Shading by adjacent structures and terrain is the same in the baseline and proposed.  
**Rule Assertion:** B-RMR building:has_site_shading = P-RMR building:has_site_shading  
**Appendix G Section:** Section G3.1-14(a) Building Envelope Modeling Requirements for the Proposed design and Baseline  
**Appendix G Section Reference:** None  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  None  

**Manual Check:** Yes  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  
**Function Call:** None  

## Rule Logic:  

**Rule Assertion:**  

- Case 1: If neither B-RMR nor P-RMR has site shading modeled: `if ( NOT B_RMR.building.has_site_shading ) AND ( NOT P_RMR.building.has_site_shading ): PASS`

- Case 2: Else if both B-RMR and P-RMR have site shading modeled: `if ( B_RMR.building.has_site_shading ) AND ( P_RMR.building.has_site_shading ): CAUTION and raise_warning "SHADING BY ADJACENT STRUCTURES AND TERRAIN IS MODELED FOR BOTH B-RMR AND P-RMR. VERIFY SHADING IN BOTH CASES ARE THE SAME."`

- Case 3: Else, site shading is modeled differently in B-RMR and P-RMR: `else: FAIL`

**Notes:**

1. BASELINE=PROPOSED match, archived on 10/26/2023

**[Back](../_toc.md)**
