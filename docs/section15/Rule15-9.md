# Transformers - Rule 15-9
**Rule ID:** Rule 15-9  
**Rule Description:** Transformer capacity ratio reported in Baseline RMR equals User RMR  
**Rule Assertion:** User RMR = Baseline RMR  
**Appendix G Section:** Transformers  
**Appendix G Section Reference:**  Table G3.1 15. Distribution Transformers  
**Data Lookup:** Table 8.4.4  
**Evaluation Context:**  Each Data Element  
**Applicability Checks:**
1. Transformer is DRY_TYPE
2. U_RMR transformer capacity is within range of Table 8.4.4  

**Manual Checks:** None  

## Rule Logic:
- For each transformer `_user_transformer` in `U_RMR.transformers`:  
    - Get maximum regulated capacity: `if _user_transformer.phase == SINGLE_PHASE: _max_capacity_limit = 333.0 else if _user_transformer.phase == THREE_PHASE: _max_capacity_limit = 1000.0`  
    - **Applicability Check 1:** `_user_transformer.type == DRY_TYPE`  
    - **Applicability Check 2:** `_user_transformer.capacity >= 15.0 and _user_transformer.capacity <= _max_capacity_limit:`  
    - Get baseline transformer matching ID of user transformer: `_baseline_transformer = match_data_element(B_RMR, transformers, _user_transformer.id)`  
    - Calculate user transformer capacity ratio: `_user_transformer_capacity_ratio = _user_transformer.capacity / _user_transformer.peak_load`  
    - Calculate baseline transformer capacity ratio: `_baseline_transformer_capacity_ratio = _baseline_transformer.capacity / _baseline_transformer.peak_load`  
    - **Rule Assertion:** `_user_transformer_capacity_ratio == _baseline_transformer_capacity_ratio`  

## Diagram
<img src="../diagrams/Section15.png">

**[Back](../_toc.md)**
