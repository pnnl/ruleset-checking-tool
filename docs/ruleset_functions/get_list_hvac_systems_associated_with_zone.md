# get_list_hvac_systems_associated_with_zone

**Schema Version:** 0.0.23
**Description:** Get the list of the heating ventilaiton and cooling system ids associated with a zone in either the U_RMR, P_RMR, or B_RMR.    

**Inputs:**  
- **U-RMR or P-RMR or B-RMR**: The U-RMR, P-RMR or B-RMR to evaluate to get the list of the heating ventilaiton and cooling system ids associated with a zone in either the U_RMR, P_RMR, or B_RMR. 
- **Zone ID**: The zone.id for which the list of associated heating ventilation and cooling system will be generated.  

**Returns:**  
- **list_hvac_systems_associated_with_zone**: A list that saves all the HVAC systems associated with the zone.  
 
**Function Call:** None

## Logic:  
- Set the zone object equal to the zone with zone.id for the RMR (P, B, or U) input to the function: `zone = RMR...zone.id `
- For each terminal in zone: `for terminal in zone.terminals:`
    - Get HVAC system serving terminal: `hvac = terminal.served_by_heating_ventilating_air_conditioning_system`
    - Add to list of applicable_hvac_systems_list as the code loops through the terminal units: `list_hvac_systems_associated_with_zone = list_hvac_systems_associated_with_zone.append(list_hvac_systems_associated_with_zone)`                        
- Convert the list of list_hvac_systems_associated_with_zone to a set and the back to a list to eliminate duplicates after looping through all zones: `list_hvac_systems_associated_with_zone = list(set(list_hvac_systems_associated_with_zone))`       

 **Returns** `return list_hvac_systems_associated_with_zone`  

**[Back](../_toc.md)**