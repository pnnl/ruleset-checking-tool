# is_baseline_system_1  

**Description:** Get a TRUE or FALSE output as to whether the HVAC system is ASHRAE 90.1 2019 Appendix G system 1.  

**Inputs:**  
- **B-RMR**: To evaluate if the hvac system is system 1 in the B_RMR.   
- **hvac_b.id**: The id of the hvac system to evaluate.  

**Returns:**  
- **is_baseline_system_1**: The functions returns TRUE if the system is system 1 and FALSE if the system is not system 1.  
 
**Function Call:** None  

## Logic:  
- Check that there is only one heating system, one cooling system and no preheat system associated with the HVAC system. If any of these criteria are not met then the function should return FALSE: `if Len(hvac_b.id.heating_system) == 1 AND Len(hvac_b.id.cooling_system) == 1 AND Len(hvac_b.id.preheat_system) == Null then:`  
    
