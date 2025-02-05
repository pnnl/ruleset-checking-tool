
# Envelope - Rule 5-44  

**Rule ID:** 5-44  
**Rule Description:** Space Conditioning Categories. Space conditioning categories used to determine applicability of the envelope requirements in Tables G3.4-1 through G3.4-8 shall be the same as in the proposed design.

Exception: Envelope components of the HVAC zones that are semiheated in the proposed design must meet conditioned envelope requirements in Tables G3.4-1 through G3.4-8 if, based on the sizing runs, these zones are served by a baseline system with sensible cooling output capacity >= 5 Btu/h·ft2 of floor area, or with heating output capacity greater than or equal to the criteria in Table G3.4-9, or that are indirectly conditioned spaces.  

**Rule Assertion:** Baseline equals proposed, except defined exceptions  
**Appendix G Section:** Table G3.1 Section 5(b) Baseline  
**Schema Version:** 0.0.39  

**Applicability:** All required data elements exist for B_RMD  
**Applicability Checks:** Buiding has spaces  

**Evaluation Context:** Each Data Element  
**Data Lookup:** None  
**Function Call:**

  1. get_surface_conditioning_category()  

## Applicability:
- this rule applies to buildings with exterior or underground surfaces.
- Get surface conditioning category dictionary for B_RMD: ```scc_dictionary_b = get_surface_conditioning_category(B_RMD)```
- possible surface conditioning types are "UNREGULATED", "SEMI-EXTERIOR", "EXTERIOR MIXED", "EXTERIOR RESIDENTIAL", "EXTERIOR NON-RESIDENTIAL".  This rule applies if there is at least one surface that is one of: "SEMI-EXTERIOR", "EXTERIOR MIXED", "EXTERIOR RESIDENTIAL", "EXTERIOR NON-RESIDENTIAL"
- Look at each surface id: ```for surface_id in scc_dictionary_b:```
  - if the value is one of "SEMI-EXTERIOR", "EXTERIOR MIXED", "EXTERIOR RESIDENTIAL", "EXTERIOR NON-RESIDENTIAL", CONTINUE TO RULE LOGIC: ```if scc_dictionary_b[surface_id] in ["SEMI-EXTERIOR", "EXTERIOR MIXED", "EXTERIOR RESIDENTIAL", "EXTERIOR NON-RESIDENTIAL"]:```
    - CONTINUE TO RULE LOGIC
- if the applicability logic arrives here without going to rule logic, the rule is not applicable: RULE NOT APPLICABLE

## Rule Logic:  

- create a list of surfaces that do not comply with this rule: ```non_compliant_surface_ids = []```
  
- Get surface conditioning category dictionary for P_RMD: ```scc_dictionary_p = get_surface_conditioning_category(P_RMD)```  

- For each building surface in the Baseline model: ```for building_surface_b in B_RMD...surfaces:```
  - if the surface does not have the same surface conditioning category in the proposed and baseline, need to check if the exception applies: ```if scc_dictionary_b[building_surface_b.id] != scc_dictionary_p[building_surface_b.id]:```
    - according to the exception, if the surface is semi-heated ("SEMI-EXTERIOR") in the proposed design, it might be classified as fully-conditioned in the baseline, if, according to sizing runs, the zone is served by HVAC equipment that meets the requirements of a fully-conditioned space.  The function get_surface_conditioning_category runs these checks, so we just need to check the conditioning types.  First, check whether the proposed conditioning type is SEMI-EXTERIOR: ```if scc_dictionary_p[building_surface_b.id] == "SEMI-EXTERIOR":```
      - if the baseline is NOT one of the fully-conditioned surface types ("EXTERIOR MIXED", "EXTERIOR RESIDENTIAL", "EXTERIOR NON-RESIDENTIAL"), add this surface ID to the list of non compliant surface ids: ```if !(scc_dictionary_b[building_surface_b.id] in ["EXTERIOR MIXED", "EXTERIOR RESIDENTIAL", "EXTERIOR NON-RESIDENTIAL"]: non_compliant_surface_ids.append(building_surface_b.id)```
    - Otherwise, the exception is not met, add the id of this surface to the list of non compliant surface ids: ```else: non_compliant_surface_ids.append(building_surface_b.id)```

**Rule Assertion:**  
Case 1: If the non_compliant_surface_ids list has a length of 0, then PASS: ```if len(non_compliant_surface_ids) == 0: PASS```
Case 2: All other cases, FAIL: ```else: FAIL```

**Notes:**


**[Back](../_toc.md)**
