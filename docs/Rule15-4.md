# Transformers - Rule 15-4
**Description:** User RMR transformer Name in Baseline RMR  
**Applicability:** Number of U_RMR.transformers > 0  
**Reference:**  
**Manual Check:** None  
**Evaluation Context:**  Each Data Element   
**Data Lookup:** None  
**Determining Expected Value:**
- Get list of Baseline transformer names: `for transformer in B_RMR.building.transformers: baseline_transformer_names = transformer.name`

**Rule Assertion:**
- For each User transformer: `for transformer in U_RMR.transformers: transformer.name in baseline_transformer_names`

**[Back](_toc.md)**