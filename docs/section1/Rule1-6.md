
# Section 1 - Rule 1-6 

**Rule ID:** 1-6   
**Rule Description:** On-site renewable energy shall not be included in the baseline building performance.  
**Rule Assertion:** Baseline RMD = expected value  
**Appendix G Section:** G3.11 18 Baseline 

**Mandatory Rule:** True    
**Evaluation Context:** Each baseline RMD  
**Function Call:**  

## Applicability Check:  
- All projects are applicable


## Rule Logic:
- set a boolean has_renewables and set it to false: `has_renewables = false`
- look at each baseline model rotation: `for rotation in [B_RMD, B_RMD_90, B_RMD_180, B_RMD_270]:`
    - get the baseline output schema: `output = rotation.output`
    - get the output instance: `output_instance = output.output_instance`
    - look at each end use result: `for end_use_result in output_instance.annual_end_use_results:`
        - check if the energy source for the end_use_result is "ON_SITE_RENEWABLES": `if end_use_result.energy_source == "ON_SITE_RENEWABLES":`
            - check if the energy end use is greater than 0: `if end_us_result.annual_site_energy_use > 0:`
                - set has_renewables to true and continue to rule assertion: `has_renewables = true; CONTINUE TO RULE ASSERTION`
- if we get here without going to the rule assertion, continue to rule assertion: `CONTINUE TO RULE ASSERTION`

**Rule Assertion:**
- Case 1: If has_renewables is true, then FAIL: `if has_renewables == true: FAIL`
- Case 2: otherwise, there are no renewables, PASS: `else: PASS`


**Notes:**
1.  

**[Back](../_toc.md)**


