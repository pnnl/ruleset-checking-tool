# compare_objects

**Schema Version:** 0.0.23

**Description:** compares two objects in different RMIs based on a list of field names
**IMPORTANT NOTE TO RCT TEAM:** caution with using getattr_ - the absence of the a key in obj_1 or obj_2 should not result in an error.  Rather if both objects do not have the key, we want the comparison to continue.  If only one object has one of the keys, we want the function to return FALSE

**Inputs:**  
- **RMI_1**: one of the RMIs which holds the object
- **RMI_2**: the other RMI
- **object_id**: the id of the object to be compared
- **fields_list**: a list of fields to be compared with a simple ==
- **schedules_list**: a list of the fields which contain schedules.  Schedules are compared with the compare_schedules function

**Returns:**  
- **result**: TRUE or FALSE, indicating whether the fields are the same in both files
 
**Function Call:**
- **get_component_by_id**
- **compare_schedules**

## Logic:
- set the result to true: `result = TRUE`
- get the object in RMI_1: `obj_1 = get_component_by_id(RMI_1,object_id)`
- get the object in RMI_2: `obj_2 = get_component_by_id(RMI_2,object_id)`
- if either object is null, set result to false and return: `if(obj_1 == NULL || obj_2 == NULL): result = FALSE; return result`
  - create a variable `index` to iterate through the fields in fields_list: `index = 0`
  - loop through the fields in fields_list, and while result == TRUE, continue matching fields: `while result == TRUE and index < len(fields_list):`
    - check if the values in obj_1 and obj_2: `if obj_1.fields_list[index] == obj_2.fields_list[index]:`
      - the values match, increment tank_index: `index += 1`
    - else the values don't match, set result to FALSE: `else: all_match = FALSE; break`
  - reset index to zero: `index = 0`
  - loop through the fields in schedules_list, and while result == TRUE, continue matching fields: `while result == TRUE and index < len(schedules_list):`
    - get the schedule in RMI_1: `schedule_1 = get_component_by_id(RMI_1, obj_1.schedules_list[index]`
    - get the schedule in RMI_2: `schedule_2 = get_component_by_id(RMI_2, obj_2.schedules_list[index]`
    - if both schedules are null, the values match and we don't need to do a schedule compare: `if not( schedule_1 == schedule_2 && schedule_1 == NULL):`
      - check that both schedules are not equal to NULL: `if schedule_1 != NULL && schdule_2 != NULL:`
      - do the schedule compare by getting the dictionary returned by the compare_schedules function: `schedule_compare_dict = compare_schedules(schedule_1,schedule_2,always_1_schedule)`
        - the schedules match if `schedule_compare_dict["TOTAL_HOURS_COMPARED"] == schedule_compare_dict["TOTAL_HOURS_MATCH"]`, if the schedules DONT match, set result = FALSE and break out of the loop: `if schedule_compare_dict["TOTAL_HOURS_COMPARED"] != schedule_compare_dict["TOTAL_HOURS_MATCH"]: result = FALSE; break`

**Returns**  `return result`

**[Back](../_toc.md)**
