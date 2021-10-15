
# Envelope - Rule 5-22  

**Rule ID:** 5-22  
**Rule Description:** The baseline fenestration area for an existing building shall equal the existing fenestration area prior to the proposed work.  
**Rule Assertion:** B-RMR total (subsurface.glazed_area+subsurface.opaque_area) = expected value  
**Appendix G Section:** Section 5 Envelope  
**Appendix G Section Reference:** Section G3.1-5(c) Building Envelope Modeling Requirements for the Baseline building  

**Data Lookup:** None  
**Evaluation Context:**  Each Data Element  

**Applicability Checks:** 

1. The baseline building has existing or altered spaces

**Manual Checks:** Yes  
**Function Call:**  None  

## Rule Logic:

- For each zone in B_RMR: `for zone_b in B_RMR...zones:`

  - For each space in zone: `for space_b in zone_b.spaces:`

    - Check if space is existing or altered, set rule applicability check to True: `if ( space_b.status_type == "EXISTING" ) OR ( space_b.status_type == "ALTERATION" ): rule_applicability_check = TRUE`

      - Add to total number of existing or altered spaces in zone: `num_space_existing_altered += 1`

**Rule Assertion:**

- For each zone, if any space in zone is existing or altered: `if num_space_existing_altered > 0: CAUTION and raise_warning "PART OR ALL OF ZONE IS EXISTING. THE BASELINE VERTICAL FENESTRATION AREA FOR EXISTING ZONES MUST EQUAL TO THE FENESTRATION AREA PRIOR TO THE PROPOSED SCOPE OF WORK. THE BASELINE FENESTRATION AREA IN ZONE MUST BE CHECKED MANUALLY."`

**Applicability Check:** For each building, if no space is existing or altered, rule is not applicable: `if NOT rule_applicability_check: is_applicable = FALSE`

**[Back](../_toc.md)**
