# is_zone_mechanically_cooled
**Schema Version:** 0.0.25  

**Description:** determines whether a zone is cooled.  Checks for transfer air

**Inputs:**
- **RMI**
- **zone**

**Returns:**  
- **has_cooling_system**: a boolean - TRUE or FALSE
 
**Function Call:**
- **get_list_hvac_systems_associated_with_zone**

## Logic:
- set a boolean has_cooling_system to false: `has_cooling_system = FALSE`
- get the hvac systems serving the zone by using the get_list_hvac_systems_associated_with_zone function: `list_hvac_systems = get_list_hvac_systems_associated_with_zone(RMI,zone)`
	- loop through each HeatingVentilatingAirconditionsSystem system: `for system in list_hvac_systems:`
		- look for a cooling system: `if system.cooling_system != NULL or system.cooling_system != NONE:`
			- there is a cooling system: `has_cooling_system = TRUE`
- at this point, if there is no cooling system, continue looking in the zone terminals for a cooling system (if there is a cooling system at this level, the function should return false regardless of what is in the zone terminals, and we can skip to the end): `if !has_cooling_system:`
	- look at each terminal in the zone: `for terminal in zone.terminals:`
		- check if there is a terminal.cooling_source specified: `if terminal.cooling_source != NULL or terminal.cooling_source != NONE:`
			- there is a terminal cooling source, set has_cooling_system equal to true: `has_cooling_system = TRUE`
- if has_cooling_system is FALSE, check if the zone receives transfer air from a cooled zone: `if !has_cooling_system:`

	- if the zone has transfer air: `if zone.transfer_airflow_rate > 0:`
		- create variable for the transfer source zone: `transfer_source_zone = zone.transfer_airflow_source_zone`
		- get the hvac systems serving the transfer_source_zone by using the get_list_hvac_systems_associated_with_zone function: `list_hvac_systems_for_transfer_source_zone = get_list_hvac_systems_associated_with_zone(RMI,transfer_source_zone)`
		- loop through each HeatingVentilatingAirconditionsSystem system: `for transfer_source_system in list_hvac_systems_for_transfer_source_zone:`
			- look for a cooling system: `if transfer_source_system.cooling_system != NULL or transfer_source_system.cooling_system != NONE:`
				- there is a cooling system: `has_cooling_system = TRUE`
		- at this point, if there is no cooling system, continue looking in the zone terminals for a cooling system (if there is a cooling system at this level, the function should return false regardless of what is in the zone terminals, and we can skip to the end): `if !has_cooling_system:`
		- look at each terminal in the zone: `for transfer_source_terminal in transfer_source_zone.terminals:`
			- check if there is a transfer_source_terminal.cooling_source specified: `if transfer_source_terminal.cooling_source != NULL or transfer_source_terminal.cooling_source != NONE:`
				- there is a terminal cooling source, set has_cooling_system equal to true: `has_cooling_system = TRUE`

**Returns** `has_cooling_system`


**Notes/Questions:**  
1.  Are there any cases where a cooling system would exist, but there is no mechanical cooling?

**[Back](../_toc.md)**
