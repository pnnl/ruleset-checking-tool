# Transformers - Rule 15-1
**Rule ID:** 15-1  
**Rule Description:** Number of transformers modeled in User RMR and Baseline RMR are the same  
**Rule Assertion:** Baseline RMR = User RMR  
**Appendix G Section:** Transformers  
**Appendix G Section Reference:** None  
**Data Lookup:** None  
**Evaluation Context:**  Data Group  
**Applicability Checks:** 
1. Number of transformers in User RMR greater than 0  

**Manual Checks:** None  

## Rule Logic:
- **Applicability Check 1:** `length(U_RMR.transformers) > 0:`  
- Calculate number of User RMR transformers `num_user_transformers = length(U_RMR.transformers)`
- Calculate number of Baseline RMR transformers `num_baseline_transformers = length(B_RMR.transformers)`
- **Rule Assertion:** `num_user_transformers == num_baseline_transformers`  

## Diagram
<img src="../diagrams/Section15.png">

**[Back](../_toc.md)**