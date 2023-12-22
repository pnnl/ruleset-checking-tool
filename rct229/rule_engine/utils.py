# Functions for evaluating rules
import json


def _load_json(path: str):
    try:
        with open(path, "r") as json_file:
            rpd_json = json.load(json_file)
            return _helper_convert_id_to_uppercase(rpd_json)
    except FileNotFoundError:
        print(f"Error: The file '{path}' was not found.")
    except json.JSONDecodeError:
        print(f"Error: Invalid RPD format in '{path}'.")
    return None


def _helper_convert_id_to_uppercase(json_obj):
    if isinstance(json_obj, dict):
        new_dict = {}
        for key, value in json_obj.items():
            if isinstance(value, str):
                new_dict[key] = value.upper()
            else:
                new_dict[key] = _helper_convert_id_to_uppercase(value)
        return new_dict
    elif isinstance(json_obj, list):
        return [_helper_convert_id_to_uppercase(item) for item in json_obj]
    else:
        return json_obj


def _assert_rule(val):
    return val


def _assert_equal_rule(user_value, expected_value):
    if user_value == expected_value:
        return True
    else:
        return False


def _compare_rule(val):
    return val


def _select_equal_or_greater(input_value, reference_value):
    if input_value >= reference_value:
        return input_value
    else:
        return reference_value


def _select_equal_or_lesser(input_value, reference_value):
    if input_value <= reference_value:
        return input_value
    else:
        return reference_value
