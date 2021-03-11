# Transformers - Rule 15-1
**Rule ID:** 15-1  
**Rule Description:** Number of transformers modeled in User RMR and Baseline RMR are the same  
**Appendix G Section:** Transformers  
**Appendix G Section Reference:** None  
**Applicability:** Number of U_RMR.transformers > 0  
**Manual Check:** None  
**Evaluation Context:**  Data Group  
**Data Lookup:** None  
**Determining Expected Value:**
- Calculate number of User RMR transformers `num_user_transformers = length(U_RMR.transformers)`
- Calculate number of Baseline RMR transformers `num_baseline_transformers = length(B_RMR.transformers)`

**Rule Assertion:**
- Number of User and Baseline transformers are equal: `num_user_transformers == num_baseline_transformers`

**[Back](../_toc.md)**