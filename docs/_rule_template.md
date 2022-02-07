The following provides a template with general instructions for creating a Rule Definition Strategy (RDS) document for defining rules in the Ruleset Checking Tool.  

# <SECTION_NAME> - Rule <RULE_ID>
**Rule ID:** The unique string identifier used to identify the rule within the ruleset.  
**Rule Description:** A textual description of the rule intended to be human readable. This description is included in the output JSON created by the RCT.  
**Rule Assertion:** The logical assertion that is applied to determine the outcome of a rule evaluation. Options are []   
**Appendix G Section:** The section number reference to the rule within Standard 90.1. e.g., *Section G3.1-5(b) Building Envelope Modeling Requirements for the Baseline building.*    
**Appendix G Section Reference:**
- A list of references to other ruleset sections used within the rule.
- Use *None* if no references are required. 

**Data Lookup:** A reference to specific data tables within ASHRAE 90.1 that are required for the rule evaluation. e.g., *Tables G3.4-1 to G3.4-8*  
**Evaluation Context:** A string signifying at what level with the RMR data tree the rule evaluation must occur. Options are *Each Data Element* and *Data Group*. 
- When defined as *Each Data Element* the rule entire scope of the rule evaluation occurs at each data element in the defined group. This implies a separate applicability check, manual check, and rule assertion for each data element. An individual output is written for each data element within the group.
- A rule that is evaluated at a *Data Group* is evaluated once for the relevant data group. This type of evaluation usually involves aggregating or calculating values up to the data group level prior to applying the assertion. A single output is written for the entire data group evaluation.  

**Applicability Checks:** 
1. A list of all applicability checks with brief narrative description.  
2. Implementation of applicability check should be included within the rule logic section of the RDS.
3. Applicability check should be formatted as an enumerated list.

**Manual Checks:**  
1. A list of all manual checks with brief narrative description.  
2. Implementation of manual check should be included within the rule logic section of the RDS.
3. Manual checks should be formatted as an enumerated list.

**Function Calls:**  
1. A list of all functions that this rule utilizes.  
2. Functions should be formatted as an enumerated list.

## Rule Logic:
- This section defines the logical evaluation of a rule using pseudocode. This description is used to develop the Rule Definition code in the RCT representing the rule.  
    - A nested list structure should be used to denote code that operates iteratively, such as within a For Loop.
        - Further nesting can be used, if required to iterate through data elements in the RMR file.
- The format of a Applicability Check should follow the following:  
**Applicability Check 1:** `(Example) if calculated_value > threshold:`  
    - Applicability Checks should be placed within the appropriate location of the code structure. These checks should be written to affirm whether a rule is applicable to a data element or data group. More than one Applicability Checks may be used, if necessary. 
    - The RCT will automatically handle cases that fail the Applicability Checks by outputting a *NOT_APPLICABLE* outcome. No additional description in the RDS is required for cases failing Applicability Checks.
    - A Rule Assertion should be provided where appropriate within the code structure. The Rule Assertion should be a simple logical evaluation that is used to determine one of the four possible outcomes for a Rule Evaluation. Examples of possible Rule Assertion outcomes are: *PASS*, *FAIL*, *UNDETERMINED*    
- A Rule Assertion section should be definined within the appropriate level of the code structure, so that the rule can be evaluated for each relevant data element in the RMR.
- The Rule Assertion should generally follow the following format:  
**Rule Assertion:** 
    - Define quantity, unit, precision for the evaluation" `(Example) if calculated_value == expected_value: outcome == "PASS"`
    - Define quantity, unit, precision for the evaluation: `(Example) elif calculated_value > expected_value: outcome == "UNDETERMINED"` 
    - Define quantity, unit, precision for the evaluation: `(Example) else: outcome == "FAIL"`   

**[Back](_toc.md)**