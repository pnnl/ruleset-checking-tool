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

**Applicability Checks:**
- no logic here, applies to all P-RMDs



## Rule Logic: 
- create a boolean to keep track of whether everything matches: `all_match = TRUE`
- all ServiceWaterHeatingDistributionSystems match in the proposed and user models: `if not P_RMI = U_RMI for ServiceWaterHeatingDistributionSystem: all_match = FALSE`
- all ServiceWaterHeatingEquipment matches in the proposed and user models: `if not P_RMI = U_RMI for ServiceWaterHeatingEquipment: all_match = FALSE`
- all DHW tanks match in the proposed and user models **question:** in rare cases, there could be a tank connected to a solar hot water system that does not match in the two models.  Returning FAIL in this case will only trigger a manual review (& these tanks will likely be the same between user and proposed models anyway), so I don't think it's a major issue.  thoughts?: `if not P_RMI = U_RMI for Tank: all_match = FALSE`
- all ServiceWaterPiping matches in the proposed and user models: `if not P_RMI = U_RMI for ServiceWaterPiping: all_match = FALSE`

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

**[Back](../_toc.md)**
