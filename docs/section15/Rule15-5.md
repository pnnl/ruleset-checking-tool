# Transformers - Rule 15-5
**Rule ID:** 15-5  
**Rule Description:** Transformer efficiency reported in Baseline RMR equals Table 8.4.4  
**Rule Assertion:** Baseline RMR = expected value  
**Appendix G Section:** Transformers  
**Appendix G Section Reference:**  Table G3.1 15. Distribution Transformers  
**Data Lookup:** Table 8.4.4  
**Evaluation Context:**  Each Data Element  
**Applicability Checks:**
1. Number of transformers in User RMR greater than 0  
2. Transformer name is in Baseline RMR (Rule 15-4)
3. Transformer is DRY_TYPE
4. U_RMR transformer capacity is within range of Table 8.4.4  

**Manual Checks:** None  

## Rule Logic:
- **Applicability Check 1:** `length(U_RMR.transformers) > 0:`  
- For each transformer in User RMR: `For _user_transformer in U_RMR.transformers:`
    - **Applicability Check 2:** `if rule_outcome(15_4, _user_transformer.name) is True:`  
    - **Applicability Check 3:** `if _user_transformer.type is DRY_TYPE:`  
    - Get maximum regulated capacity: `if user_transformer.phase == SINGLE_PHASE: _max_capacity_limit = 333.0 else if user_transformer.phase == THREE_PHASE: _max_capacity_limit = 1000.0`  
    - **Applicability Check 4:** `if (user_transformer.capacity >= 15.0) and (_user_transformer.capacity <= _max_capacity_limit):`  
    - Get Baseline transformer matching name of user transformer: `_baseline_transformer = match_data_element(B_RMR, transformers, user_transformer.name)`
    - Get required Baseline transformer efficiency: `_required_baseline_transformer_efficiency = data_lookup(table_8_4_4, _baseline_transformer.capacity, user_transformer.phase)`
    - **Rule Assertion:** `_baseline_transformer.efficiency == _required_baseline_transformer_efficiency`

**[Back](../_toc.md)**