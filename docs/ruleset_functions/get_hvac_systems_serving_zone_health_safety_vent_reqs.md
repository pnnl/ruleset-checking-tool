# get_hvac_systems_serving_zone_health_safety_vent_reqs  

**Schema Version:** 0.0.23
**Description:** Get the list of HVAC systems that are likely to serve zones that have health and safety mandated minimum ventilation requirements during unoccupied hours.  

**Inputs:**  
- **U, P, or B-RMI**: To determine if any of the zones have spaces with lighting spaces types that are likely to have health and safety mandated minimum ventilation requirements during unoccupied hours and to create a list of the hvac systems associated with these zones.  

**Returns:**  
- **hvac_systems_unocc_health_safety_vent_list_x**: A list that saves all hvac systems that are likely to serve zones that have health and safety mandated minimum ventilation requirements during unoccupied hours.  
 
**Function Call:**  
1. get_list_hvac_systems_associated_with_zone()  

## Logic:  
- Create an object from the RMI input to the function (RMI = function input RMI): `X_RMI = RMI`
- For each zone in X_RMI: `for zone_x in X_RMI..Zone:`
    - Reset zone is likely to have health and safety reqs during unocc hours boolean variable: `zone_has_health_safety_reqs_unocc_check = FALSE` 
    - For each space in zone: `for space_x in zone_x.spaces:`
        - Check if space is of type that is likely to have health and safety mandated minimum ventilation requirements during unoccupied hours, if yes then set zone is likely to have health and safety reqs during unocc hours boolean variable to true based on lighting_space_type: `if space_x.lighting_space_type in ["MANUFACTURING_FACILITY_DETAILED_MANUFACTURING_AREA", "MANUFACTURING_FACILITY_EQUIPMENTROOM", "HEALTHCARE_FACILITY_EXAM_TREATMENT_ROOM", "HEALTHCARE_FACILITY_MEDICAL_SUPPLY_ROOM", "HEALTHCARE_FACILITY_NURSERY", "HEALTHCARE_FACILITY_OPERATING_ROOM", "HEALTHCARE_FACILITY_PATIENT_ROOM", "HEALTHCARE_FACILITY_RECOVERY_ROOM", "MUSEUM_RESTORATION_ROOM","PHARMACY_AREA","EMERGENCY_VEHICLE_GARAGE", "CONFINEMENT_CELLS"]:`
            - Set zone is likely to have health and safety reqs during unocc hours boolean variable to true: `zone_has_health_safety_reqs_unocc_check = TRUE`
        - Check if space is of type that is likely to have health and safety mandated minimum ventilation requirements during unoccupied hours, if yes then set zone is likely to have health and safety reqs during unocc hours boolean variable to true based on ventilation_space_type: `if space_x.ventilation_space_type in ["OUTPATIENT_HEALTH_CARE_FACILITIES_CLASS_1_IMAGING_ROOMS", "ANIMAL_FACILITIES_ANIMAL_IMAGING_MRI_CT_PET"]:`
            - Set zone is likely to have health and safety reqs during unocc hours boolean variable: `zone_has_health_safety_reqs_unocc_check = TRUE`
    - Check if the zone is likely to have health and safety reqs during unocc hours boolean variable equals TRUE, if true then get list of hvac systems associated with the zone: `if zone_has_health_safety_reqs_unocc_check == TRUE:`
        - Get a list of hvac systems associated with the zone and add to master list: `hvac_systems_unocc_health_safety_vent_list_x = hvac_systems_unocc_health_safety_vent_list_x.append(get_list_hvac_systems_associated_with_zone(X_RMI,zone_x.id))`  
        
- Remove duplicates by creating a set from list and then turning it back into a list: `hvac_systems_unocc_health_safety_vent_list_x = list(set(hvac_systems_unocc_health_safety_vent_list_x))`

**Returns** `hvac_systems_unocc_health_safety_vent_list_x`

**[Back](../_toc.md)**