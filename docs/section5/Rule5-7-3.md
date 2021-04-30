# Envelope - Rule 5-7-3  
**Rule ID:** 5-7-3  
**Rule Description:** Baseline RMR fenestration area prior to proposed work cannot be verified.  
**Rule Assertion:** Cannot be verified  
**Appendix G Section:** Envelope  
**Appendix G Section Reference:**
- Table G3.1, 5. Building Envelope, Baseline Building Performance, c. Vertical Fenestration Areas

**Data Lookup:** None
**Evaluation Context:**  Each Data Element  

**Applicability Checks:** 
1. Building has spaces that are EXISTING.

**Manual Checks:** None  

## Rule Logic:
- **Applicability Check 1:** `length( [ if _space.status_type for _space in U_RMR...spaces is in [EXISTING ] ) > 0:`  
- For each building segment in the Baseline model: `For building_segment in B_RMR.building.building_segments:`
    - Get the building area type of the building segment: `_building_area_type = building_segment.area_type_vertical_fenestration`
    - Get thermal_block from building segment: `_thermal_block in building_segment.thermal_blocks:`
    - Get thermal_zone from thermal block: `_thermal_zone in _thermal_block.thermal_zones:`
    - Get space from thermal zone: `_space in _thermal_zone.spaces:`
    - Check if space is EXISTING: `if _space.status_type == EXISTING:`
    - **Rule Assertion** `CANNOT_BE_VERIFIED`

**[Back](../_toc.md)**