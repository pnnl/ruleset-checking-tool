# is_space_a_computer_room

**Description:** Returns true or false as to whether space is a computer room. The criteria is such that it is considered a computer room if the total of misc INFORMATION_TECHNOLOGY_EQUIPMENT Power density in W/sf exceeds 20 W/sf per the definition of a computer room in 90.1 Section 3.  

**Inputs:**  
- **B-RMI,P-RMI**: The applicable ruleset model instance.   
- **Space_obj**: The space to assess whether or not it is a computer room.

**Returns:**  
- **is_space_a_computer_room**: The function returns true or false as to whether space is a computer room. The criteria is such that it is considered a computer room if the total of misc INFORMATION_TECHNOLOGY_EQUIPMENT Power density in W/sf exceeds 20 W/sf per the definition of a computer room in 90.1 Section 3. 
 

**Function Call:**  None  


## Logic:    
- Set is_space_a_computer_room to false: `is_space_a_computer_room = false`               
- Set the total_space_misc_Wattage_including_multiplier variable: `total_space_misc_Wattage_including_multiplier = 0`
- For each miscellaneous equipment id in the space: `For misc_p in space_p.miscellaneous_equipment:`
    - Check if the energy type is electricity, if not then skip this misc_p: `if misc_p.energy_type = "ELECTRICITY":`
        - Check if the energy type is INFORMATION_TECHNOLOGY_EQUIPMENT: `if misc_p.type == "INFORMATION_TECHNOLOGY_EQUIPMENT":`
            - Get the miscellaneous equipment Wattage: `misc_p_power = misc_p.power`
            - Get the maximum of (1.0 and the maximum value in the miscellaneous equipment multiplier schedule) (convert the schedule to an 8760 schedule using a function if needed): `misc_p_multiplier_value = MAX(1,Max(misc_p.multiplier_schedule.hourly_values))`
            - Calculate (misc_p_power * misc_p_multiplier_value) for this misc_p: `misc_p_total_Wattage = misc_p_power * misc_p_multiplier_value`
            - Add to the running total of Wattage associated with the space: `total_space_misc_Wattage_including_multiplier = total_space_misc_Wattage_including_multiplier + misc_p_total_Wattage`
- Get the square footage of the space: `floor_area = space_p.floor_area`
- Calculate the maximum equipment power density for the space (total design Wattage/space sf): `space_EPD = total_space_misc_Wattage_including_multiplier/floor_area`
- Check if it is greater than 20 W/sf: `if space_EPD > 20: is_space_a_computer_room = true`  

**Returns** `is_space_a_computer_room`  

**Questions/Note:**  
1. This logic was recycled from a Section 4 RDS (14-14) .

**[Back](../_toc.md)**
