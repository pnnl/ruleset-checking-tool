# Transformers - Rule 15-5
**Rule ID:** Rule 15-5  
**Description:** Transformer efficiency reported in Baseline RMR equals Table 8.4.4  
**Appendix G Section:** Transformers  
**Appendix G Section Reference:**  Table G3.1 15. Distribution Transformers  
**Applicability:**
 - Rule 15-3 passes  
 - Transformer is DRY_TYPE
 - U_RMR transformer efficiency is greater than Table 8.4.4  
 
**Manual Check:** None  
**Evaluation Context:**  Each Data Element   
**Data Lookup:** Table 8.4.4  
**Calculate Expected Value:**
- For each transformer in Baseline RMR: `For user_transformer in U_RMR.transformers:`
    - Check if transformer is DRY_TYPE: `if user_transformer.type is DRY_TYPE:`   
    - Get user efficiency limit: `user_transformer_efficiency_limit = data_lookup(table_8_4_4, user_transformer.capacity)`
    - Determine if modeled user efficiency exceeds limit: `if user_transformer.efficiency > user_transformer_efficiency_limit:`
        - Get baseline transformer matching name of user transformer: `baseline_transformer = match_data_element(B_RMR, transformers, user_transformer.name)`
        - Get baseline efficiency requirement: `required_baseline_transformer_efficiency = data_lookup(table_8_4_4, baseline_transformer.capacity)`

**Rule Assertion:**
- For each Baseline transformer: `baseline_transformer.efficiency == required_baseline_transformer_efficiency`

**[Back](_toc.md)**