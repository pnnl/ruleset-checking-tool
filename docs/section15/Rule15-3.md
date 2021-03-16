# Transformers - Rule 15-3
**Rule ID:** 15-3  
**Rule Description:** User RMR transformer Name in Proposed RMR  
**Rule Assertion:** Proposed RMR = expected value  
**Appendix G Section:** Transformers  
**Appendix G Section Reference:** None  
**Data Lookup:** None  
**Evaluation Context:**  Each Data Element   
**Applicability Checks:**  
 1. Number of transformers in User RMR greater than 0  
 
**Manual Checks:** None  

## Rule Logic:
- **Applicability Check 1:** `length(U_RMR.transformers) > 0:`  
- For each transformer in User RMR: `for _user_transformer in U_RMR.transformers:`  
    - Get list of Proposed transformer names: `_proposed_transformer_names = [ _proposed_transformer.name for _proposed_transformer in P_RMR.building.transformers ]`
    - **Rule Assertion:** `_user_tranformer.name in _proposed_transformer_names`

**[Back](../_toc.md)**