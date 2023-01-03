# is_zone_mechanically_heated_and_not_cooled
**Schema Version:** 0.0.23  

**Description:** determines whether a zone is mechanically heated, but not cooled.  DOES NOT CHECK FOR TRANSFER AIR

**Inputs:**
- **RMD**
- **zone**

**Returns:**  
- **result**: a boolean - TRUE or FALSE
 
**Function Call:**
- **get_list_hvac_systems_associated_with_zone**

## Logic:
- set result to FALSE: `result = FALSE`
- get the hvac systems serving the zone by using the get_list_hvac_systems_associated_with_zone function: `list_hvac_systems = get_list_hvac_systems_associated_with_zone(RMD,zone)`
	- loop through each HeatingVentilatingAirconditionsSystem system: `for system in list_hvac_systems:`
		- check for a heating system: `if system.heating_system != "Null":`
			- make sure the heating system type is not equal to None: `if system.heating_system.heating_system_type != NONE:`
				- look for a cooling system: `if system.cooling_system == "Null":`
					- there is no cooling system, set result to TRUE: `result = TRUE`
				- otherwise: `else:`
					- check to see if the cooling_system_options equals "None": `if system.cooling_system.cooling_system_options == NONE:`
						- there is a cooling system in the zone: `result = TRUE`

**Returns** `result`


**Notes/Questions:**  
1.  Are there any cases where a cooling system would exist, but there is no mechanical cooling?

**[Back](../_toc.md)**
