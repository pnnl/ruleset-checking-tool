# expected_system_type_from_Table_G3_1_1
**Schema Version:** 0.0.22  

**Description:** returns the expected system type based on the BAT, the number of floors of the building and the area of the BAT, and climate zone

**Inputs:**
- **building_area_type** - ("RESIDENTIAL", "PUBLIC_ASSEMBLY", "RETAIL", "HOSPITAL", "OTHER_NON_RESIDENTIAL", "HEATED-ONLY_STORAGE")
- **number_of_floors** - this is the bumber of floors in the building integer greater than 0
- **area_of_BAT** - this is the total area of the building area type, including
- **climate_zone** - this is a string - one of the options given by ClimateZoneOptions2019ASHRAE901

**Returns:**  
- **result**: a list indicating the expected system type from table G3_1_1 ("SYS-1", "SYS-2", etc) and a string that indicates how the system was chosen, for example "Buildings in CZ 0-3A with predominant HVAC BAT = public assembly, <120,000 ft2 have baseline HVAC system type 4 (PSZ HP)" - does not take into account G3.1.1 b-g
 
**Function Call:**
- **is_CZ_0_to_3a**
- **is_CZ_3b_3c_and_4_to_8**

## Logic:
- create area_of_BAT_string, which will be appended to the details_of_system_selection string: `area_of_BAT_string = ""`
- create number_of_floors_string, which will be appended to the details_of_system_selection string: `number_of_floors_string = ""`

- get the climate zone category using the functions is_CZ_0_to_3a and is_CZ_3b_3c_and_4_to_8: `if is_CZ_0_to_3a(climate_zone):`
	- set climate_zone_category to CZ_0_to_3a: `climate_zone_category = "CZ_0_to_3a"

- else if the climate zone is 3b, 3c or 4 to 8: `if is_CZ_3b_3c_and_4_to_8(climate_zone):`
	- set climate_zone_category to CZ_3b_3c_or_4_to_8: `climate_zone_category = "CZ_3b_3c_or_4_to_8"

- check if the building area type is residential: `if building_area_type == "RESIDENTIAL":`
	- check if the climate zone is CZ_0_to_3a: `if climate_zone_category == "CZ_0_to_3a":`
		- the expected system is System 1: `system_type = "SYS-1"`
	- otherwise, for CZ_3b_3c_or_4_to_8: `if climate_zone_category == "CZ_3b_3c_or_4_to_8":`
		- the expected system is System 2: `system_type = "SYS-2"


- check if the building area type is Public Assembly: `if building_area_type == "PUBLIC_ASSEMBLY":`
	- check if the space area is less than 120,000 ft2: `if area_of_BAT < 120000:`
		- set area_of_BAT_string to "< 120,000": `area_of_BAT_string = " < 120,000 ft2"`
		- check if the climate zone is CZ_0_to_3a: `if climate_zone_category == "CZ_0_to_3a":`
			- the expected system is System 3: `system_type = "SYS-3"`
		- otherwise, for CZ_3b_3c_or_4_to_8: `if climate_zone_category == "CZ_3b_3c_or_4_to_8":`
			- the expected system is System 4: `system_type = "SYS-4"
	- otherwise, the space area is greater than 120,000 ft2: `else:`
		- set area_of_BAT_string to ">= 120,000": `area_of_BAT_string = " >= 120,000 ft2"`
		- check if the climate zone is CZ_0_to_3a: `if climate_zone_category == "CZ_0_to_3a":`
			- the expected system is System 12: `system_type = "SYS-12"`
		- otherwise, for CZ_3b_3c_or_4_to_8: `if climate_zone_category == "CZ_3b_3c_or_4_to_8":`
			- the expected system is System 13: `system_type = "SYS-13"


- check if the building area type is heated-only storage: `if building_area_type == "HEATED-ONLY_STORAGE":`
	- check if the climate zone is CZ_0_to_3a: `if climate_zone_category == "CZ_0_to_3a":`
		- the expected system is System 9: `system_type = "SYS-9"`
	- otherwise, for CZ_3b_3c_or_4_to_8: `if climate_zone_category == "CZ_3b_3c_or_4_to_8":`
		- the expected system is System 10: `system_type = "SYS-10"


- check if the building area type is Retail: `if building_area_type == "RETAIL":`
	- check if there are fewer than 3 floors in the building: `if number_of_floors < 3:`
		- check if the climate zone is CZ_0_to_3a: `if climate_zone_category == "CZ_0_to_3a":`
			- the expected system is System 3: `system_type = "SYS-3"`
		- otherwise, for CZ_3b_3c_or_4_to_8: `if climate_zone_category == "CZ_3b_3c_or_4_to_8":`
			- the expected system is System 4: `system_type = "SYS-4"
- otherwise, WHAT HAPPENS WHEN RETAIL IS IN A BUILDING THAT IS MORE THAN 2 FLOORS?  FOR NOW, I'LL RECLASSIFY AS OTHER_NON_RESIDENTIAL: `else:`
	- check if the space area is less than 120,000 ft2: `building_area_type = "OTHER_NON_RESIDENTIAL"


- check if the building area type is Hospital: `if building_area_type == "HOSPITAL":`
	- check if the space area is more than 150,000 ft2 OR the building is more than 5 floors: `if((area_of_BAT > 150000) || (number_of_floors > 5)):`
		- set area_of_BAT_string to "> 150,000 ft2 or > 5 floors": `area_of_BAT_string = " > 150,000 ft2 or > 5 floors"`
		- the expected system is System 7: `system_type = "SYS-7"`
- otherwise: `else:`
	- set area_of_BAT_string to "<= 150,000 ft2 or <=5 floors": `area_of_BAT_string = " <= 150,000 ft2 or <=5 floors"`
	- the expected system is System 5: `system_type = "SYS-5"`


- check if the building area type is other non-residential: `if building_area_type == "OTHER_NON_RESIDENTIAL":`
	- check if the space area is less than 25,000: `if area_of_BAT < 25000:`
		- set area_of_BAT_string to "< 25,000": `area_of_BAT_string = " < 25,000 ft2"`
		- check if the building is fewer than 4 floors: `if number_of_floors < 4:
			- set number_of_floors_string to " 3 floors or fewer": `number_of_floors_string = " 3 floors or fewer"`
			- check if the climate zone is CZ_0_to_3a: `if climate_zone_category == "CZ_0_to_3a":`
				- the expected system is System 3: `system_type = "SYS-3"`
			- otherwise, for CZ_3b_3c_or_4_to_8: `if climate_zone_category == "CZ_3b_3c_or_4_to_8":`
				- the expected system is System 4: `system_type = "SYS-4"
		- else this is still < 25000 ft2, check if it is in a building less than 6 floors: `if number_of_floors < 6:`
			- set number_of_floors_string to " 4-5 floors": `number_of_floors_string = " 4-5 floors"`
			- check if the climate zone is CZ_0_to_3a: `if climate_zone_category == "CZ_0_to_3a":`
				- the expected system is System 5: `system_type = "SYS-5"`
			- otherwise, for CZ_3b_3c_or_4_to_8: `if climate_zone_category == "CZ_3b_3c_or_4_to_8":`
				- the expected system is System 6: `system_type = "SYS-6"
	- else if the space area is between 25,000 and 150,000 ft2 AND in a building that is fewer than 6 floors: `if((area_of_BAT >= 25000) && (area_of_BAT < 150000) &&& (number_of_floors < 6)):`
		- set area_of_BAT_string to " >=25,000 ft2 AND <=150,000 ft2": `area_of_BAT_string = " >=25,000 ft2 AND <=150,000 ft2"`
		- check if the climate zone is CZ_0_to_3a: `if climate_zone_category == "CZ_0_to_3a":`
			- the expected system is System 5: `system_type = "SYS-5"`
		- otherwise, for CZ_3b_3c_or_4_to_8: `if climate_zone_category == "CZ_3b_3c_or_4_to_8":`
			- the expected system is System 6: `system_type = "SYS-6"
	- else if the area_of_BAT is greater than 150,000 ft2 OR the building has more than 5 floors: `if((area_of_BAT > 150000) || (number_of_floors > 5)):`
		- set area_of_BAT_string to " >150,000 ft2 or > 5 floors": `area_of_BAT_string to " >150,000 ft2 or > 5 floors"`
		- set number_of_floors_string to "" - this is because the area_of_BAT_string contains floor information, and we because we re-assigned "RETAIL" to "OTHER_NON_RESIDENTIAL" above, we need to overwriate any data currently in the number_of_floors_string: `number_of_floors_string = ""`
		- check if the climate zone is CZ_0_to_3a: `if climate_zone_category == "CZ_0_to_3a":`
			- the expected system is System 7: `system_type = "SYS-7"`
		- otherwise, for CZ_3b_3c_or_4_to_8: `if climate_zone_category == "CZ_3b_3c_or_4_to_8":`
			- the expected system is System 8: `system_type = "SYS-8"

- create the string that holds details about how the system was selected.  This string will need to match the expected string in 18-1 to 18-16 rule tests: `details_of_system_selection = climate_zone_category + area_of_BAT_string + number_of_floors_string`
- set result equal to a list of the system_type and details_of_system_selection: `result = [system_type, details_of_system_selection]`

**Returns** `result`


**Notes/Questions:**  
1. WHAT HAPPENS WHEN RETAIL IS IN A BUILDING THAT IS MORE THAN 2 FLOORS?  Seems like there is a hole in Table G3.1.1
2. I will check the text strings for correctness as I write each individual rule

**[Back](../_toc.md)**
