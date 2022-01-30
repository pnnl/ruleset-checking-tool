
# Boiler - Rule 21-1  

**Rule ID:** 21-1  
**Rule Description:** For systems using purchased hot water or steam, the heating source shall be modeled as
purchased hot water or steam in both the proposed design and baseline building design. If any system in the proposed design uses purchased hot water or steam, all baseline systems with hot water coils shall use the same type of purchased hot water or steam.  
**Rule Assertion:** B-RMR = expected value  
**Appendix G Section:** Section 21 Boiler  
**Appendix G Section Reference:** Section G3.1.1.1 & G3.1.1.3.1 Building System-Specific Modeling Requirements for the Baseline model  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  

1. P-RMR is modeled with purchased hot water or steam.

**Manual Check:** Yes  
**Evaluation Context:** Building  
**Data Lookup:** None  
**Function Call:** 

1. check_purchased_chw_hhw()
2. get_baseline_system_types()

**Applicability Checks:**

- Check if P-RMR is modeled with purchased chilled water or purchased hot water/steam: `purchased_chw_hhw_status_dict = check_purchased_chw_hhw(P_RMR)`

  - If P-RMR is not modeled with purchased hot water/steam, rule is not applicable to B-RMR: `if NOT purchased_chw_hhw_status_dict["PURCHASED_HEATING"]: RULE_NOT_APPLICABLE`

  - Else, P-RMR is modeled with purchased hot water/steam, continue to rule logic: `else: CHECK_RULE_LOGIC`

## Rule Logic:  

- Check if B-RMR is modeled with any air-side system that is Type-1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 1a, 3a, 7a, 8a, 11a, 12a, 13a, i.e. any air-side system using heating source other than purchased hot water or steam, set check flag to True: `if any(sys_type in baseline_hvac_system_dict.keys() for sys_type in ["SYS-1", "SYS-2", "SYS-3", "SYS-4", "SYS-5", "SYS-6", "SYS-7", "SYS-8", "SYS-9", "SYS-10", "SYS-11", "SYS-12", "SYS-13", "SYS-1A", "SYS-3A", "SYS-7A", "SYS-8A", "SYS-11A", "SYS-12A", "SYS-13A"]): check_flag = TRUE`

**Rule Assertion:**

- Case 1: If check flag is True: `if check_flag: FAIL`

- Case 2: Else: `else: UNDETERMINED and raise_message "P-RMR IS MODELED WITH PURCHASED HOT WATER OR STEAM. VERIFY B-RMR HEATING SOURCE IS MODELED CORRECTLY."`

**[Back](../_toc.md)**
