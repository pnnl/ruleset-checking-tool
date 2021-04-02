# Transformers - Rule 15-3
**Rule ID:** 15-3  
**Rule Description:** User RMR transformer Name in Proposed RMR  
**Rule Assertion:** Proposed RMR = expected value  
**Appendix G Section:** Transformers  
**Appendix G Section Reference:** None  
**Data Lookup:** None  
**Evaluation Context:**  Each Data Element   
**Applicability Checks:** None  
**Manual Checks:** None  

## Rule Logic:
- Get list of Proposed transformer names: `_proposed_transformer_names = [ _proposed_transformer.name for _proposed_transformer in P_RMR.transformers ]`
- For each transformer `_user_transformer` in `U_RMR.transformers`:
    - **Rule Assertion:** `_user_tranformer.name in _proposed_transformer_names`

**[Back](../_toc.md)**
