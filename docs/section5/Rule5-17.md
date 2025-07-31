
# Envelope - Rule 5-17  

**Schema Version:** 0.0.23
**Rule ID:** 5-17  
**Rule Description:** The baseline fenestration area for an existing building shall equal the existing fenestration area prior to the proposed work.  
**Rule Assertion:** B-RMD total (subsurface.glazed_area+subsurface.opaque_area) = expected value  
**Appendix G Section:** Section 5 Envelope  
**Appendix G Section Reference:** Section G3.1-5(c) Building Envelope Modeling Requirements for the Baseline building  

**Data Lookup:** None  
**Evaluation Context:**  Each Data Element  

**Applicability Checks:** 

1. The baseline building has existing or altered spaces

**Manual Checks:** Yes  
**Function Call:**  None  

## Rule Logic:
- create undetermined_zone_list: `undetermined_zone_list = []`

- For each zone in B_RMR: `for zone_b in B_RMR...zones:`

  - For each space in zone: `for space_b in zone_b.spaces:`

    - Check if space is existing or altered, set rule applicability check to True: `if ( space_b.status_type == EXISTING ) OR ( space_b.status_type == ALTERED ): rule_applicability_check = TRUE`

      - Add to total number of existing or altered spaces in zone: `num_space_existing_altered += 1`

      - Add to array of zones with existing or altered spaces if not already saved: `if NOT zone_b in undetermined_zone_list: undetermined_zone_list.append(zone_b)`

**Rule Assertion - Component:**

    - For each zone, if any space in zone is existing or altered: `if num_space_existing_altered > 0: UNDETERMINED"`

**Rule Assertion - RMR:**

- Case 1: If any zone in B-RMR is ruled as "UNDETERMINED": `UNDETERMINED and raise_message "PART OR ALL OF ZONES LISTED BELOW IS EXISTING OR ALTERED. THE BASELINE VERTICAL FENESTRATION AREA FOR EXISTING ZONES MUST EQUAL TO THE FENESTRATION AREA PRIOR TO THE PROPOSED SCOPE OF WORK. THE BASELINE FENESTRATION AREA IN ZONE MUST BE CHECKED MANUALLY. ${undetermined_zone_list}"`

**Applicability Check:** For each building, if no space is existing or altered, rule is not applicable: `if NOT rule_applicability_check: is_applicable = FALSE`

**Notes:**

1. Update Rule ID from 5-22 to 5-18 on 10/26/2023
2. Update Rule ID from 5-18 to 5-17 on 12/22/2023

**[Back](../_toc.md)**
