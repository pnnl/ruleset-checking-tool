# compare_iterative_objects

**Schema Version:** 0.0.23

**Description:** this function is used when two objects need to be compared and one of the fields references a list of objects of the same type.  For example: `ServiceWaterPiping.child_service_water_piping`

**IMPORTANT NOTE TO RCT TEAM:** caution with using getattr_ - the absence of the a key in obj_1 or obj_2 should not result in an error.  Rather if both objects do not have the key, we want the comparison to continue.  If only one object has one of the keys, we want the function to return FALSE.

Also, it would be great if, as keys, this function could accept a reference.id.  For example, if we are comparing two Tanks, we could pass in `[location_zone.id]` to the the id of the zone in which the tank is located

**Inputs:**  
- **RMI_1**: one of the RMIs which holds the object
- **RMI_2**: the other RMI
- **object_id**: the id of the object to be compared
- **fields_list**: a list of fields to be compared with a simple ==
- **schedules_list**: a list of the fields which contain schedules.  Schedules are compared with the compare_schedules function
- **iterative_field**: the name of the field in which the iterative object (or list of objects) exists

**Returns:**  
- **result**: TRUE or FALSE, indicating whether the fields are the same in both files
 
**Function Call:**
- **get_component_by_id**
- **compare_objects**
- **compare_iterative_objects**
- **compare_same_field_in_different_objects**

## Logic:
- call `compare_objects` and continue only if the function is true: `if not compare_objects(RMI_1,RMI_2,object_id,fields_list,schedules_list):`
  - set the result to false and return: `result = FALSE; return result;`
- get the two objects from each RMI: `obj_1 = get_component_by_id(RMI_1,object_id); obj_2 = get_component_by_id(RMI_2,object_id)`

- call compare_same_field_in_different_objects on the iterative field: `if not compare_same_field_in_different_objects(obj_1, obj_2, iterative_field) == SAME:`
  - set the result to false and return: `result = FALSE; return result;`
- check whether the iterative field points to a list: `if type(obj_1.iterative_field) == list):`
  - create a list of object ids for the objects in the list of obj_1: `obj_1_sub_ids = [] for sub_1 in obj_1.iterative_field: obj_1_sub_ids.append(sub_1.id)`
    - iterate through each sub in obj_2: `for sub_2 in obj_2.iterative_field:`
      - check whether the sub_2.id is in the list of subs for obj_1: `if sub_2.id in obj_1_sub_ids:`
        - compare the two subs using compare_iterative_objects: `if not compare_iterative_objects(P_RMI,U_RMI,sub_2.id,fields_list,schedules_list,iterative_field):`



  
- otherwise, the iterative field points to an object, not a list: `else:`

**Returns**  `return result`

**[Back](../_toc.md)**
