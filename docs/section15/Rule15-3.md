# Transformers - Rule 15-3
**Rule ID:** 15-3  
**Rule Description:** User RMR transformer Name in Proposed RMR  
**Appendix G Section:** Transformers  
**Appendix G Section Reference:** None  
**Applicability:** Number of U_RMR.transformers > 0  
**Manual Check:** None  
**Evaluation Context:**  Each Data Element   
**Data Lookup:** None  
**Determining Expected Value:**
- Get list of Proposed transformer names: `for transformer in P_RMR.building.transformers: proposed_transformer_names = transformer.name`

**Rule Assertion:**
- For each User transformer: `for transformer in U_RMR.transformers: transformer.name in proposed_transformer_names`

**[Back](../_toc.md)**