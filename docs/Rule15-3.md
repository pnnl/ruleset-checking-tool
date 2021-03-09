# Transformers - Rule 15-3
**Description:** User RMR transformer Name in Proposed RMR  
**Applicability:** Number of U_RMR.transformers > 0  
**Reference:**  
**Manual Check:** None  
**Evaluation Context:**  Each Data Element   
**Data Lookup:** None  
**Determining Expected Value:**
- Get list of Proposed transformer names: `for transformer in P_RMR.building.transformers: proposed_transformer_names = transformer.name`

**Rule Assertion:**
- For each User transformer: `for transformer in U_RMR.transformers: transformer.name in proposed_transformer_names`

**[Back](_toc.md)**