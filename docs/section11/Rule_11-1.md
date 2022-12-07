# Service_Water_Heating - Rule 11-1
**Schema Version:** 0.0.23  

**Mandatory Rule:** TRUE

**Rule ID:** 11-1

**Rule Description:** "Where a complete service water-heating system exists, the proposed design shall reflect the actual system type. Where a service water-heating system has been designed the service waterheating type shall be consistent with design documents."

**Rule Assertion:** Options are PASS/FAIL

**Appendix G Section Reference:** Table G3.1 #11, proposed column, a & b

**Evaluation Context:** P-RMI
**Data Lookup:**   
**Function Call:** 
- **compare_objects**
- **get_component_by_id**
- **compare_same_field_in_different_objects**
- **compare_iterative_objects**

**Applicability Checks:**
- no logic here, applies to all P-RMDs

## Setup:
- create a list of relevant fields for each of the object types that we are checking
- ServiceWaterHeatingDistributionSystem fields to compare: `service_weater_heating_distribution_system_field_list = [
    design_supply_temperature,
    design_supply_temperature_difference,
    is_central_system,
    distribution_compactness,
    control_type,
    configuration_type,
    is_recovered_heat_from_drain_used_by_water_heater,
    drain_heat_recovery_efficiency,
    drain_heat_recovery_type,
    is_ground_temperature_used_for_entering_water
]

- ServiceWaterHeatingDistributionSystem schedules to compare: `service_weater_heating_distribution_system_schedules_field_list = [
    flow_multiplier_schedule,
    entering_water_mains_temperature_schedule
]
    
- Tank: `tank_field_list = [
    storage_capacity,
    type,
    height,
    interior_insulation,
    exterior_insulation,
    location,
    location_zone.id
]
- tanks, flow_multiplier_schedule, entering_water_mains_temperature_schedule

## Rule Logic: 
- we need to check that the service water heating systems in the P-RMD and U-RMD match.  For each item, if there is a list of objects, we will first check that there are the same number of elements, then we will check that the elements match.
- first create a boolean `all_match` and set to TRUE: `all_match = TRUE` 
- create a list of the tanks in the project: `tank_list = []`
- create a list of ServiceWaterPiping in the project: `service_water_piping_list = []`
- check if there are the same number of Service Water Heating Distribution Systems: `if len(P_RMI.service_water_heating_distribution_systems) == len(U_RMI.service_water_heating_distribution_systems):`
  - loop through the Service Water Heating Distribution Systems and check whether they are the same: `for service_water_heating_distribution_system_p in P_RMI.service_water_heating_distribution_systems:`
    - use the compare_objects function to compare the service water heating systems in P_RMI and U_RMI: `if compare_objects(P_RMI,U_RMI,service_water_heating_distribution_system_p.id,service_weater_heating_distribution_system_schedules_field_list,service_weater_heating_distribution_system_schedules_field_list):`
      - get the equivalent user service_water_heating_distribution_system: `service_water_heating_distribution_system_u = get_component_by_id(U_RMI, service_water_heating_distribution_system_p.id)`
      - compare the tanks field using the function compare_same_field_in_different_objects.  A SAME result tells us that both fields are not NULL and that they have the same contents.  Because this field is a list field, we know that both objects contain lists of the same length: `if compare_same_field_in_different_objects(service_water_heating_distribution_system_p, service_water_heating_distribution_system_u, tanks) == SAME:`
        - create a list of tank ids for service_water_heating_distribution_system_u: `tank_u_ids = []; for tank_u in service_water_heating_distribution_system_u.tanks: tank_u_ids.append(tank_u.id)`
        - iterate through each tank in service_water_heating_distribution_system_p: `for tank_p in service_water_heating_distribution_system_p.tanks:`
          - check whether the tank_p.id is in the list of tanks for service_water_heating_distribution_system_u: `if tank_p.id in tank_u_ids:`
            - compare the two tanks using compare_objects: `if not compare_objects(P_RMI,U_RMI,tank_p.id,tank_field_list,[]):`
              - set all_match to false, break out of the loop: `all_match = FALSE; break`
          - else the tank is not attached to the system in the user_model: `else:`
            - set all_match to false, break out of the loop: `all_match = FALSE; break`
      - compare the service_water_piping field using the function compare_same_field_in_different_objects.  A SAME result tells us that both fields are lists of the same length: `if compare_same_field_in_different_objects(service_water_heating_distribution_system_p, service_water_heating_distribution_system_u, service_water_piping) == SAME:`
        - create a list of service water piping ids for service_water_heating_distribution_system_u: `service_water_piping_ids = []: for swp_u in service_water_heating_distribution_system_u.service_water_piping: service_water_piping_ids.append(swp_u.id)`
        - iterate through each service_water_piping in service_water_heating_distribution_system_p: `for swp_p in service_water_heating_distribution_system_p.service_water_piping:`
          - check whether the swp_p.id is in the list of swp's for service_water_heating_distribution_system_u: `if swp_p.id in service_water_piping_ids:`
            - compare the two piping systems using compare_iterative_objects: `if not compare_iterative_objects(P_RMI,U_RMI,spw_p.id,service_water_piping_field_list,[],child_service_water_piping):`
              - set all_match to false, break out of the loop: `all_match = FALSE; break`
          - else the service water piping system is not attached to the system in the user_model: `else:`
            - set all_match to false, break out of the loop: `all_match = FALSE; break`
    - otherwise, the systems are not the same, set all_match to FALSE and break out of the loop: `else: all_match = FALSE; break;`

TODO: 
  ServiceWaterHeatingEquipment
  Pump





  **Rule Assertion:**
  
  **Notes:**
  1.  This logic assumes that equal elements in the P-RMD and U-RMD have the same id.
  2.  Is there an automatic way to get all the fields associated with an object instead of listing them?  Manually creating a list means that errors will be introduced when the schema changes
  3.  would there ever be a valid reason that flow_multiplier_schedule or entering_water_mains_temperature_schedule

**[Back](../_toc.md)**
