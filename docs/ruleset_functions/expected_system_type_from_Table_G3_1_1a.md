# expected_system_type_from_Table_G3_1_1
**Schema Version:** 0.0.22  

**Description:** returns the expected system type based on the BAT, the number of floors of the building and the area of the BAT, and climate zone

**Inputs:**
- **building_area_type** - ("RESIDENTIAL", "PUBLIC_ASSEMBLY", "RETAIL", "HOSPITAL", "OTHER_NON_RESIDENTIAL", "HEATED-ONLY_STORAGE")
- **climate_zone** - schema enum, refer to ClimateZoneOptions2019ASHRAE901
- **number_of_floors** - this is the number of floors in the building (should be an integer greater than 0)
- **building_area** - this is the total area of the building

**Returns:**  
- **result**: a dict indicating the expected system type from table G3_1_1 ("SYS-1", "SYS-2", etc) and a string that indicates how the system was chosen, for example: {"EXPECTED_SYSTEM_TYPE": "SYS-4", "SYSTEM_ORIGIN": "PUBLIC_ASSEMBLY CZ_0_to_3a < 120,000 ft2"} - does not take into account G3.1.1 b-g
 
**Function Call:**
- **is_CZ_0_to_3a**

## Logic:
- create building_area_string, which will be appended to the details_of_system_selection string: `building_area_string = ""`
- create number_of_floors_string, which will be appended to the details_of_system_selection string: `number_of_floors_string = ""`

- get the climate zone category using the functions is_CZ_0_to_3a: `if is_CZ_0_to_3a(climate_zone):`
	- set climate_zone_category to CZ_0_to_3a: `climate_zone_category = " CZ_0_to_3a"`

- else (the climate zone is 3b, 3c or 4 to 8): `else:`
	- set climate_zone_category to CZ_3b_3c_or_4_to_8: `climate_zone_category = " CZ_3b_3c_or_4_to_8"`


- check if the building area type is Retail: `if building_area_type == "RETAIL":`
	- check if there are fewer than 3 floors in the building: `if number_of_floors < 3:`
		- set number_of_floors_string to " 1 or 2 floors": `number_of_floors_string = " 1 or 2 floors"`
		- check if the climate zone is CZ_0_to_3a: `if is_CZ_0_to_3a():`
			- the expected system is System 4: `expected_system_type = "SYS-4"`
		- otherwise, it's CZ_3b_3c_or_4_to_8: `else:`
			- the expected system is System 3: `expected_system_type = "SYS-3"`
	- otherwise reclasify the building area type to OTHER_NON_RESIDENTIAL: `else: building_area_type = "OTHER_NON_RESIDENTIAL"`


- check if the building area type is residential: `if building_area_type == "RESIDENTIAL":`
	- check if the climate zone is CZ_0_to_3a: `if is_CZ_0_to_3a():`
		- the expected system is System 2: `system_type = "SYS-2"`
	- otherwise, it's  CZ_3b_3c_or_4_to_8: `else:`
		- the expected system is System 1: `expected_system_type = "SYS-1"`


- check if the building area type is Public Assembly: `if building_area_type == "PUBLIC_ASSEMBLY":`
	- check if the space area is less than 120,000 ft2: `if building_area < 120000:`
		- set building_area_string to "< 120,000": `building_area_string = " < 120,000 ft2"`
		- check if the climate zone is CZ_0_to_3a: `if is_CZ_0_to_3a():`
			- the expected system is System 4: `expected_system_type = "SYS-4"`
		- otherwise, it's CZ_3b_3c_or_4_to_8: `else:`
			- the expected system is System 3: `expected_system_type = "SYS-3"`
	- otherwise, the space area is greater than 120,000 ft2: `else:`
		- set building_area_string to ">= 120,000": `building_area_string = " >= 120,000 ft2"`
		- check if the climate zone is CZ_0_to_3a: `if is_CZ_0_to_3a():`
			- the expected system is System 13: `expected_system_type = "SYS-13"`
		- otherwise, it's CZ_3b_3c_or_4_to_8: `else:`
			- the expected system is System 12: `expected_system_type = "SYS-12"`


- check if the building area type is heated-only storage: `if building_area_type == "HEATED-ONLY_STORAGE":`
	- check if the climate zone is CZ_0_to_3a: `if is_CZ_0_to_3a():`
		- the expected system is System 10: `expected_system_type = "SYS-10"`
	- otherwise, it's CZ_3b_3c_or_4_to_8: `else:`
		- the expected system is System 9: `expected_system_type = "SYS-9"`


- check if the building area type is Hospital: `if building_area_type == "HOSPITAL":`
	- Hospital BAT doesn't use the climate zone to determine system type, so set climate_zone_category to "": `climate_zone_category = ""`
	- check if the space area is more than 150,000 ft2 OR the building is more than 5 floors: `if((building_area > 150000) || (number_of_floors > 5)):`
		- set building_area_string to " > 150,000 ft2 or > 5 floors": `building_area_string = " > 150,000 ft2 or > 5 floors"`
		- the expected system is System 7: `expected_system_type = "SYS-7"`
	- otherwise: `else:`
		- set building_area_string to " All Other": `building_area_string = " All Other"`
		- the expected system is System 5: `expected_system_type = "SYS-5"`


- check if the building area type is other non-residential: `if building_area_type == "OTHER_NON_RESIDENTIAL":`
	- check if the space area is less than 25,000: `if building_area < 25000:`
		- set building_area_string to "< 25,000": `building_area_string = " < 25,000 ft2"`
		- check if the building is fewer than 4 floors: `if number_of_floors < 4:`
			- set number_of_floors_string to " 3 floors or fewer": `number_of_floors_string = " 3 floors or fewer"`
			- check if the climate zone is CZ_0_to_3a: `if is_CZ_0_to_3a():`
				- the expected system is System 4: `expected_system_type = "SYS-4"`
			- otherwise, it's CZ_3b_3c_or_4_to_8: `if else:`
				- the expected system is System 3: `expected_system_type = "SYS-3"`
		- else this is still < 25000 ft2, check if it is in a building less than 6 floors: `if number_of_floors < 6:`
			- set number_of_floors_string to " 4-5 floors": `number_of_floors_string = " 4-5 floors"`
			- check if the climate zone is CZ_0_to_3a: `if is_CZ_0_to_3a():`
				- the expected system is System 6: `expected_system_type = "SYS-6"`
			- otherwise, it's CZ_3b_3c_or_4_to_8: `else:`
				- the expected system is System 5: `expected_system_type = "SYS-5"
		- else if the space area is between 25,000 and 150,000 ft2 AND in a building that is fewer than 6 floors: `if((building_area >= 25000) && (building_area < 150000) && (number_of_floors <= 5)):`
			- set building_area_string to " >=25,000 ft2 AND <=150,000 ft2": `building_area_string = " >=25,000 ft2 AND <=150,000 ft2"`
			- set number_of_floors_string to " < 6 floors": `number_of_floors_string = " < 6 floors"`
			- check if the climate zone is CZ_0_to_3a: `if is_CZ_0_to_3a():`
				- the expected system is System 6: `expected_system_type = "SYS-6"`
			- otherwise, it's CZ_3b_3c_or_4_to_8: `else:`
				- the expected system is System 5: `expected_system_type = "SYS-5"`
		- else if the building_area is greater than 150,000 ft2 OR the building has more than 5 floors: `if((building_area > 150000) || (number_of_floors > 5)):`
			- set building_area_string to " >150,000 ft2 or > 5 floors": `building_area_string to " >150,000 ft2 or > 5 floors"`
			- check if the climate zone is CZ_0_to_3a: `if is_CZ_0_to_3a():`
				- the expected system is System 8: `expected_system_type = "SYS-8"`
			- otherwise, it's CZ_3b_3c_or_4_to_8: `else:`
				- the expected system is System 7: `expected_system_type = "SYS-7"

- create the string that holds details about how the system was selected.  This string will need to match the expected string in 18-1 to 18-16 rule tests: `details_of_system_selection = building_area_type + climate_zone_category + building_area_string + number_of_floors_string`
- set result equal to a list of the expected_system_type and details_of_system_selection: `result = [expected_system_type, details_of_system_selection]`

**Returns** `result`


**Notes/Questions:**  
1. I will check the text strings for correctness as I write each individual rule

**[Back](../_toc.md)**
