import os
import json

def nested_dict(dic, keys, value):
    """ Used to set nested python dictionary strings (Source: https://stackoverflow.com/a/13688108). Useful for setting
    dictionary values for JSON generation.
    Example: nested_set(my_dict, ['a', 'b', 'c'], 'my_value') is same as my_dict['a']['b']['c'] = 'my_value'

    Parameters
    ----------
    dic : dictionary
        Dictionary on which to append new nested value
    keys: list
        Key names used for writing in the nested dictionary

    value: string
        Value set to the nested dictionary

    """
    for key in keys[:-1]:
        dic = dic.setdefault(key, {})
    value = clean_value(value)
    dic[keys[-1]] = value


# Get a nested dictionary from a list of keys
def nested_get(dic, keys):

    """ Used to get nested python dictionary strings
    Example: nested_get(my_dict, ['a', 'b', 'c']) returns my_dict['a']['b']['c']

    Parameters
    ----------
    dic : dictionary
        Dictionary on which to append new nested value
    keys: list
        Key names used for writing in the nested dictionary

    Returns
    -------
    dic: dictionary

        Returns the referenced Python dictionary.
    """

    for key in keys:
        dic = dic[key]
    return dic

def inject_json_path_from_enumeration(key_list, json_path_ref_string):

    """ A few JSON paths are shorthanded with an enumeration. This function appends the key_list with the list of keys
    found in this shorthand enumeration. These are found in json_pointer_enumerations.json.
     Example: JSON_PATH:spaces = ["buildings","building_segments","thermal_blocks","zones","spaces"]

     Parameters
     ----------
     key_list : list
         List of keys describing the JSON path. The shorthand enumeration's key list is appended onto this list

     json_path_ref_string: str

        String describing which enumeration to use. E.g., "JSON_PATH:spaces"
     """


    # JSON path enumerations. Used to simplify JSON path references in test spreadsheets
    file_dir = os.path.dirname(__file__)
    json_path_enums_file_path = os.path.join(file_dir, 'resources', 'json_pointer_enumerations.json')

    with open(json_path_enums_file_path) as f:
        # Construct dictionary to map shorthand names for JSON Paths
        # (e.g., path_enum_dict['spaces] = 'buildings/building_segments/thermal_blocks/zones/spaces')
        path_enum_dict = json.load(f)

    # Pull out enumeration key from json_path_ref_string
    json_path_enumeration = json_path_ref_string.split(':')[1].strip()

    # Split enumeration path into a list and append it to existing key_list
    # (e.g. 'buildings/building_segments/thermal_blocks/zones/spaces' ->
    #       ['buildings', 'building_segments', 'thermal_blocks', 'zones', 'spaces']
    enumeration_list = path_enum_dict[json_path_enumeration].split('/')

    # Inject enumeration list into keylist
    key_list.extend(enumeration_list)

def add_to_dictionary_list(json_dict, key_list, dict_string):
    """ Used to add a list of dictionaries to a Python dictionary

    Parameters
    ----------
    json_dict : dict
        Python dictionary to be appended with dictionary list

    key_list: list
        List of keys describing where to add this dictionary list

    dict_string: str
        String describing keys for dictionary list. E.g., "id:1,2,3"

    """

    # Remove DICT_LIST from key list
    key_list.pop()

    # Try to get the nested_dictionary where you will set the dictionary list. If KeyError, initialize
    # that JSON path as a dictionary
    try:
        dictionary_list = nested_get(json_dict, key_list)
    except TypeError:
        print('TODO: Need to resolve how to do a list inside a list')

    except KeyError:
        nested_dict(json_dict, key_list, {})
        dictionary_list = nested_get(json_dict, key_list)

    split_pair = dict_string.split(':')
    key = split_pair[0]  # e.g., id
    value_list = split_pair[1].split(',')  # e.g., 1,2,3

    # Check if a list of dictionaries has already been set at the list key in json_dict. If not, initialize it.
    if not isinstance(dictionary_list, list):
        dictionary_list = []

    # Iterate through each value and add its key/value pair to each sequential dictionary in list
    for i in range(len(value_list)):

        # If a dictionary doesn't exist at element "i", add one
        if len(dictionary_list) < i+1:
            dictionary_list.append({})

        # Set value for dictionary "i" and key "key"
        dictionary_list[i][key] = clean_value(value_list[i]) #value_list[i]

    nested_dict(json_dict, key_list, dictionary_list)


def clean_value(value):
    """ Used to change strings to numerics, if possible.

        Parameters
        ----------
        value : str
            String to be cleaned

        """

    # Set value directly if not convertible to a numeric
    if isinstance(value, dict) or isinstance(value, list):
        return value
    else:
        # Set value as integer or float if convertible
        try:
            value = int(value)
            return value
        except ValueError:
            try:
                value = float(value)
                return value
            except ValueError:
                return value




