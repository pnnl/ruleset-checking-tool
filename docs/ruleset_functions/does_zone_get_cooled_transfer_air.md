# does_zone_gets_cooled_transfer_air
**Schema Version:** 0.0.23

**Description:** determines whether a zone receives cooled transfer air.  It is based on a variable that has not yet been implemented in the schema (version 0.0.22)

**Inputs:**
- **RMI**
- **zone_id**

**Returns:**  
- **result**: boolean
 
**Function Call:**
- **is_zone_mechanically_heated_and_not_cooled**
- **get_component_by_id**
- **get_list_hvac_systems_associated_with_zone**

## Logic:
- set result to FALSE: `result = FALSE`
- get the zone object: `zone = get_component_by_id(RMI,zone_id)`
- look for transfer air into the space: `if zone.transfer_airflow_rate > 0:`
    - set result to TRUE, we are assuming that the transfer airflow is air conditioned until proven otherwise: `result = TRUE` 
    - Find the transfer air source zone to determine if this zone has air conditioning: `transfer_air_source_zone_id = zone.transfer_airflow_source_zone`
    - get the transfer source zone: `transfer_source_zone = get_component_by_id(RMI,transfer_air_source_zone_id)`
    - get the hvac systems serving the zone by using the get_list_hvac_systems_associated_with_zone function: `list_hvac_systems = get_list_hvac_systems_associated_with_zone(RMI,transfer_source_zone)`
  	- loop through each HeatingVentilatingAirconditionsSystem system: `for system in list_hvac_systems:`
		  	- look for a cooling system: `if system.cooling_system == "Null":`
			  	- there is no cooling system, set result to TRUE: `result = FALSE`
			  - otherwise: `else:`
				  - check to see if the cooling_system_options equals "None": `if system.cooling_system.cooling_system_options == "None":`
					  - there is a cooling system in the zone: `result = FALSE`


**Returns** `result`


**Notes/Questions:**  

**[Back](../_toc.md)**
