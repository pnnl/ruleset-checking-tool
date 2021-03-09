# Transformers - Rule 15-2
**Description:** Number of transformers modeled in User RMR and Proposed RMR are the same  
**Reference:**  
**Applicability:** Number of U_RMR.transformers > 0  
**Manual Check:** None  
**Evaluation Context:**  Data Group  
**Data Lookup:** None  
**Determining Expected Value:**
- Calculate number of User RMR transformers `num_user_transformers = length(U_RMR.transformers)`
- Calculate number of Proposed RMR transformers `num_proposed_transformers = length(B_RMR.transformers)`

**Rule Assertion:**  
- Number of User and Proposed transformers are equal: `num_user_transformers == num_proposed_transformers`

**[Back](_toc.md)**