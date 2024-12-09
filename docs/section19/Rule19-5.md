# Section 19 - Rule 19-5      
**Schema Version:** 0.0.24    
**Mandatory Rule:** True      
**Rule ID:** 19-5       
**Rule Description:** Unmet load hours for the proposed design shall not exceed 300 (of the 8760 hours simulated).   
**Rule Assertion:** Options are Pass/Fail/UNDETERMINED       
**Appendix G Section:** G3.1.2.3        
**90.1 Section Reference:** None  

**Data Lookup:** None  

**Evaluation Context:** Each Proposed Design RulesetModelInstance  

**Applicability Checks:**  

1. Applies only to the proposed design rule set model instance.  

**Function Calls:**  None

## Rule Logic:   
**Applicability Check 1:**  
- For each RulesetModelInstance in ASHRAE229.ruleset_model_instance : `for RulesetModelInstance in ASHRAE229.ruleset_model_instance:`  
    - Check if the ruleset model instance is the proposed model instance: `If RulesetModelInstance.RulesetModelOptions2019ASHRAE901.ruleset_model_type = "PROPOSED":`  
        - Get the heating unmet load hours for the rule set model instance: `unmet_load_hours_heating = RulesetModelInstance.output.OutputInstance.unmet_load_hours_heating`  
        - Get the cooling unmet load hours for the rule set model instance: `unmet_load_hours_cooling = RulesetModelInstance.output.OutputInstance.unmet_load_hours_cooling`  
        - Get the coincident unmet load hours for the rule set model instance: `coincident_unmet_load_hours = RulesetModelInstance.output.OutputInstance.unmet_load_hours`  

        **Rule Assertion:** 
        - Case 1: If the coincident unmet load hours are less than or equal to 300 and not equal to Null then pass: `if coincident_unmet_load_hours != Null and coincident_unmet_load_hours <= 300: outcome = "Pass"`  
        - Case 2: Elif the heating + cooling unmet load hours less than or equal to 300 and neither is equal to Null then pass: `elif unmet_load_hours_heating != Null and unmet_load_hours_cooling != Null and (unmet_load_hours_heating + unmet_load_hours_cooling <= 300): outcome = "Pass"`  
        - Case 3: Elif the coincident unmet load hours are greater than 300 and not equal to Null then fail: `elif coincident_unmet_load_hours != Null and coincident_unmet_load_hours > 300: outcome = "Fail"`  
        - Case 4: Elif the heating + cooling unmet load hours greater than 600 then fail: `elif unmet_load_hours_heating + unmet_load_hours_cooling > 600: outcome = "FAIL"`   
        - Case 5: Else, UNDETERMINED: `Else: outcome = "UNDETERMINED and raise_message "Conduct manual check that unmet load hours for the proposed design do not exceed 300 (of the 8760 hours simulated)"`   

**Notes/Questions:**  
1. I left in the checks on the heating and cooling unmet load hours separately in case coincident unmet load hours is not defined to avoid flags. 
2. I made the final else statement an undetermined outcome because it would mean that coincident_unmet_load_hours was not populated in the RMD and unmet_load_hours_heating + unmet_load_hours_cooling is between 300 and 600 (or nothing needed was populated in the RMD). 



**[Back](../_toc.md)**