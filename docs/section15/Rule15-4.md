# Transformers - Rule 15-4
**Rule ID:** Rule 15-4  
**Rule Description:** User RMR transformer Name in Baseline RMR  
**Rule Assertion:** Baseline RMR = expected value  
**Appendix G Section:** Transformers  
**Appendix G Section Reference:** None  
**Data Lookup:** None  
**Evaluation Context:**  Each Data Element   
**Applicability Checks:** 
1. Number of transformers in User RMR greater than 0  

**Manual Checks:** None  

## Rule Logic:
- **Applicability Check 1:** `length(U_RMR.transformers) > 0:`  
- Get list of Baseline transformer names: `for transformer in B_RMR.building.transformers: baseline_transformer_names = transformer.name`
- **Rule Assertion:** `for transformer in U_RMR.transformers: transformer.name in baseline_transformer_names`

**[Back](../_toc.md)**