# Envelope - Rule 5-42  
**Schema Version:** 0.0.37  
**Mandatory Rule:** False    
**Rule ID:** 5-42  
 
**Rule Description:** Each linear thermal bridge and point thermal bridge as identified in Section 5.5.5 shall be modeled using either of the following techniques:  

a. A separate model of the assembly within the energy simulation model.  
b. Adjustment of the clear-field U-factor in accordance with Section A10.2.    

**Rule Assertion:** B-RMR = expected value                                           
**Appendix G Section:** Table G3.1 Section 5(a)-1 Proposed  
**Appendix G Section Reference:** 5(a)  
**Data Lookup:** None  
**Evaluation Context:** Evaluate each Project   

**Applicability Checks:** 

1. A project has an exterior wall

**Function Call:** 

**Manual Check:** Ensure that linear and point thermal bridges, as identified in Section 5.5.5 are modeled using either of the following techniques:  
a. A separate model of the assembly within the energy simulation model.  
b. Adjustment of the clear-field U-factor in accordance with Section A10.2.      
 
**Rule Logic:**  
**Applicability:**  
- look at each zone in the RMD: `for zone in P_RMD....zones:`
    - look at each surface in the zone: `for surface in zone.surfaces:`
    - if the surface is an exterior surface, then this rule is applicable for the entire project: `if((surface.adjacent_to == "EXTERIOR") or (surface.adjacent_to == "GROUND")): UNDETERMINED`
- if the rule logic gets here without an UNDETERMINED outcome, then the project is not applicable: `NOT_APPLICABLE`    


 **[Back](../_toc.md)**
