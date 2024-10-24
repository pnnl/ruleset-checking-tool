# Section 19 - Rule 19-3     
**Schema Version:** 0.0.29  
**Mandatory Rule:** False    
**Rule ID:** 19-3     
**Rule Description:** Weather conditions used in sizing runs to determine baseline equipment capacities shall be based either on design days developed using 99.6% heating design temperatures and 1% dry-bulb and 1% wet-bulb cooling design temperatures.    
**Rule Assertion:** Options are UNDETERMINED     
**Appendix G Section:** G3.1.2.2.1      
**90.1 Section Reference:** None  

**Data Lookup:** None  

**Evaluation Context:** Each RulesetProjectDescription

**Applicability Checks:** None  

**Function Calls:**  None

## Rule Logic:
- Get the weather for the ruleset project description: `weather = RulesetProjectDescription.weather`

- **Rule Assertion:**
- Case 1: Heat/cooling design day types were not specified, conduct manual check; outcome=UNDETERMINED: `if (weather.cooling_design_day_type == NULL or weather.heating_design_day_type == NULL): UNDETERMINED and raise_message "Check that the weather conditions used in sizing runs to determine baseline equipment capacities is based on design days developed using 99.6% heating design temperatures and 1% dry-bulb and 1% wet-bulb cooling design temperatures."`
- Case 2: Heating/cooling design day types do not match the definitions in 90.1-2019; outcome=NOT_APPLICABLE: `elif (weather.cooling_design_day_type != COOLING_1_0 or weather.heating_design_day_type != HEATING_99_6): NOT_APPLICABLE`
- Case 3: Otherwise, conduct manual check that rule is met; outcome=UNDETERMINED:  `else: UNDETERMINED and raise_message "Check that the weather conditions used in sizing runs to determine baseline equipment capacities is based on design days developed using 99.6% heating design temperatures and 1% dry-bulb and 1% wet-bulb cooling design temperatures."`  


**Notes/Questions:**  None

**[Back](_toc.md)**