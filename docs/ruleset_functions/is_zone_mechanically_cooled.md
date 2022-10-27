# is_zone_mechanically_cooled
**Schema Version:** 0.0.22  

**Description:** determines whether a zone is mechanically cooled or not.  DOES NOT CHECK FOR TRANSFER AIR

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
	- loop through each heating system: `for system in list_hvac_systems:`
		- look for a cooling system: `if system.cooling_system != "Null":`
			- check to see if the cooling_system_options equals "None": `if system.cooling_system.cooling_system_options != "None":`
				- there is a cooling system in the zone: `result = TRUE`

**Returns** `result`


**Notes/Questions:**  
1.  Are there any cases where a cooling system would exist, but there is no mechanical cooling?

**[Back](../_toc.md)**
