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
- **get_component_by_id**
- **compare_context_pair** - there is no RDS for this function, but it is a function developed for Rule 1-6 that compares two elements

**Applicability Checks:**
- no logic here, applies to all P-RMDs



## Rule Logic: 
- create a boolean to keep track of whether everything matches: `all_match = TRUE`
- check if the ServiceWaterHeatingDistributionSystem matches between the propoesd and user models.  First check whether there are the same number of systems: `if len(P_RMD.service_water_heating_distribution_systems) == len(B_RMD.service_water_heating_distribution_systems):`
    - look at each SHW distribution system in the proposed model and see if there is one that is the same in the user model.  This check relies on the understanding that the RCT team has a method for comparing all elements within an object match (compare_context_pair): `for p_SHW_dist_system in P_RMD.service_water_heating_distribution_systems:`
        - if this system is in B_RMD.service_water_heating_distribution_systems, compare the systems: `if p_SHW_dist_system in B_RMD.service_water_heating_distribution_systems:`
            - use compare_context_pair to compare systems and set all_match to FALSE if the systems don't compare: `if !compare_context_pair(p_SHW_dist_system, B_RMD.get_component_by_id(p_SHW_dist_system.id)): all_match = FALSE`
        - otherwise, set all_match to false: `else: all_match = FALSE`
- otherwise, all_match is false: `all_match = FALSE`
- continue if all_match is still true: `if all_match:`
    - do the same comparison for ServiceWaterHeatingEquipment in the proposed and user models: `if len(P_RMD.service_water_heating_distribution_systems) == len(B_RMD.service_water_heating_distribution_systems):`
        - look at each SHW system in the proposed model and see if there is one that is the same in the user model.  This check relies on the understanding that the RCT team has a method for comparing all elements within an object match (compare_context_pair): `for p_SHW_equipment in P_RMD.service_water_heating_equipment:`
              - use compare_context_pair to compare systems and set all_match to FALSE if the systems don't compare: `if !compare_context_pair(p_SHW_equipment, B_RMD.get_component_by_id(p_SHW_equipment.id)): all_match = FALSE`
        - otherwise, set all_match to false: `else: all_match = FALSE`
    - otherwise, all_match is false: `all_match = FALSE`
 
- we also need to compare the pumps connected to the DHW system, but not all pumps in the models are DHW pumps.  Create a list of the SHW pumps `shw_pumps_list = []`
- Iterate through the pumps in the proposed model: `for pump_p in P_RMI.pumps:`
    - check that the pump is connected to a ServiceWaterPiping object: `if type(pump_p.loop_or_piping) == ServiceWaterPiping:`
        - add the pump to the SHW pumps list: `shw_pumps_list.append(pump_p.id)`
- Iterate through the pumps in the user model: `for pump_u in U_RMI.pumps:`
    - check that the pump is connected to a ServiceWaterPiping object: `if type(pump_u.loop_or_piping) == ServiceWaterPiping:`
        - add the pump to the SHW pumps list: `shw_pumps_list.append(pump_u.id)`
- Iterate through the pump ids in the shw pumps list: `for pump_id in set(shw_pumps_list):`
    - find the pump in the proposed model: `pump_p = get_component_by_id(pump_id, P_RMI)`
    - find the pump in the user model: `pump_u = get_component_by_id(pump_id, U_RMI)`
    - if both pump_p and pump_u exist, we compare the inputs: `if type(pump_u) == Pump && type(pump_p) == Pump:`
        - check that the loop_or_piping is the same: `if not pump_p.loop_or_piping.id == pump_u.loop_or_piping.id: all_match = FALSE`
        - check that the specification method is the same: `if not pump_p.specification_method == pump_u.specification_method: all_match = FALSE`
        - check that the design electric power is the same: `if not pump_p.design_electric_power == pump_u.design_electric_power: all_match = FALSE`
        - check that the design speed control is the same: `if not pump_p.speed_control == pump_u.speed_control: all_match = FALSE`

    - otherwise, the pump exists in only one of the two models, set all_match to false: `all_match = FALSE`






  **Rule Assertion:**
  - if all_match is TRUE, then return PASS: `if all_match: return PASS`
  - if all_match is FALSE, return FAIL, one of the elements does not match: `if not all_match: return FAIL`
  
  
  **Notes:**
  1.  using compare_context_pair might not be the correct approach - this function requires data elements in the extra schema to have a tag "AppG P_RMD Equals U_RMD" - is it possible to pass in a custom json created for this rule which identifies which elements need to be equal?
  2.  using compare_context_pair - how are sub-components like [{Tank}] (in ServiceWaterHeatingDistributionSystem) and {Tank} (in SolarThermal and ServiceWaterHeatingEquipment) evaluated? - also {Pump} and {ServiceWaterPiping}

**[Back](../_toc.md)**
