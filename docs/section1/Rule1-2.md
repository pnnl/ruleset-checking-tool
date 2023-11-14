# Section 1 - Rule 1-2
**Schema Version:** 0.0.29  
**Mandatory Rule:** True  
**Rule ID:** 1-2  
**Rule Description:** Where a building has multiple building area types, the required BPF shall be equal to the area-weighted average of the building area types.
**Rule Assertion:** Options are Pass/Fail/IN_APPLICABLE     
**Appendix G Section:** None
**90.1 Section Reference:** Section 4.2.1.1   

**Data Lookup:** Table 4.2.1.1 

**Evaluation Context:** Output2019ASHRAE901

**Applicability Checks:**
1. Applies to projects with more than 1 building area type

**Function Calls:** None

## Rule Logic:   
**Applicability Check - Check if there is more than 1 building area type for the project**  
- APPLICABILITY CHECK HERE `APPLICABILITY CHECK HERE`

- Get the project climate zone: `climate_zone = ASHRAE229.weather.climate_zone`
- Initialize the total project area: `total_area = 0`
- Initialize the BPF*Area product sum value: `bpf_area_product_sum = 0`
- For each building segment in B_RMD: `for building_segment_b in B_RMD...building_segments:`
  - Get the building area type: `building_area_type = `
  - Get the expected BPF value from Table 4.2.1.1 based on building area type and climate zone: `building_area_expected_bpf = data_lookup(Table_4_2_1_1, building_area_type)`
  - Initialize the total area of the building area type: `building_area_total_area = 0`
  - For each space in building_segment_b: `for space_b in building_segment_b...spaces:`
    - Add the space area to the total area of the building area type: `building_area_total_area += space_b.floor_area`
  - Add the product of expected BPF and total area of the building area type to the product sum: `bpf_area_product_sum += building_area_total_area * building_area_expected_bpf`
- Calculate the expected total area weighted average BPF: `expected_bpf = bpf_area_product_sum/total_area`
- Get the output BPF value: `output_bpf = Output2019ASHRAE901.total_area_weighted_building_performance_factor`
**Rule Assertion:**
- If the output BPF matches the expected BPF; outcome=PASS: `if output_bpf == expected_bpf: PASS`
- Otherwise, outcome=FAIL: `else: FAIL`


**[Back](../_toc.md)**