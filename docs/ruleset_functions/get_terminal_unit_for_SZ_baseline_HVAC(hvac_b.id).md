# get_terminal_unit_for_SZ_baseline_HVAC

**Description:** Get the terminal unit object associated with a single zone hvac system in the baseline model.  The function returns the terminal unit object associated with the hvac system ID input to the function. If there is more than one terminal unit associated with the HVAC system or no terminal units associated with the HVAC system then return Null.

**Inputs:**
- **B-RMR**: To get the terminal unit object associated with the single zone HVAC system ID input to the function.   
- **hvac_b.id**: The id of the hvac system to evaluate.  

**Returns:**
- **terminal_obj**: A terminal unit object. Returns Null if there is more than one terminal unit associated with the HVAC system or no terminal units associated with the HVAC system.

**Function Call:**  
1. get_hvac_zone_list_w_area()  

## Logic:  
- Get dictionary list of baseline zones and the associated HVAC systems: `hvac_zone_list_w_area_dict_b = get_hvac_zone_list_w_area (B_RMR)`  
- Get list of zones that the HVAC system serves (should only be one): `zone_list_b = hvac_zone_list_w_area_dict_b[hvac_b.id]["ZONE_LIST"]`  
- Create an object for the zone associated with the HVAC system (should only be one since this function is for single zone systems only): `zone_b = zone_list_b[0]`
- Check that there is only one terminal unit associated with the zone: `if len(zone_b.terminals) == 1:`  
    - Get and store the terminal unit object: `terminal_obj = zone_b.terminals[0]`    
- Else, terminal_obj_ equals Null: `Else: terminal_obj = Null`  

**Returns** `return terminal_obj`  

**[Back](../_toc.md)**