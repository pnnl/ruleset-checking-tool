
# Envelope - Rule 5-39  

**Rule ID:** 5-39  
**Rule Description:** It is acceptable to use either an annual average ground temperature or monthly average ground temperatures for calculation of heat loss through basement floors.  
**Rule Assertion:** B-RMR ASHRAE229:weather.monthly_ground_temperature != NULL  
**Appendix G Section:** Section 5 Envelope  
**Appendix G Section Reference:** Section G3.1-14(b) Building Envelope Modeling Requirements for the Proposed design and Baseline  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  None  

**Manual Check:** Yes  
**Evaluation Context:** Each Data Element  
**Data Lookup:** None  
**Function Call:** None  

## Rule Logic:  

**Rule Assertion:**  

- Case 1: If B-RMR includes annual average or monthly average ground temperature: `if B_RMR.ASHRAE229.weather.monthly_ground_temperature: PASS`

- Case 2: Else: `else: FAIL`


**Notes:**
1. Do we need to check if RMR has basement floors and only apply this rule to models with basement floors?
2. Update Rule ID from 5-52 to 5-39 on 10/26/2023

**[Back](../_toc.md)**

**Notes:**
