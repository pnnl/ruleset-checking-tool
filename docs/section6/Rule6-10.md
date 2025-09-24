
# Lighting - Rule 6-10  

**Rule ID:** 6-10  
**Rule Description:** Lighting and miscellaneous equipment loads and schedules are modeled identically across the baseline and proposed for plenums, crawl spaces, and interstitial spaces.  
**Rule Assertion:** Proposed RMD = Baseline RMD    
**Appendix G Section:** Table G3.1 #1 Baseline Column  
**Appendix G Section Reference:** None  

**Applicability:** Spaces with a function defined as plenum, crawl space, or interstitial space.  
**Applicability Checks:**  

  1. Spaces with a function defined as plenum, crawl space, or interstitial space.

**Manual Check:** None  
**Evaluation Context:** Each Space  
**Data Lookup:** None  

**Function Call:**

1. compare_schedules()
2. normalize_space_schedules()
3. match_data_element()

## Rule Logic:  

- For each space in the proposed RMD: `for space_p in P_RMD...Space:`

  - **Applicability Check:** `if space_p.function not in [PLENUM, CRAWL_SPACE, INTERSTITIAL_SPACE]:`   
    - RULE_NOT_APPLICABLE: `continue`
  
  - **Rule Logic:**
  - Create boolean to track mismatch between baseline and proposed: `mismatch = False`  
  - Match baseline space: `space_b = match_data_element(B_RMD, Spaces, space_p.name)`  
  - If space not found then mismatch is TRUE: `if not space_b:`  
    - mismatch = True: `mismatch = True`  
    - No match found: `continue`  
  - Index baseline lighting by ID or name for quick lookup: `baseline_lighting = {obj.id: obj for obj in space_b.interior_lighting}`  
  - For each interior lighting object associated with space_p, compare each to baseline lighting object: `for lighting_p in space_p.interior_lighting:`  
    - Get analogous baseline lighting object: `lighting_b = baseline_lighting.get(lighting_p.id)`  
    - If lighting_b not found then mismatch is TRUE: `if not lighting_b:`  
      - mismatch = True: `mismatch = True`  
      - No match found: `continue` 
    - Compare attributes: `        if (
            lighting_b.power_per_area != lighting_p.power_per_area or
            lighting_b.occupancy_control_type != lighting_p.occupancy_control_type or
            lighting_b.daylighting_control_type != lighting_p.daylighting_control_type or
            not compare_schedules(
                lighting_p.lighting_multiplier_schedule,
                lighting_b.lighting_multiplier_schedule,
                method="1 for all 8760"
            )
        ):`  
      - Mismatch equals true: `mismatch = True`  
  - Index baseline misc by ID or name for quick lookup: `baseline_misc = {obj.id: obj for obj in space_b.miscellaneous_equipment}`  
  - For each misc equipment object associated with space_p, compare each to baseline misc object: `for misc_p in space_p.miscellaneous_equipment:`  
    - Get analogous baseline misc object: `misc_b = baseline_misc.get(misc_p.id)`  
    - If misc_b not found then mismatch is TRUE: `if not misc_b:`  
      - mismatch = True: `mismatch = True`  
      - No match found: `continue` 
    - Compare attributes: `        if (
            misc_b.energy_type != misc_p.energy_type or
            misc_b.power != misc_p.power or
            misc_b.sensible_fraction != misc_p.sensible_fraction or misc_b.latent_fraction != misc_p.latent_fraction or
            misc_b.remaining_fraction_to_loop != misc_p.remaining_fraction_to_loop or
            misc_b.energy_from_loop != misc_p.energy_from_loop or
            misc_b.automatic_controlled_percentage != misc_p.automatic_controlled_percentage or
            not compare_schedules(
                misc_p.multiplier_schedule,
                misc_b.multiplier_schedule,
                method="1 for all 8760"
            )
        ):`  
      - Mismatch equals true: `mismatch = True`  

  **Rule Assertion:**  
  - Case 1: If no mismatch was found then PASS: `if not mismatch: PASS`  
  - Case 2: if a mismatch was found then FAIL: `else: FAIL and raise_message "It is expected that lighting and miscelleneous equipment would be modeled identically across the baseline and proposed for plenums, crawl spaces, and interstitial spaces. A mismatch was observed for <include space id and the mismatches observed>" `   

**Notes:**
1. Could the interiorlighting and misc objects have different IDS across the baseline and proposed, if so how do we match them up ?  

**[Back](../_toc.md)**
