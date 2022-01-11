
# Boiler - Rule 21-1  

**Rule ID:** 21-1  
**Rule Description:** For systems using purchased hot water or steam, the heating source shall be modeled as
purchased hot water or steam in both the proposed design and baseline building design. If any system in the proposed design uses purchased hot water or steam, all baseline systems with hot water coils shall use the same type of purchased hot water or steam.  
**Rule Assertion:** B-RMR = expected value  
**Appendix G Section:** Section 21 Boiler  
**Appendix G Section Reference:** Section G3.1.1.1 & G3.1.1.3.1 Building System-Specific Modeling Requirements for the Baseline model  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:** None  

**Manual Check:** Yes  
**Evaluation Context:** Building  
**Data Lookup:** None  
**Function Call:** 

1. check_purchased_chw_hhw()

## Rule Logic:  

- Check if P-RMR is modeled with purchased cooling or purchased hot water/steam: `purchased_chw_hhw_status_dict = check_purchased_chw_hhw(P_RMR)`

  - If P-RMR is not modeled with purchased hot water or steam: `if NOT purchased_chw_hhw_status_dict["PURCHASED_HEATING"]:`

    - Check if B-RMR is modeled with any external fluid source that is hot water or steam type: `if external_fluid_source_b.type in ["HOT_WATER", "STEAM"] for external_fluid_source_b in B_RMR.ASHRAE229.external_fluid_source:`

      **Rule Assertion:** Case 1. Fail: `FAIL`

    - Else, B-RMR is not modeled with any external fluid source that is hot water or steam type: `else:`

      **Rule Assertion:** Case 2. Pass: `PASS`

  - Else, P-RMR is modeled with external fluid source that is hot water or steam type: `else:`
  
    **Rule Assertion:** Case 3. Undetermined: `UNDETERMINED and raise_message "P-RMR IS MODELED WITH PURCHASED HOT WATER OR STEAM. VERIFY B-RMR HEATING SOURCE IS MODELED CORRECTLY."`

**[Back](../_toc.md)**

**Notes:**

1. What if P-RMR is modeled with purchased hot water and steam, which source should be modeled in the baseline?
2. Can SHW also be served by purchased HHW or steam?
3. How to make sure that the external fluid source is used by system in P-RMR? Maybe it's just a orphan object.
