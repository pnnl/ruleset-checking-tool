# is_terminal_heat_source_none   

**Description:** Returns TRUE if the heat source associated with the terminal unit is None or Null. It returns FALSE if the terminal unit has a heat source other than None or Null.   

**Inputs:**  
- **B-RMR**: To evaluate if the heat source associated with the terminal unit is None or Null.   
- **terminal_b.id**: The id of the terminal unit to evaluate.  

**Returns:**  
- **is_terminal_heat_source_none**: The function returns TRUE if the heat source associated with the terminal unit is None or Null. It returns FALSE if the terminal unit has a heat source other than None or Null.  
 
**Function Call:**  
1. get_hvac_zone_list_w_area()  


## Logic: 
- Get dictionary list of baseline zones and the associated HVAC systems: `hvac_zone_list_w_area_dict_b = get_hvac_zone_list_w_area (B_RMR)`  
- Get list of zones that the HVAC system serves (should only be one): `zone_list_b = hvac_zone_list_w_area_dict_b[hvac_b.id]["ZONE_LIST"]`  
- Create an object for the zone associated with the HVAC system (should only be one since this function is for single zone systems only): `zone_b = zone_list_b[0]`
- Check that there is only one terminal unit associated with the zone: `if len(zone_b.terminals) == 1:`  
    - Get and store the terminal unit object: `terminal_obj = zone_b.terminals[0]`    
- Else, terminal_obj_ equals Null: `Else: terminal_obj = Null` 
- Create an object for the terminal unit: `terminal_b = terminal_b.id`  
- Check if the heat source associated with the terminal unit equals None or is Null: `if terminal_b.heating_source == "None" or terminal_b.heating_source == Null: is_terminal_heat_source_none = TRUE`
- Else: `Else: is_terminal_heat_source_none = FALSE`

**Returns** `return is_terminal_heat_source_none`  

**[Back](../_toc.md)**
