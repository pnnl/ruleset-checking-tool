
# Airside System - Rule 23-4 

**Schema Version:** 0.0.34  
**Mandatory Rule:** False  
**Rule ID:** 23-4  
**Rule Description:** Baseline systems 5 & 7 serving lab spaces per G3.1.1c shall reduce lab exhaust and makeup air during unoccupied periods to 50% of zone peak airflow, the minimum outdoor airflow, or rate required to comply with minimum accreditation standards whichever is larger.
**Rule Assertion:** B-RMD = expected value  
**Appendix G Section:** Section 23 Air-side  
**90.1 Section Reference:** Exception to G3.1.3.13 VAV Minimum Flow Set Points (Systems 5 and 7)  
**Data Lookup:** None  
**Evaluation Context:** Building  

**Applicability Checks:**  

1. B-RMD is modeled with at least one air-side system that is Type-5 or 7 and serves only lab spaces.  

**Function Calls:**  

1. get_baseline_system_types()
2. baseline_system_type_compare()
3. get_lab_zone_hvac_systems()

**Applicability Checks:**  
- create a list of the target system types: `APPLICABLE_SYS_TYPES = [HVAC_SYS.SYS_5, HVAC_SYS.SYS_7]`
- Get B-RMD system types: `baseline_hvac_system_dict = get_baseline_system_types(B-RMD)`
- Get climate zone: `climate_zone_b = ASHRAE229.weather.climate_zone`    
- Get is_leap_year: `is_leap_year_b = ASHRAE229.calendar.is_leap_year`  

- make a list of hvac system type ids for systems that are one of 5 or 7: `hvac_sys_5_or_7_list = []`
- loop through the applicable system types: `for target_sys_type in APPLICABLE_SYS_TYPES:`
    - and loop through the baseline_system_types_dict to check the system types of the baseline systems: `for system_type in baseline_system_types_dict:`
        - do baseline_system_type_compare to determine whether the baseline_system_type is the applicable_system_type: `if((baseline_system_type_compare(system_type, target_sys_type, false)):`
            - the systems in the list: baseline_system_types_dict[system_type] are either sys-5 or 7, add them to hvac_sys_5_or_7_list: `hvac_sys_5_or_7_list.extend(baseline_system_types_dict[system_type])`
- use the function get_lab_zone_hvac_systems to get a list of systems serving lab zones: `hvac_systems_serving_lab_zones = get_lab_zone_hvac_systems(B-RMD, P-RMD, climate_zone, is_leap_year)`
- we'll iterate through the hvac systems serving labs.  hvac_systems_serving_lab_zones has two keys - one indicating "LAB_ZONES_ONLY" and one indicating "LAB_AND_OTHER", because this rule references G3.1.1c, which requires systems to serve only lab zones, we will concern ourselves only with "LAB_ZONES_ONLY": `for hvac_system_id in hvac_systems_serving_lab_zones["LAB_ZONES_ONLY"]:`
      - now check if this system is a System 5 or System 7 by looking for the hvac_system_id in hvac_sys_5_or_7_list, it is, the rule is applicable: `if(hvac_system_id in hvac_sys_5_or_7_list): UNDETERMINED`

      - Else, rule is not applicable to B-RMD: `else: RULE_NOT_APPLICABLE`

**Notes:**

**[Back](../_toc.md)**
