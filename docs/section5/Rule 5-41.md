# Envelope - Rule 5-41  
**Schema Version:** 0.0.37  
**Mandatory Rule:** False    
**Rule ID:** 5-41  
 
**Rule Description:** Linear and Point Thermal Bridges. Where linear thermal bridges and point thermal bridges, as identified in Section 5.5.5 are modeled in the proposed design, they shall not be modeled in the budget building design.  

**Rule Assertion:** B-RMR = expected value                                           
**Appendix G Section:** Table G3.1 Section 5(c) Baseline  
**Appendix G Section Reference:** 5(c)  
**Data Lookup:** None  
**Evaluation Context:** Evaluate each Project   

**Applicability Checks:** 

1. A project has an exterior wall

**Function Call:** 

**Manual Check:** Where linear thermal bridges and point thermal bridges, as identified in Section 5.5.5 are modeled in the proposed design, they shall not be modeled in the budget building design.  
 
**Rule Logic:**  
**Applicability:**  
- look at each zone in the RMD: `for zone in B_RMD....zones:`
    - look at each surface in the zone: `for surface in zone.surfaces:`
    - if the surface is an exterior surface, then this rule is applicable for the entire project: `if((surface.adjacent_to == "EXTERIOR") or (surface.adjacent_to == "GROUND")): UNDETERMINED`
- if the rule logic gets here without an UNDETERMINED outcome, then the project is not applicable: `NOT_APPLICABLE`    


 **[Back](../_toc.md)**
