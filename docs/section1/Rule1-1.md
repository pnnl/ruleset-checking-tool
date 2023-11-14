# Section 1 - Rule 1-1
**Schema Version:** 0.0.29  
**Mandatory Rule:** True  
**Rule ID:** 1-1
**Rule Description:** Building performance factors shall be from Standard 90.1-2019, Table 4.2.1.1, based on the building area type and climate zone. For building area types not listed in Table 4.2.1.1  “All others.” shall be used to determine the BPF.
**Rule Assertion:** Options are Pass/Fail/IN_APPLICABLE     
**Appendix G Section:** Section 4.2.1.1  
**90.1 Section Reference:** None  

**Data Lookup:** Table 4.2.1.1 

**Evaluation Context:** Output2019ASHRAE901

**Applicability Checks:**
1. Applies to projects with only 1 building area type

**Function Calls:**
get_area_type_bpf()

## Rule Logic:   
**Applicability Check - Check if there is only 1 building area type for the project**  
- Get the project building area type: `building_area_type = `
- Get the project climate zone: `climate_zone = ASHRAE229.weather.climate_zone`
- Get the expected BPF value from Table 4.2.1.1 based on building area and climate zone: `expected_bpf = data_lookup(Table_4_2_1_1, building_area_type)`
- Get the output BPF value: `output_bpf = Output2019ASHRAE901.total_area_weighted_building_performance_factor`
**Rule Assertion:**
- If the output BPF matches the expected BPF; outcome=PASS: `if output_bpf == expected_bpf: PASS`
- Otherwise, outcome=FAIL: `else: FAIL`

**Notes/Questions:** None


**[Back](../_toc.md)**