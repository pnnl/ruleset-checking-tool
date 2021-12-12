
# Boiler - Rule 21-6  

**Rule ID:** 21-6  
**Rule Description:** When baseline building includes two boilers each shall stage as required by load.  
**Rule Assertion:** B-RMR  
**Appendix G Section:** Section 21 Boiler  
**Appendix G Section Reference:** Section G3.1.3.2 Building System-Specific Modeling Requirements for the Baseline model  

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  

1. B-RMR is modeled with at least one air-side system that is Type-1, 5, 7, 11, or 12
2. B-RMR is not modeled with purchased heating.
3. B-RMR is modeled with two boilers.

**Manual Check:** None  
**Evaluation Context:** Building  
**Data Lookup:** None  
**Function Call:** None  

**Applicability Checks:**  

1. B-RMR is modeled with at least one air-side system that is Type-1, 5, 7, 11, or 12: `PLACEHOLDER`
2. B-RMR is not modeled with purchased heating: `if RULE-21-1 == "NOT APPLICABLE":`
3. B-RMR is modeled with two boilers: `if ( Rule-21-5 == PASS ) AND ( LEN(B_RMR.ASHRAE229.boilers) == 2):`

## Rule Logic:  

- Get both boilers in B_RMR: `boiler_1 = B_RMR.ASHRAE229.boilers[0], boiler_2 = B_RMR.ASHRAE229.boilers[1]`

**Rule Assertion:**

- Case 1: If boiler_1's operation lower limit is 0 and operation upper limit is equal to its rated capacity, and boiler_2's operation lower limit is equal to its rated capacity and operation upper limit is equal to twice its rated capacity: `if ( boiler_1.operation_lower_limit == 0 ) AND ( boiler_1.operation_upper_limit == boiler_1.rated_capacity ) AND ( boiler_2.operation_lower_limit == boiler_2.rated_capacity ) AND ( boiler_2.operation_upper_limit == boiler_2.rated_capacity * 2 ): PASS`

- Case 2: If boiler_2's operation lower limit is 0 and operation upper limit is equal to its rated capacity, and boiler_1's operation lower limit is equal to its rated capacity and operation upper limit is equal to twice its rated capacity: `if ( boiler_2.operation_lower_limit == 0 ) AND ( boiler_2.operation_upper_limit == boiler_2.rated_capacity ) AND ( boiler_1.operation_lower_limit == boiler_1.rated_capacity ) AND ( boiler_1.operation_upper_limit == boiler_1.rated_capacity * 2 ): PASS`

- Case 3: Else: `else: FAIL`

**[Back](../_toc.md)**
