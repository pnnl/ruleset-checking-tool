## get_zones_health_safety_vent_reqs

**Description:** Get the list of zones that are likely to have health and safety mandated minimum ventilation requirements during unoccupied hours.  

**Inputs:**
- **P-RMR**: To determine if any of the zones have spaces with lighting spaces types that are likely to have health and safety mandated minimum ventilation requirements during unoccupied hours.

**Returns:**
- **applicable_zones_health_safety_vent_list_p**: A list that saves all zones that are likely to have health and safety mandated minimum ventilation requirements during unoccupied hours.
 
**Function Call:** None


**Logic:**
- For each zone in P_RMR: `for zone_p in P_RMR...Zones:`
    - Reset applicability flag: `health_safety_reqs_unocc_check = FALSE` 
    - For each space in zone: `for space_p in zone_p.spaces:`
        - Check if space is of type that is likely to have health and safety mandated minimum ventilation requirements during unoccupied hours, if yes then set applicability flag to true based on lighting_space_type: `if space_p.lighting_space_type in ["MANUFACTURING_FACILITY_DETAILED_MANUFACTURING_AREA", "MANUFACTURING_FACILITY_EQUIPMENTROOM", "HEALTHCARE_FACILITY_EXAM_TREATMENT_ROOM", "HEALTHCARE_FACILITY_MEDICAL_SUPPLY_ROOM", "HEALTHCARE_FACILITY_NURSERY", "HEALTHCARE_FACILITY_OPERATING_ROOM", "HEALTHCARE_FACILITY_PATIENT_ROOM", "HEALTHCARE_FACILITY_RECOVERY_ROOM", "MUSEUM_RESTORATION_ROOM","PHARMACY_AREA","EMERGENCY_VEHICLE_GARAGE", "CONFINEMENT_CELLS"]:`
            - Set applicability flag: `health_safety_reqs_unocc_check = TRUE`
        - Check if space is of type that is likely to have health and safety mandated minimum ventilation requirements during unoccupied hours, if yes then set applicability flag to true based on ventilations_space_type: `if space_p.ventilations_space_type in ["OUTPATIENT_HEALTH_CARE_FACILITIES_CLASS_1_IMAGING_ROOMS", "ANIMAL_FACILITIES_ANIMAL_IMAGING_MRI_CT_PET"]:`
            - Set applicability flag: `health_safety_reqs_unocc_check = TRUE`
    - Check if the applicability flag equals TRUE, if true then add to list of zones: `if health_safety_reqs_unocc_check == TRUE:`
        - Add to list of applicable zones: `applicable_zones_health_safety_vent_list_p = applicable_zones_health_safety_vent_list_p.append(zone_p.id)`

**Returns** `return applicable_zones_health_safety_vent_list_p`

**[Back](../_toc.md)**