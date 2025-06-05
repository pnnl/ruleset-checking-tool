# is_CZ_0_to_3a
**Schema Version:** 0.0.22  

**Description:** Determines whether the building is in climate zone 0 to 3a - used for Appendix G Table G3.1.1-3

**Inputs:**
- **climate_zone:** `ClimateZoneOptions2019ASHRAE901`  # or is it: ASHRAE229.weather.climate_zone?

**Returns:**  
- **result**: a boolean TRUE or FALSE
 
**Function Call:**

## Logic:
1. Check if the climate zone is CZ0-3A: `result = climate_zone in ["CZ0A","CZ0B","CZ1A","CZ1B","CZ2A","CZ2B","CZ3A"]`


**Returns** `result`


**Notes/Questions:**  

**[Back](../_toc.md)**
