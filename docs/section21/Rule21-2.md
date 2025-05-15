
# Boiler - Rule 21-2  

**Rule ID:** 21-2  
**Rule Description:** For purchased HW/steam in the proposed model, the baseline shall have the same number of pumps as proposed
**Rule Assertion:** B-RMD = expected value  
**Appendix G Section:** Section 21 Boiler  
**Appendix G Section Reference:** Section G.3.1.1.3.4 On-Site Distribution Pumps  
**Schema Version:** 0.0.25 

**Applicability:** All required data elements exist for B_RMI  
**Applicability Checks:**  

1. P-RMD is modeled with purchased hot water or steam.

**Manual Check:** Yes  
**Evaluation Context:** Building  
**Data Lookup:** None  
**Function Call:** 

1. check_purchased_chw_hhw()


**Applicability Checks:**

- Check if P-RMD is modeled with purchased chilled water or purchased hot water/steam: `purchased_chw_hhw_status_dict = check_purchased_chw_hhw(P_RMI)`

  - If P-RMD is not modeled with purchased hot water/steam, rule is not applicable to B-RMD: `if NOT purchased_chw_hhw_status_dict["PURCHASED_HEATING"]: RULE_NOT_APPLICABLE`

  - Else, P-RMD is modeled with purchased hot water/steam, continue to rule logic: `else: CHECK_RULE_LOGIC`

## Rule Logic:  


**Rule Assertion:**

- Case 1:  `UNDETERMINED and raise_message "P-RMD IS MODELED WITH PURCHASED HOT WATER OR STEAM. VERIFY B-RMD HAS THE SAME NUMBER OF PUMPS AS THE PROPOSED."`

**[Back](../_toc.md)**
