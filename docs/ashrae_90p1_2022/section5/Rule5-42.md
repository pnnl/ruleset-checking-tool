# Envelope - Rule 5-42  
**Schema Version:** 0.0.37  
**Mandatory Rule:** False    
**Rule ID:** 5-42  

**Rule Description:** Each linear thermal bridge and point thermal bridge as identified in Section 5.5.5 shall be modeled using either of the following techniques:  

a. A separate model of the assembly within the energy simulation model.  
b. Adjustment of the clear-field U-factor in accordance with Section A10.2.    

**Rule Assertion:** B-RMR = expected value                                           
**Appendix G Section:** Section G3.1-5 Building Envelope Modeling Requirements for the Proposed building  
**Appendix G Section Reference:** Table G3.1 Section 5(a) Exception #1   
**Data Lookup:** None  
**Evaluation Context:** Evaluate each Project   

**Applicability Checks:** 

1. A project has at least one regulated surface.

**Function Call:** 

**Manual Check:** Ensure that linear and point thermal bridges, as identified in Section 5.5.5 are modeled using either of the following techniques:  
a. A separate model of the assembly within the energy simulation model.  
b. Adjustment of the clear-field U-factor in accordance with Section A10.2.      

**Rule Logic:**  
**Applicability:**  
- for each building in the proposed RMD: `for building in P_RMD....buildings:`
  - get the surface conditioning category dictionary for the building: `scc_dictionary_p = get_surface_conditioning_category(climate_zone, building)`
  - for each zone in the building: `for zone in building....zones:`
      - for each surface in the zone: `for surface in zone.surfaces:`
          - get the surface conditioning category: `scc = scc_dictionary_p[surface.id]`
          - if the project has at least one surface that is not an unregulated surface then this rule applies: `if scc != UNREGULATED:`
            - set the outcome as UNDETERMINED because the rule cannot be fully evaluated: `outcome = UNDETERMINED`
- if the loop completes without finding a regulated surface then the rule is not applicable: `outcome = NOT_APPLICABLE`    


 **[Back](../_toc.md)**