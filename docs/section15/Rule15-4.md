# Transformers - Rule 15-4
**Rule ID:** Rule 15-4  
**Rule Description:** User RMR transformer ID in Baseline RMR  
**Rule Assertion:** Baseline RMR = expected value  
**Appendix G Section:** Transformers  
**Appendix G Section Reference:** None  
**Data Lookup:** None  
**Evaluation Context:**  Each Data Element   
**Applicability Checks:** None  
**Manual Checks:** None  

## Rule Logic:
- Get list of Baseline transformer names: `_baseline_transformer_ids = [ _baseline_transformer.id for _baseline_transformer in B_RMR.transformers ]`
- For each transformer `_user_transformer` in `U_RMR.transformers`:
    - **Rule Assertion:** `_user_tranformer.id in _baseline_transformer_ids`

## TCD Diagram
<img src="../diagrams/Section15.png">

**[Back](../_toc.md)**
