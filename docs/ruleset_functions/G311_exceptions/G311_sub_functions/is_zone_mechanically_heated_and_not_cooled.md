# is_zone_mechanically_heated_and_not_cooled
**Schema Version:** 0.0.23  

**Description:** determines whether a zone is mechanically heated, but not cooled.  Checks for transfer air

**Inputs:**
- **RMI**
- **zone**

**Returns:**  
- **result**: a boolean - TRUE or FALSE
 
**Function Call:**
- **get_list_hvac_systems_associated_with_zone**

## Logic:
- set a boolean is_heated to false: `is_heated = FALSE`
- set a boolean is_cooled to false: `is_cooled = FALSE`
- get the hvac systems serving the zone by using the get_list_hvac_systems_associated_with_zone function: `list_hvac_systems = get_list_hvac_systems_associated_with_zone(RMI,zone)`
	- loop through each HeatingVentilatingAirconditionsSystem system: `for system in list_hvac_systems:`
		- check for a heating system: `if system.heating_system != NULL:`
			- `if system.heating_system.type != NONE:`
				- set the boolean is_heated to true: `is_heated = TRUE`
		- look for a cooling system: `if system.cooling_system != NULL:`
			- `if system.cooling_system != NONE:`
				- there is a cooling system: `is_cooled = TRUE`
- at this point, if there is no cooling system, continue looking in the zone terminals for a cooling system (if there is a cooling system at this level, the function should return false regardless of what is in the zone terminals, and we can skip to the end): `if !is_cooled:`
	- look at each terminal in the zone: `for terminal in zone.terminals:`
		- check if there is a terminal.heating_source specified: `if terminal.heating_source != NULL:`
			- `if terminal.heating_source != NONE:`
				- there is a terminal heat source, set is_heated equal to true: `is_heated = TRUE`
		- check if there is a terminal.cooling_source specified: `if terminal.cooling_source != NULL:`
			-  `if terminal.cooling_source != NONE:`
				- there is a terminal cooling source, set is_cooled equal to true: `is_cooled = TRUE`
- if the zone is heated, but not cooled, check if the zone receives transfer air from a cooled zone: `if is_heated && !is_cooled:`
	- if the zone has transfer air: `if zone.transfer_airflow_rate > 0:`
		- set transfer_source_zone equal to the zone.transfer_airflow_source_zone: `transfer_source_zone = zone.transfer_airflow_source_zone`
		- get the hvac systems serving the transfer airflow source zone: `transfer_source_zone_list_hvac_systems = get_list_hvac_systems_associated_with_zone(RMI,transfer_source_zone)`
		- loop through heach HVAC system: `for transfer_system in transfer_source_zone_list_hvac_systems:`
			- look for a cooling system: `if transfer_system.cooling_system != NULL:`
				- `if transfer_system.cooling_system.type != NONE:`
					- there is a cooling system: `is_cooled = TRUE`
		- if there is no cooling system, look through the zone terminals of the transfer_source_zone for a cooling system: `if !is_cooled:`
			- look at each terminal in the transfer_source_zone: `for transfer_terminal in transfer_source_zone.terminals:`
				- check if there is a transfer_terminal.cooling_source specified: `if transfer_terminal.cooling_source != NULL:`
					-  `if transfer_terminal.cooling_source.type != NONE:`
						- there is a terminal cooling source, set is_cooled equal to true: `is_cooled = TRUE`


- set result equal to is_heated and !is_cooled: `result = is_heated and !is_cooled`

**Returns** `result`


**Notes/Questions:**  
1.  Are there any cases where a cooling system would exist, but there is no mechanical cooling?

**[Back](../_toc.md)**
