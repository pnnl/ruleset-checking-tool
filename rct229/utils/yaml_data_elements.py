## file that will read in the schema configuration given the path to the YAML schema (schema_yaml_path)
## then looks at all json files in the folder given by folder_containing_jsons
## outputs a file to output_yaml_path that gives a summary of all the data groups and data elements used
## by the jsons in the folder_containing_jsons

import json
import yaml
import os
from pathlib import Path

folder_containing_jsons = os.path.join(
    Path(__file__).parents[1],"ruletest_engine","ruletest_jsons","ashrae9012019"
)

print("folder containing jsons: " + folder_containing_jsons)

schema_yaml_path = os.path.join(
    Path(__file__).parents[0], "ASHRAE229_extra.schema.yaml"
)

output_yaml_path = os.path.join(
    Path(__file__).parents[0], "data_elements_used.yaml"
)

def used_keys(object_hash,found_keys,data_group_name,reference_hash):
    found_objects = []
    found_keys[data_group_name]["exists"] = True
    for key in object_hash:
        if key in found_keys[data_group_name]:
            found_keys[data_group_name][key] = True
        if key in reference_hash[data_group_name]:
            if isinstance(object_hash[key],list):
                for h in object_hash[key]:
                    found_objects.append({reference_hash[data_group_name][key]: h})
            else:
                found_objects.append({reference_hash[data_group_name][key]: object_hash[key]})
    for new_object in found_objects:
        for new_data_group_name in new_object:
            new_object_hash = new_object[new_data_group_name]
            used_keys(new_object_hash,found_keys,new_data_group_name,reference_hash)


with open(schema_yaml_path) as f:
    schema_yaml_dict = yaml.load(f,Loader = yaml.Loader)

### for the yaml schema parsing:
yaml_found_keys = {}
yaml_reverse_data_groups = {}

## fill the data_groups dictionary with keys before doing next step
for data_group_name in schema_yaml_dict:
    if schema_yaml_dict[data_group_name]["Object Type"] == "Data Group":
        yaml_found_keys[data_group_name] = {}
        yaml_found_keys[data_group_name]["exists"] = False
        yaml_reverse_data_groups[data_group_name] = {}

## now look for where these data groups are referenced by other data groups
for data_group_name in schema_yaml_dict:
    print("data group name: " + data_group_name)
    if schema_yaml_dict[data_group_name]["Object Type"] == "Data Group":
        for data_group_element in schema_yaml_dict[data_group_name]["Data Elements"]:
            print("data group element: " + data_group_element)
            yaml_found_keys[data_group_name][data_group_element] = False

            if "Data Type" in schema_yaml_dict[data_group_name]["Data Elements"][data_group_element]:
                # didn't check for # Data Type: "(<OutputSchemaOptions2019ASHRAE901>, <OutputSchemaOptions2019T24>, OutputSchemaOptionsRESNET)"
                # "{}"

                data_type = schema_yaml_dict[data_group_name]["Data Elements"][data_group_element]["Data Type"]
                if "{" == data_type[:1]:
                    ref = data_type[1:(len(data_type)-1)]
                # "[{}]"
                elif "[{" == data_type[:2]:
                    ref = data_type[2:(len(data_type)-2)]
                else: ref = ""
                if ref in yaml_reverse_data_groups:
                    yaml_reverse_data_groups[data_group_name][data_group_element] = ref
                    #print("ref " + data_group_name + ": " + data_group_element + "; " + ref)

subfolders = [ f.path for f in os.scandir(folder_containing_jsons) if f.is_dir() ]
for subfolder in subfolders:
    for root, dirs, files in os.walk(subfolder):
        for file in files:
            if file.endswith(".json"):
                print(os.path.join(root, file))
                with open(os.path.join(root, file)) as f2:
                    test_list_dictionary = json.load(f2)
                for test_name in test_list_dictionary:
                    if "rmr_transformations" in test_list_dictionary[test_name]:
                        for transformation in test_list_dictionary[test_name]["rmr_transformations"]:
                            used_keys(test_list_dictionary[test_name]["rmr_transformations"][transformation], yaml_found_keys,
                                      "RulesetProjectDescription", yaml_reverse_data_groups)


yaml_output = yaml.dump(yaml_found_keys)
with open(output_yaml_path, "w") as f:
    for key in yaml_found_keys:
        if yaml_found_keys[key]["exists"]:
            f.write(key + ": used \n")
        else:
            f.write(key + ": unused \n")
        for data_element in yaml_found_keys[key]:
            if data_element != "exists":
                f.write("  " + data_element + ":  " + str(yaml_found_keys[key][data_element]) + "\n")
        f.write("\n")
