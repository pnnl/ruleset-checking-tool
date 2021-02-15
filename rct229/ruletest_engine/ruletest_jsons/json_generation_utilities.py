

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

    Returns
    -------
    dic: dictionary

        Returns the modified Python dictionary.
    """
    for key in keys[:-1]:
        dic = dic.setdefault(key, {})
    dic[keys[-1]] = value


# Takes a formatted string and returns a list of dictionaries
# e.g. "id:1,2|name:Jack,Jill" = [{id:'1',name:'Jack'},
#                                 {id:'2',name:'Jill'}]

def parse_string_to_dictionary_list(dict_string):
    """ Used to set multiple identical elements in a dictionary. Used for RMR transformations.
    Example: "id:1,2|name:Jack,Jill" = [{id:'1',name:'Jack'},
                                        {id:'2',name:'Jill'}]

    Parameters
    ----------
    dict_string : string
        String separated by colons, commas, and pipes to specify list of dictionaries.
        Example: "id:1,2|name:Jack,Jill" = [{id:'1',name:'Jack'},
                                            {id:'2',name:'Jill'}]
    Returns
    -------
    dictionary_list: dictionary

        Returns the generated Python dictionary.
    """

    dictionary_list = []

    # Remove \n from string
    dict_string = dict_string.replace('\n', '')

    # Split string to get new keys
    # Example of a key_list_pair string: "id:1,2,3"
    key_list_pairs = dict_string.split('|')

    # Iterate through each key_list_pair and set their values in the dictionary list
    for key_list_pair in key_list_pairs:

        split_pair = key_list_pair.split(':')
        key = split_pair[0]                    # e.g., id
        value_list = split_pair[1].split(',')  # e.g., 1,2,3

        # Set key values for each dictionary in dictionary_list
        for i in range(len(value_list)):

            # Define dictionary_list[i] as dictionary if not specified
            if len(dictionary_list) < i+1:
                dictionary_list.append({})

            dictionary_list[i][key] = value_list[i]

    return dictionary_list
