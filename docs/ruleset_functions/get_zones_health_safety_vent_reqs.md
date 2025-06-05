# get_zones_health_safety_vent_reqs  

**Schema Version:** 0.0.23
**Description:** Get the list of zones that are likely to have health and safety mandated minimum ventilation requirements during unoccupied hours.  

**Inputs:**  
- **P-RMR**: To determine if any of the zones have spaces with lighting spaces types that are likely to have health and safety mandated minimum ventilation requirements during unoccupied hours.  

**Returns:**  
- **zones_health_safety_vent_list_p**: A list that saves all zones that are likely to have health and safety mandated minimum ventilation requirements during unoccupied hours.  
 
**Function Call:** None  

## Logic:  
- For each zone in P_RMR: `for zone_p in P_RMR..Zone:`
    - Reset zone is likely to have health and safety reqs during unocc hours boolean variable: `zone_has_health_safety_reqs_unocc_check = FALSE` 
    - For each space in zone: `for space_p in zone_p.spaces:`
        - Check if space is of type that is likely to have health and safety mandated minimum ventilation requirements during unoccupied hours, if yes then set zone is likely to have health and safety reqs during unocc hours boolean variable to true based on lighting_space_type: `if space_p.lighting_space_type in ["MANUFACTURING_FACILITY_DETAILED_MANUFACTURING_AREA", "MANUFACTURING_FACILITY_EQUIPMENTROOM", "HEALTHCARE_FACILITY_EXAM_TREATMENT_ROOM", "HEALTHCARE_FACILITY_MEDICAL_SUPPLY_ROOM", "HEALTHCARE_FACILITY_NURSERY", "HEALTHCARE_FACILITY_OPERATING_ROOM", "HEALTHCARE_FACILITY_PATIENT_ROOM", "HEALTHCARE_FACILITY_RECOVERY_ROOM", "MUSEUM_RESTORATION_ROOM","PHARMACY_AREA","EMERGENCY_VEHICLE_GARAGE", "CONFINEMENT_CELLS"]:`
            - Set zone is likely to have health and safety reqs during unocc hours boolean variable to true: `zone_has_health_safety_reqs_unocc_check = TRUE`
        - Check if space is of type that is likely to have health and safety mandated minimum ventilation requirements during unoccupied hours, if yes then set zone is likely to have health and safety reqs during unocc hours boolean variable to true based on ventilation_space_type: `if space_p.ventilation_space_type in ["OUTPATIENT_HEALTH_CARE_FACILITIES_CLASS_1_IMAGING_ROOMS", "ANIMAL_FACILITIES_ANIMAL_IMAGING_MRI_CT_PET"]:`
            - Set zone is likely to have health and safety reqs during unocc hours boolean variable: `zone_has_health_safety_reqs_unocc_check = TRUE`
    - Check if the zone is likely to have health and safety reqs during unocc hours boolean variable equals TRUE, if true then add to list of zones: `if zone_has_health_safety_reqs_unocc_check == TRUE:`
        - Add to list of zones: `zones_health_safety_vent_list_p = zones_health_safety_vent_list_p.append(zone_p.id)`  

**Returns** `return zones_health_safety_vent_list_p`

**[Back](../_toc.md)**