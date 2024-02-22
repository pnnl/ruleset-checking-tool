import re

from rct229.rulesets.ashrae9012019.data import data

EXTRA_SCHEMA = data["ASHRAE229.9012019.extra.schema"]

exception_list = ["Enumerations2019ASHRAE901", "EnumerationsRESNET", "Enumerations2019T24", "Output2019ASHRAE901"]


def if_required(required):
    if isinstance(required, str):
        return False
    else:
        return required


def get_extra_schema_by_data_type(data_type):
    if data_type.startswith("[") or data_type.startswith("{"):
        # this is a data group
        data_type = ''.join(re.findall(r'[\w\s]+', data_type))
        if EXTRA_SCHEMA.get(data_type):
            return EXTRA_SCHEMA[data_type]["Data Elements"]
    elif data_type.startswith("({"):
        # this is for a referenced external schema.
        data_type = ''.join(re.findall(r'[\w\s]+', data_type))
        return data_type
    return None


def compare_proposed_with_user(proposed, user, error_msg_list, element_path, extra_schema, required_equal):
    matched = True
    if isinstance(proposed, dict):
        # proposed and user object type shall be aligned.
        if user and user.get("id") and required_equal and proposed["id"] != user["id"]:
            error_msg_list.append(f'path: {element_path}: data object {proposed["id"]} does not match {user["id"]}')
            matched = False
        for key in proposed:
            new_element_path = f'{element_path}.{key}'
            key_schema = extra_schema[key]
            extra_schema_data_group = get_extra_schema_by_data_type(key_schema["Data Type"])
            new_extra_schema = extra_schema_data_group if extra_schema_data_group else key_schema["Data Type"]
            if isinstance(new_extra_schema, str) and new_extra_schema in exception_list:
                # avoid processing data outside the master schema
                continue
            matched = compare_proposed_with_user(proposed[key], user.get(key), error_msg_list, new_element_path, new_extra_schema, if_required(key_schema.get("AppG P_RMD Equals U_RMD"))) and matched

    elif isinstance(proposed, list):
        if user and required_equal and len(user) != len(proposed):
            error_msg_list.append(f'path: {element_path}: length of objects ({len(proposed)} in proposed model != length of objects {len(user)} in user model.')
            matched = False
        if all(isinstance(item, dict) for item in proposed):
            # avoid processing any list of primitive data types
            # sort the proposed and user
            sorted_proposed = sorted(proposed, key=lambda x: x["id"])
            sorted_user = sorted(user, key=lambda x: x["id"])
            for i in range(len(sorted_proposed)):
                # in this case, we are still using the same extra_schema
                new_element_path = f'{element_path}[{i}]'
                matched = compare_proposed_with_user(sorted_proposed[i], sorted_user[i], error_msg_list, new_element_path, extra_schema, if_required(extra_schema.get("AppG P_RMD Equals U_RMD"))) and matched

    elif isinstance(extra_schema, str):
        # print(proposed, user, required_equal)
        # in this case, it is either string, numerical, references or other simple data type
        if required_equal:
            if user is None:
                error_msg_list.append(
                    f'path: {element_path}: user is missing this data')
                matched = False
            if proposed is None:
                error_msg_list.append(
                    f'path: {element_path}: proposed is missing this data')
                matched = False
            elif user != proposed:
                error_msg_list.append(
                    f'path: {element_path}: proposed data: {proposed} does not equal to user data: {user}')
                matched = False

    return matched

