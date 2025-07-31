# Section 1 - Rule 1-1
**Schema Version:** 0.0.36  
**Mandatory Rule:** True  
**Rule ID:** 1-1  
**Rule Description:** Building performance factors shall be from Standard 90.1-2019, Table 4.2.1.1, based on the building area type and climate zone. For building area types not listed in Table 4.2.1.1  “All others.” shall be used to determine the BPF.  
**Rule Assertion:** Options are PASS/FAIL/UNDETERMINED     
**Appendix G Section:** Section 4.2.1.1  
**90.1 Section Reference:** None  

**Data Lookup:** Table 4.2.1.1 

**Evaluation Context:** RPD

**Applicability Checks:** None

**Function Calls:**
get_BPF_building_area_types_and_zones()

## Rule Logic:
- Create a set of the BPF values used in the RMDs: `output_bpf_set = set([B_0_RMD.output.total_area_weighted_building_performance_factor, B_90_RMD.output.total_area_weighted_building_performance_factor, B_180_RMD.output.total_area_weighted_building_performance_factor, B_270_RMD.output.total_area_weighted_building_performance_factor, P_RMD.output.total_area_weighted_building_performance_factor, U_RMD.output.total_area_weighted_building_performance_factor])`
- If the length of the set is greater than 1, raise a message and return FAIL: `if len(output_bpf_set) > 1: FAIL and raise_message "More than one BPF value was used in the project."`

- Get the dictionary of interpreted BPF building area types for the project: `bpf_building_area_type_dict = get_BPF_building_area_types_and_zones(B_0_RMD)`
- If the BPF building area type dictionary contains any building segments with UNDETERMINED BPF building area type, has_undetermined=TRUE (can skip remaining logic and proceed to rule assertion from here): `if "UNDETERMINED" in bpf_building_area_type_dict: has_undetermined = True`
- Get the project climate zone: `climate_zone = RulesetProjectDescription.weather.climate_zone`
- Create a variable to store the summed product of BPF and Area: `bpf_bat_sum_prod = 0`
- Create a variable to store the Total Area: `total_area = 0`
- Iterate through the building area type(s) in the BPF building area type dictionary: `for bpf_bat in bpf_building_area_type_dict:`
  - Get the expected BPF value from Table 4.2.1.1 based on building area and climate zone: `expected_bpf = data_lookup(Table_4_2_1_1, bpf_bat, climate_zone)`
  - Add the area to the total: `total_area += bpf_building_area_type_dict[bpf_bat]["AREA"]`
  - Add the product of expected BPF and area to the expected summed product of BPF and area: `bpf_bat_sum_prod += (expected_bpf * bpf_building_area_type_dict[bpf_bat]["AREA"])`

**Rule Assertion:**
- If has_undetermined is TRUE; outcome=UNDETERMINED: `if has_undetermined: UNDETERMINED and raise_message "One or more building area types could not be determined for the project's building segments. Assigning a lighting building area type to all building segments will fix this issue."`
- Else if the output BPF matches the expected BPF; outcome=PASS: `elif bpf_bat_sum_prod/total_area == output_bpf_set[0]: PASS`
- Otherwise, outcome=FAIL: `else: FAIL`

**Notes/Questions:** 
1. Rule assertion at the RMD level, not at the building level. For projects that include more than one building, there will be a single compliance calculation that includes all buildings.
2. The way this is written will also cover the requirements of rule 1-2 without needing to repeat the logic of get_BPF_building_area_types_and_zones() again.

**[Back](../_toc.md)**