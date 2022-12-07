# compare_same_field_in_different_objects

**Schema Version:** 0.0.23

**Description:** accepts two objects and a field name.  Compares the contents of the two fields.  For fields that contain a list, it will check the type and length of the list, but not the contents of the list 

**IMPORTANT NOTE TO RCT TEAM:** caution with using getattr_ - the absence of the a key in obj_1 or obj_2 should not result in an error.  Rather if both objects do not have the key, we want the comparison to return TRUE.  If only one object has the key, we want the function to return FALSE.

**Inputs:**  
- **obj_1**: one of the objects
- **obj_2**: the other object
- **field_to_compare**: the name of the field to be compared

**Returns:**  
- **result**: an enum, which can be SAME, NOT_SAME, or NONE - NONE indicates that both fields are null, SAME indicates that both fields match and are not null.  NOT_SAME indicates that the fields do not match (one of them might be null)
 
**Function Call:**

## Logic:
- check if both fields are null: `if obj_1.field_to_compare == NULL && obj_2.field_to_compare == NULL:`
  - set the result to NONE and return: `result = NONE; return result` 
- set the result to false: `result = NOT_SAME`
- check if a simple compare works: `if obj_1.field_to_compare == obj_2.field_to_compare:`
  - set result to TRUE and return: `result = SAME; return result`
- if the objects do not match, it could be because they reference lists or objects.  The first check we do is for lists: `elsif type(obj_1.field_to_compare) == list && type(obj_2.field_to_compare) == list:`
  - check that the length of the lists is the same: `if len(obj_1.field_to_compare) == len(obj_2.field_to_compare):`
    - set result to TRUE and return: `result = SAME; return result`
- if both objects are not lists, it is possible that there is a reference object here: `elsif: obj_1.field_to_compare != NULL && obj_2.field_to_compare != NULL:`
  - the following will need to be contained in a try block because it is possible both fields are not null, and simply not equal: `try:`
    - now check if the id's compare: `if obj_1.field_to_compare.id == obj_2.field_to_compare.id:`
      - set result to TRUE and return: `result = SAME; return result`

**Returns**  `return result`

**[Back](../_toc.md)**
