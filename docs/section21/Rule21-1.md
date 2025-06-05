
# Boiler - Rule 21-1  

**Rule ID:** 21-1  
**Rule Description:** For systems using purchased hot water or steam, the heating source shall be modeled as
purchased hot water or steam in both the proposed design and baseline building design. If any system in the proposed design uses purchased hot water or steam, all baseline systems with hot water coils shall use the same type of purchased hot water or steam.  
**Rule Assertion:** B-RMR = expected value  
**Appendix G Section:** Section 21 Boiler  
**Appendix G Section Reference:** Section G3.1.1.1 & G3.1.1.3.1 Building System-Specific Modeling Requirements for the Baseline model  
**Schema Version:** 0.0.25

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  

1. P-RMR is modeled with purchased hot water or steam.

**Manual Check:** Yes  
**Evaluation Context:** Building  
**Data Lookup:** None  
**Function Call:** 

1. check_purchased_chw_hhw()
2. get_baseline_system_types()
3. baseline_system_type_compare()

**Applicability Checks:**

- Check if P-RMR is modeled with purchased chilled water or purchased hot water/steam: `purchased_chw_hhw_status_dict = check_purchased_chw_hhw(P_RMR)`

  - If P-RMR is not modeled with purchased hot water/steam, rule is not applicable to B-RMR: `if NOT purchased_chw_hhw_status_dict["PURCHASED_HEATING"]: NOT_APPLICABLE`

  - Else, P-RMR is modeled with purchased hot water/steam, continue to rule logic: `else: CHECK_RULE_LOGIC`

## Rule Logic:  

- get baseline system types: `baseline_hvac_system_dict = get_baseline_system_types(B_RMI)`
- Check if B-RMR is modeled with any air-side system that is Type-1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 1a, 3a, 7a, 8a, 11a, 12a, 13a, i.e. any air-side system using heating source other than purchased hot water or steam, set check flag to True: `if any(baseline_system_type_compare(sys_type, target_system_type, true) for sys_type in baseline_hvac_system_dict.keys() for target_system_type in [HVAC.SYS_1, HVAC.SYS_2, HVAC.SYS_3, HVAC.SYS_4, HVAC.SYS_5, HVAC.SYS_6, HVAC.SYS_7, HVAC.SYS_8, HVAC.SYS_9, HVAC.SYS_10, HVAC.SYS_11, HVAC.SYS_12, HVAC.SYS_13, HVAC.SYS_1A, HVAC.SYS_3A, HVAC.SYS_7A, HVAC.SYS_8A, HVAC.SYS_11A, HVAC.SYS_12A, HVAC.SYS_13A]): check_flag = TRUE`

**Rule Assertion:**

- Case 1: If check flag is True: `if check_flag: NOT_APPLICABLE`

- Case 2: Else: `else: UNDETERMINED and raise_message "P-RMR IS MODELED WITH PURCHASED HOT WATER OR STEAM. VERIFY B-RMR HEATING SOURCE IS MODELED CORRECTLY."`

**[Back](../_toc.md)**
