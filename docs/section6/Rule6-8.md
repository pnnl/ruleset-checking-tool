
# Lighting - Rule 6-8

**Rule ID:** 6-8
**Rule Description:** Baseline Interior Lighting Power Allowance for all spaces is determined based in Table G3.7 when lighting systems has been designed and submitted with design documents (space by space method is used).   
**Appendix G Section:** Table G3.1 Part 6 Lighting under Baseline Building Performance  
**Appendix G Section Reference:**  

- Table G3.7, Performance Rating Method Lighting Power Density Allowances and Occupancy Sensor Reductions Using the Space-by-Space Method

**Applicability:** All required data elements exist for B_RMR  
**Applicability Checks:**  

**Ruleset Functions:**  
  1. Check whether space by space method is being used.  

**Manual Check:** None  
**Evaluation Context:** Each Data Element  
**Data Lookup:** Table G3.7  
## Rule Logic: 

- **Ruleset Function 1:** ```is_space_by_space_method_used = <Ruleset Function 1>(B_RMR)```

- For each space in Baseline RMR: ```_space in ...spaces:```  

  - Get lighting_space_type: ```_lighting_space_type = space.lighting_space_type```  
    
    - Get the lighting power density allowance: ```_lighting_power_allowance = data_lookup(table_G_3_7, _lighting_space_type)```  

    - Get interior_lighting in space: ```_interior_lighting = _space.interior_lightings```  

    - Get the total design power_per_area for the space: ```_space_lighting_power_per_area = sum( _lighting.power_per_area for _lighting in _interior_lighting )``` 

     **Rule Assertion:** For each space in the baseline model: ```_space_lighting_power_per_area == _lighting_power_allowance```  
     
     **Note:** If space type = "sales area" and the baseline LPD doesnt align with G3.7, this could be due to additional retail lighting power allowance for display lighting. This space should include a CAUTION message and clarify that manual verification is required to verify the retail baseline LPD.
