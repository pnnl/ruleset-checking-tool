# HVAC_SystemZoneAssignment – Rule 18-3    
**Schema Version:** 0.0.28  
**Mandatory Rule:** False    
**Rule ID:** 18-3  
 
**Rule Description:** The lab exhaust fan shall be modeled as constant horsepower (kilowatts) reflecting constant-volume stack discharge with outdoor air bypass in the baseline

**Rule Assertion:** B-RMR = expected value                                           
**Appendix G Section:** Section G3.1-10 HVAC Systems for the baseline building  
**Appendix G Section Reference:** None  
**Data Lookup:** None  
**Evaluation Context:** Evaluate each Building   

**Applicability Checks:** 

1. The building includes >15,000cfm of lab exhaust

**Function Call:** 

1. get_zone_target_baseline_system()



**Applicability Check:** 
- check if any of the target baseline system types from the function `get_zone_target_baseline_system` have a SYSTEM_ORIGIN of "G3_1_1d" - this indicates that there is greater than 15,000 cfm of laboratory exhaust in the building, and that some of it comes from air handlers
- get the target baseline systems: `target_baseline_systems = get_zone_target_baseline_system(P_RMD,B_RMD)`
- look through all of the target baseline systems, and determine if any has a SYSTEM_ORIGIN of "G3_1_1d": `if any(zone["SYSTEM_ORIGIN"] == "G3_1_1d" for zone in target_baseline_systems):`
      - in this case, the building might have greater than 15,000cfm lab exhaust, set result to APPLICABLE: `result = APPLICABLE`
- otherwise, it's not applicable: `result = NOT_APPLICABLE`

    


 **[Back](../_toc.md)**
