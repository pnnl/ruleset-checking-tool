# Transformers - Rule 15-6
**Rule ID:** Rule 15-6  
**Description:** Transformer efficiency reported in User RMR equals Table 8.4.4  
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
- For each transformer in User RMR: `For user_transformer in U_RMR.transformers:`
    - Check if transformer is DRY_TYPE: `if user_transformer.type is DRY_TYPE:`   
    - Get user efficiency limit: `user_transformer_efficiency_limit = data_lookup(table_8_4_4, user_transformer.capacity)`
    - Determine if modeled user efficiency exceeds limit: `if user_transformer.efficiency > user_transformer_efficiency_limit:`
        - Get user transformer matching name of user transformer: `user_transformer = match_data_element(U_RMR, transformers, user_transformer.name)`
        - Get user efficiency requirement: `required_user_transformer_efficiency = data_lookup(table_8_4_4, user_transformer.capacity)`

**Rule Assertion:**
- For each User transformer: `user_transformer.efficiency == required_user_transformer_efficiency`

**[Back](_toc.md)**