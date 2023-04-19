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
- set a boolean has_heating_system to false: `has_heating_system = FALSE`
- set a boolean has_cooling_system to false: `has_cooling_system = FALSE`
- set result to FALSE: `result = FALSE`
- get the hvac systems serving the zone by using the get_list_hvac_systems_associated_with_zone function: `list_hvac_systems = get_list_hvac_systems_associated_with_zone(RMD,zone)`
	- loop through each HeatingVentilatingAirconditionsSystem system: `for system in list_hvac_systems:`
		- check for a heating system: `if system.heating_system != NULL or system.heating_system.type != NONE:NE:`
			- set the boolean has_heating_system to true: `has_heating_system = TRUE`
		- look for a cooling system: `if system.cooling_system != NULL or system.cooling_system != NONE:`
			- there is a cooling system: `has_cooling_system = TRUE`
- at this point, if there is no cooling system, continue looking in the zone terminals for a cooling system (if there is a cooling system at this level, the function should return false regardless of what is in the zone terminals, and we can skip to the end): `if !has_cooling_system:`
	- look at each terminal in the zone: `for terminal in zone.terminals:`
		- check if there is a terminal.heating_source specified: `if terminal.heating_source != NULL or terminal.heating_source != NONE:`
			- there is a terminal heat source, set has_heating_system equal to true: `has_heating_system = TRUE`
		- check if there is a terminal.cooling_source specified: `if terminal.cooling_source != NULL or terminal.cooling_source != NONE:`
			- there is a terminal cooling source, set has_cooling_system equal to true: `has_cooling_system = TRUE`
- now, if has_heating_system is true and has_cooling_system is false, set result equal to true: `if has_heating_system and !has_cooling_system: result = TRUE`

**Returns** `result`


**Notes/Questions:**  
1.  Are there any cases where a cooling system would exist, but there is no mechanical cooling?

**[Back](../_toc.md)**
