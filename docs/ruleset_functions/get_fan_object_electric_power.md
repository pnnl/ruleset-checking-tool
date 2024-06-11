# get_fan_object_electric_power 

**Description:** Get the fan power associated with a fan object.  

**Inputs:**  
- **B-RMD,P-RMD**: To calculate and return the fan power associated with the fan object sent to this function.   
- **fan_obj**: The fan object sent to this function.  

**Returns:**  
- **get_fan_object_electric_power**: The function calculates and return the fan power associated with the fan object sent to this function. Returns 0 if fan power is not defined.   
 
**Function Call:**  None  

## Logic:    
- Set the fan_elec_powerequal to zero: `fan_elec_power = 0`
- Get the fan specification method: `fan_spec_method = fan_obj.specification_method`  
- Check if the fan specification method is simple: `if fan_spec_method == "SIMPLE":`  
    - Get the design electric power: `fan_elec_power = fan_obj.design_elecric_power`  
- Else if, fan specification method equals detailed and input_power and motor_efficiency is defined : `Elif fan_spec_method == "DETAILED" AND (fan_obj.input_power != Null or fan_obj.input_power != 0) AND (fan_obj.motor_efficiency != Null or fan_obj.motor_efficiency != 0):`  
    - Calculate the electric power (schema says input power is equivalent in concept to brakehorsepower so divided by the motor efficiency to get input power): `fan_elec_power = fan_obj.input_power/fan_obj.motor_efficiency`  
- Else if, fan specification method equals detailed and design_pressure_rise is defined and total fan efficiency is defined: `Elif fan_spec_method == "DETAILED" AND (fan_obj.design_pressure_rise != Null or fan_obj.design_pressure_rise != 0) AND (fan_obj.total_efficiency != Null or fan_obj.total_efficiency != 0) :`
    - Calculate the electric power (assumes pressure rise is fan total static pressure in units of in. w.g. ): `fan_elec_power = (fan_obj.design_pressure_rise/(8520*fan_obj.total_efficiency)) * 1000`    

- Set the function equal to the calculated fan_elec_power: `get_fan_object_electric_power = fan_elec_power`


**Returns** `get_fan_object_electric_power`  

**Questions:**
1. Should we return error instead of 0 if not enough schema elements are defined to get the fan power? 

**[Back](../_toc.md)**