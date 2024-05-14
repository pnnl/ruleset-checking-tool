# HVAC_SystemZoneAssignment - Rule 18-1

**Schema Version:** 0.0.28  
**Mandatory Rule:** True  
**Rule ID:** 18-1  
**Rule Description:** HVAC system type selection is based on ASHRAE 90.1 G3.1.1 (a-h)  
**Rule Assertion:** Options are PASS/FAIL/NOT_APPLICABLE/UNDETERMINED  
**Appendix G Section Reference:** Table G3.1.1

**Evaluation Context:** Each Zone Data Group  
**Data Lookup:**   
**Function Call:**

1. get_zone_target_baseline_system()
2. baseline_system_type_compare()
3. get_list_hvac_systems_associated_with_zone()
4. get_baseline_system_types()
5. is_zone_a_vestibule()
6. get_building_lab_zones()

**Applicability Checks:**

- call the function
  get_zone_target_baseline_system(): `target_baseline_system_dict = get_zone_target_baseline_system(P_RMD, B_RMD)`
- if the zone is conditioned or semiheated and not dedicated to parking, the rule is applicable - the zone will only be
  in the dictionary provided by get_zone_target_baseline_system() if it is a zone which requires an HVAC
  system: `if zone in target_baseline_system_dict: continue to rule logic`
- otherwise: `else: result = NOT_APPLICABLE`

## Rule Logic:

- set the result to fail: `result = FAIL`
- set expected_system_type to the expected system type given by the
  target_baseline_system_dict: `expected_system_type = target_baseline_system_dict[zone]["EXPECTED_SYSTEM_TYPE"]`
- set the system_type_origin to the SYSTEM_ORIGIN given by the target_baseline_system_dict: `system_type_origin =
  target_baseline_system_type_dict[zone]["SYSTEM_ORIGIN"]
- get the baseline system types in the building: `baseline_hvac_system_dict = get_baseline_system_types(B-RMD)`
- now check whether the system(s) serving this zone match the expected system. Start by getting the list of HVAC systems
  that serve the zone: `hvac_systems_serving_zone = get_list_hvac_systems_associated_with_zone(B-RMD)`
- get a list of all of the HVAC systems that are of the same type as the expected system type for the
  zone: `systems_of_expected_type_list = baseline_hvac_system_dict[expected_system_type]`
- set enum result to FAIL this will be set to PASS once we start looking at systems: `result = FAIL`
- loop through the systems that serve the zone: `for system_b in hvac_systems_serving_zone:`
    - check to see if system_b is in the systems_of_expected_type_list: `if system_b in systems_of_expected_type_list:`
        - change result to PASS: `result = PASS`
        - otherwise, set result to FAIL and break out of the loop: `else: result = FAIL; break`
- create a variable advisory_note, which will give the user some feedback about how the HVAC system type was selected: `
  advisory_note = "HVAC system type " + expected_system_type + " was selected based on " + system_type_origin


- for most zones, we can simply return the result at this point, but there are some special cases that require a check
  for whether an UNDETERMINED needs to be returned. We need to do further work in the case of laboratories (G3_1_1d) and
  vestibules (G3_1_1e)
- check if the system_type_origin is "G3_1_1d" we need to determine whether the laboratory exhaust meets the threshold
  based solely on zone exhaust or not: `if system_type_origin == "G3_1_1d:"`
    - complete logic to determine whether we can give a hard PASS / FAIL or simply UNDETERMINED

- get a list of laboratory zones by calling the function
  get_building_lab_zones(): `laboratory_zones = get_building_lab_zones(P_RMD)`
- Now find the laboratory exhaust for each zone in the laboratory_zones list. Loop through each
  zone: `for z in laboratory_zones:`
    - Add zonal exhaust fan airflow to zone_total_exhaust: `if zone.zone_exhaust_fans ?:`
        - look at each exhaust fan: `for exhaust_fan in zone.zone_exhaust_fans:`
        - add the airflow to the zone total exhaust: `building_total_lab_exhaust += exhaust_fan.design_airflow`
        - if the building total lab exhaust is greater than 15,000cfm, then the system selection is solid and we can
          give a hard PASS or FAIL, but if it is less than 15,000cfm, the system selection was based in part on HVAC
          system exhaust and we can't guarantee that it's all laboratory exhaust. Check if the
          building_total_lab_exhaust is less than or equal to 15,000cfm: `if building_total_lab_exhaust <= 15,000:`
        - change the result to UNDETERMINED: `result = UNDETERMINED`    -
        - change the advisory_note
          to: `advisory_note = "HVAC system type " + expected_system_type + " was selected for this zone based on ASHRAE 90.1 Appendix G3.1.1.d, which reads: `
          For laboratory spaces in a building having a total laboratory exhaust rate greater than 15,000 cfm, use a
          single system of type 5 or 7 serving only those
          spaces.` We have determined that laboratory spaces in this building have a total exhaust greater than 15,000 cfm, but we cannot determine with certainty that at least 15,000cfm of the exhaust is dedicated to laboratory purposes. If the building laboratory exhaust is greater than 15,000cfm, the system type for this zone should be " + expected_system_type + "."`

- otherwise, if the system_type_origin is "G3_1_1e" we need to determine whether the zone in question is one that is
  potentially a vestibule. We can't determine with 100% certainty if a zone is a vestibule, and if the HVAC system type
  is selected based on the fact that it might be a vestibule, then we can't determine with 100% accuracy a pass or
  fail: `elsif system_type_origin == "G3_1_1e":`
    - complete logic to determine whether we can give a hard PASS / FAIL or simply undetermined
    - use the function `is_zone_a_vestibule` to determine whether the zone is a
      vestibule: `if is_zone_a_vestibule(zone, B_RMD) == MAYBE:`
        - if the zone is MAYBE a vestibule, we need to change the result to UNDETERMINED: `result = UNDETERMINED`
        - AND we need to change the advisory_note to let the user know that the system type selection was based on the
          zone being a
          vestibule: `advisory_note = "HVAC system type " + expected_system_type + " was selected for this zone based on ASHRAE 90.1 Appendix G.3.1.1.e which reads: `
          Thermal zones designed with heating-only systems in the proposed design serving storage rooms, stairwells,
          vestibules, electrical/mechanical rooms, and restrooms not exhausting or transferring air from mechanically
          cooled thermal zones in the proposed design shall use system type 9 or 10 in the baseline building design.`
          We expect that this space is a vestibule, but cannot make a determination with 100% accuracy. If the zone is
          one of the listed space types, then the system type should be " + expected_system_type

**Rule Assertion - Zone:**

- Case 1: the result variable is PASS - return PASS and provide the advisory_note to give additional information to the
  user: `if result == PASS: PASS; advisory_note`
- Case 2: the result variable is FAIL - return FAIL and provide the advisory_note to give additional information to the
  user:`if result == FAIL: FAIL; advisory_note`

- Case 3: the result variable is UNDETERMINED - return UNDETERMINED and provide the advisory_note to give additional
  information to the user: `if result == UNDETERMINED: UNDETERMINED; advisory_note`

**Notes:**

1. this rule is written such that if all of the systems serving the zone is the expected type, it passes. In Appendix G,
   only one system per zone is allowed in the baseline model, however, this is covered by another rule.
2. I strongly feel that if the system types don't match, we need to provide logic to tell the user why they don't match.
   The details of how to set up the various baseline system types can be seen as "rules" that are not reflected
   elsewhere in the schema.

**[Back](../_toc.md)**
