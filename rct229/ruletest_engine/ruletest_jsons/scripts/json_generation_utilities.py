import json
import os


def get_nested_dict(dic, keys):
    """ Used to get nested python dictionary strings
        Example: get_nested_reference_dict(my_dict, ['a', 'b', 'c']) returns my_dict['a']['b']['c']

        Parameters
        ----------
        dic : dictionary
            Dictionary of nested dictionaries.
        keys: list
            Key names used for writing in the nested dictionary

        Returns
        -------
        dic: dictionary

            Returns the referenced Python dictionary.
    """

    # Generate a nested dictionary, slowly building on a reference nested dictionary each iteration through the loop.
    for key in keys:

        # Parse key and determine if this key references a list or a value. If list_index returns an integer (i.e., a
        # reference index in a list) this key represents a list in the dictionary and needs to be set differently
        # EXAMPLE: The key "buildings[0]" implies the "buildings" key represents a list. We set the value at
        # element 0 in the this list

        key, list_index = parse_key_string(key)
        is_list = isinstance(list_index, int)

        # If this is the first key, set the reference dictionary to the highest level dictionary and work down from
        # there.
        if key == keys[0]:
            # If first key isnt initialized, set it as a dictionary
            if key not in dic:
                dic[key] = {}
            reference_dict = dic[key]

        # If the final key, return the referenced final, nested dictionary
        elif key == keys[-1]:

            if key not in reference_dict:
                reference_dict[key] = {}

            return reference_dict

        # If neither the first nor final key in list, continue drilling down through nested dictionaries.
        else:
            if key not in reference_dict:
                if is_list:
                    reference_dict[key] = [{}]
                else:
                    reference_dict[key] = {}

            # If this element in the key_list references a list, index the value defined in 'list_index', else reference
            # the single value specified by the key.
            if is_list:
                # If list isn't long enough, append a new dictionary to it to avoid index out of bounds
                if len(reference_dict[key]) < list_index+1:
                    reference_dict[key].append({})
                reference_dict = reference_dict[key][list_index]
            else:
                reference_dict = reference_dict[key]


def parse_key_string(key_string):
    """ Inspects a string representing a key for any list references. Returns the parsed 'key' and 'list_index' reference
        Example: 'surfaces[1]' references a key = 'surfaces' which represents a list. The '[1]' implies a reference
                  to the second element in the 'surfaces' list. This would return both 'surfaces' and 1.

        Parameters
        ----------
        key_string: str
            String representing a key and possibly a reference to a list index. Example: 'surfaces[1]'

        Returns
        -------
        key: str
            String parsed out of key_string representing a referenced key.
        list_index: int
            Integer representing a list index parsed out of key_string. 'None' if no list reference is found

    """


    # If key specifies an in index (e.g.., something like "[1]" appended afterward a key name), parse the key and
    # index out from the string
    if '[' in key_string:
        split_str = key_string.split('[')
        key = split_str[0]
        list_index = int(split_str[1].replace(']', ''))
    else:
        key = key_string
        list_index = None

    return key, list_index

def set_nested_dict(dic, keys, value):
    """ Used to set nested python dictionary strings. Useful for setting dictionary values for JSON generation.
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

    # Get reference to where to set the value in the original nested dictionary, creating new lists and dictionaries
    # as necessary
    nested_dict = get_nested_dict(dic, keys)

    # Set value
    nested_dict[keys[-1]] = clean_value(value)


def inject_json_path_from_enumeration(key_list, json_path_ref_string):

    """A few JSON paths are shorthanded with an enumeration. This function appends the key_list with the list of keys
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
    json_path_enums_file_path = os.path.join(
        file_dir, "resources", "json_pointer_enumerations.json"
    )

    with open(json_path_enums_file_path) as f:
        # Construct dictionary to map shorthand names for JSON Paths
        # (e.g., path_enum_dict['spaces] = 'buildings/building_segments/thermal_blocks/zones/spaces')
        path_enum_dict = json.load(f)

    # Pull out enumeration key from json_path_ref_string
    json_path_enumeration = json_path_ref_string.split(":")[1].strip()

    # Strip off any list references, will be added back on afterward
    json_path_enumeration, list_index = parse_key_string(json_path_enumeration)

    # Split enumeration path into a list and append it to existing key_list
    # (e.g. 'buildings/building_segments/thermal_blocks/zones/spaces' ->
    #       ['buildings', 'building_segments', 'thermal_blocks', 'zones', 'spaces']
    enumeration_list = path_enum_dict[json_path_enumeration].split("/")

    # Append index back onto final key if JSON_PATH was defined as a list:
    if list_index!= None:
        enumeration_list[-1] = f'{enumeration_list[-1]}[{list_index}]'

    # Inject enumeration list into keylist
    key_list.extend(enumeration_list)


def add_to_dictionary_list(json_dict, key_list, dict_string):
    """Used to add a list of dictionaries to a Python dictionary

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
        dictionary_list = get_nested_dict(json_dict, key_list)
    except TypeError:
        print("TODO: Need to resolve how to do a list inside a list")

    except KeyError:
        set_nested_dict(json_dict, key_list, {})
        dictionary_list = get_nested_dict(json_dict, key_list)

    split_pair = dict_string.split(":")
    key = split_pair[0]  # e.g., id
    value_list = split_pair[1].split(",")  # e.g., 1,2,3

    # Check if a list of dictionaries has already been set at the list key in json_dict. If not, initialize it.
    if not isinstance(dictionary_list, list):
        dictionary_list = []

    # Iterate through each value and add its key/value pair to each sequential dictionary in list
    for i in range(len(value_list)):

        # If a dictionary doesn't exist at element "i", add one
        if len(dictionary_list) < i + 1:
            dictionary_list.append({})

        # Set value for dictionary "i" and key "key"
        dictionary_list[i][key] = clean_value(value_list[i])

    set_nested_dict(json_dict, key_list, dictionary_list)


def clean_value(value):
    """Used to change strings to numerics, if possible.

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


